import asyncio
import aiohttp
import json
import logging
import re
import signal
import sys
from datetime import datetime, timezone
from typing import Optional, Set, Dict, List
from pathlib import Path
from fastapi import FastAPI, Request, Response

# استيراد إعدادات البوت
from config import load_config, BotConfig

# إنشاء تطبيق FastAPI
app = FastAPI(title="Twitter-Discord Bridge Bot")

@app.get("/")
async def health_check():
    """Endpoint بسيط للتحقق من صحة الخدمة"""
    return {"status": "ok", "bot_running": bot_instance.is_running if bot_instance else False}


@app.get("/health")
@app.head("/health")
async def health_check_endpoint(request: Request):
    """
    GET: يعيد JSON يحتوي على حالة البوت.
    HEAD: يعيد status code فقط.
    """
    if request.method == "HEAD":
        return Response(status_code=200)

    status_data = {
        "status": "ok",
        "bot_running": getattr(bot_instance, "is_running", False),
        "timestamp": datetime.utcnow().isoformat()
    }
    return status_data


@app.on_event("startup")
async def startup_event():
    """تشغيل البوت عند بدء السيرفر"""
    global bot_instance
    if bot_instance is None:
        config = load_config()
        setup_logging(config.log_level, config.data_dir)
        bot_instance = TwitterDiscordBot(config)
        # تشغيل البوت في الخلفية
        asyncio.create_task(bot_instance.run())

# إعداد التسجيل
def setup_logging(log_level: str = "INFO", data_dir: str = "data"):
    """إعداد نظام التسجيل"""
    # إنشاء مجلد logs
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # تحويل مستوى التسجيل
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # إزالة المعالجات الموجودة لتجنب التكرار
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/bot.log', encoding='utf-8'),
            logging.StreamHandler()
        ],
        force=True  # لضمان إعادة الإعداد
    )

logger = logging.getLogger(__name__)

class TweetTracker:
    """لتتبع التغريدات المرسلة لتجنب التكرار"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.file_path = self.data_dir / "sent_tweets.json"
        self.sent_tweets: Set[str] = self._load_sent_tweets()
    
    def _load_sent_tweets(self) -> Set[str]:
        """تحميل التغريدات المرسلة من الملف"""
        try:
            if Path(self.file_path).exists():
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(data.get('sent_tweets', []))
        except Exception as e:
            logger.error(f"خطأ في تحميل التغريدات المرسلة: {e}")
        return set()
    
    def _save_sent_tweets(self):
        """حفظ التغريدات المرسلة في الملف"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump({'sent_tweets': list(self.sent_tweets)}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"خطأ في حفظ التغريدات المرسلة: {e}")
    
    def is_sent(self, tweet_id: str) -> bool:
        """التحقق من إرسال التغريدة مسبقاً"""
        return tweet_id in self.sent_tweets
    
    def mark_as_sent(self, tweet_id: str):
        """تحديد التغريدة كمرسلة"""
        self.sent_tweets.add(tweet_id)
        self._save_sent_tweets()

class TwitterAPI:
    """للتعامل مع Twitter API"""
    
    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2"
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        self.rate_limit_remaining = None
        self.rate_limit_reset = None
    
    async def handle_rate_limit(self, response_headers: dict = None):
        """معالجة تجاوز الحد المسموح"""
        wait_time = 900  # افتراضي 15 دقيقة
        
        if response_headers:
            # محاولة الحصول على وقت إعادة التجديد من headers
            reset_time = response_headers.get('x-rate-limit-reset')
            remaining = response_headers.get('x-rate-limit-remaining', '0')
            
            logger.warning(f"Rate Limit - المتبقي: {remaining}")
            
            if reset_time:
                try:
                    reset_timestamp = int(reset_time)
                    current_time = datetime.now().timestamp()
                    wait_time = max(reset_timestamp - current_time + 60, 900)  # إضافة دقيقة أمان
                except (ValueError, TypeError):
                    pass
        
        logger.warning(f"سيتم الانتظار {wait_time/60:.1f} دقيقة حتى إعادة التجديد")
        await asyncio.sleep(wait_time)
    
    async def get_user_info(self, username: str) -> Optional[Dict]:
        """الحصول على معلومات المستخدم الكاملة"""
        url = f"{self.base_url}/users/by/username/{username}"
        params = {
            "user.fields": "id,name,username,description,profile_image_url,verified,public_metrics"
        }
        
        max_retries = 2  # تقليل عدد المحاولات
        for attempt in range(max_retries):
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, headers=self.headers, params=params) as response:
                        # تحديث معلومات Rate Limit
                        self.rate_limit_remaining = response.headers.get('x-rate-limit-remaining')
                        
                        if response.status == 200:
                            data = await response.json()
                            return data['data']
                        elif response.status == 429:
                            if attempt < max_retries - 1:
                                logger.warning(f"Rate limit في الحصول على معلومات المستخدم")
                                await self.handle_rate_limit(dict(response.headers))
                                continue
                            else:
                                logger.error("تجاوز الحد الأقصى للمحاولات - معلومات المستخدم")
                                return None
                        else:
                            logger.error(f"خطأ في الحصول على معلومات المستخدم: {response.status}")
                            error_text = await response.text()
                            logger.error(f"تفاصيل الخطأ: {error_text}")
                            return None
                except Exception as e:
                    logger.error(f"خطأ في الاتصال بـ Twitter API: {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(30)
                        continue
                    return None
    
    async def get_recent_tweets(self, user_id: str, max_results: int = 10) -> tuple[list, dict]:
        """الحصول على التغريدات الحديثة للمستخدم مع الميديا"""
        # التأكد من أن max_results بين 5 و 100
        max_results = max(5, min(max_results, 100))
        
        url = f"{self.base_url}/users/{user_id}/tweets"
        params = {
            "max_results": max_results,
            "tweet.fields": "created_at,text,public_metrics,attachments,in_reply_to_user_id,context_annotations,entities",
            "media.fields": "url,type,preview_image_url,width,height,alt_text",
            "expansions": "attachments.media_keys",
            "exclude": "replies,retweets"
        }
        
        # محاولة واحدة فقط لتوفير API calls
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, params=params) as response:
                    # تحديث معلومات Rate Limit
                    self.rate_limit_remaining = response.headers.get('x-rate-limit-remaining')
                    
                    if response.status == 200:
                        data = await response.json()
                        tweets = data.get('data', [])
                        media_info = {}
                        
                        # معالجة معلومات الميديا
                        if 'includes' in data and 'media' in data['includes']:
                            for media in data['includes']['media']:
                                media_info[media['media_key']] = media
                        
                        # فلترة الردود والريتويت
                        filtered_tweets = []
                        for tweet in tweets:
                            if not tweet.get('in_reply_to_user_id'):
                                text = tweet.get('text', '')
                                if not text.startswith('@') and not text.startswith('RT @'):
                                    filtered_tweets.append(tweet)
                        
                        logger.debug(f"تم جلب {len(filtered_tweets)} تغريدة، Rate limit متبقي: {self.rate_limit_remaining}")
                        return filtered_tweets, media_info
                        
                    elif response.status == 429:
                        logger.warning("Rate limit عند جلب التغريدات")
                        await self.handle_rate_limit(dict(response.headers))
                        return [], {}
                        
                    else:
                        logger.error(f"خطأ في الحصول على التغريدات: {response.status}")
                        error_text = await response.text()
                        logger.error(f"تفاصيل الخطأ: {error_text}")
                        return [], {}
                        
            except Exception as e:
                logger.error(f"خطأ في الاتصال بـ Twitter API: {e}")
                return [], {}

class DiscordWebhook:
    """للتعامل مع Discord Webhook"""
    
    def __init__(self, webhook_url: str, mention_everyone: bool = True):
        self.webhook_url = webhook_url
        self.mention_everyone = mention_everyone
    
    def _format_numbers(self, num: int) -> str:
        """تنسيق الأرقام بشكل جميل"""
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        return str(num)
    
    def _format_timestamp(self, created_at: str) -> str:
        """تنسيق الوقت"""
        try:
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except:
            return created_at
    
    def _clean_tweet_text(self, text: str, max_length: int = 2000) -> str:
        """تنظيف نص التغريدة من الروابط القصيرة"""
        # إزالة روابط t.co
        text = re.sub(r'https://t\.co/\w+', '', text)
        # إزالة المسافات الإضافية
        text = re.sub(r'\s+', ' ', text).strip()
        # قطع النص إذا كان طويلاً
        if len(text) > max_length:
            text = text[:max_length-3] + "..."
        return text
    
    def _extract_hashtags_and_mentions(self, tweet_data: dict) -> tuple[List[str], List[str]]:
        """استخراج الهاشتاغات والمنشن"""
        hashtags = []
        mentions = []
        
        entities = tweet_data.get('entities', {})
        
        if 'hashtags' in entities:
            hashtags = [f"#{tag['tag']}" for tag in entities['hashtags']]
        
        if 'mentions' in entities:
            mentions = [f"@{mention['username']}" for mention in entities['mentions']]
        
        return hashtags, mentions
    
    def _create_embed(self, tweet_data: dict, username: str, user_info: dict, media_info: dict, max_length: int = 2000, is_startup: bool = False) -> dict:
        """إنشاء embed احترافي للتغريدة"""
        tweet_text = self._clean_tweet_text(tweet_data.get('text', ''), max_length)
        tweet_id = tweet_data['id']
        tweet_url = f"https://twitter.com/{username}/status/{tweet_id}"
        created_at = tweet_data.get('created_at', '')
        metrics = tweet_data.get('public_metrics', {})
        
        # استخراج الهاشتاغات والمنشن
        hashtags, mentions = self._extract_hashtags_and_mentions(tweet_data)
        
        # إنشاء الـ embed الأساسي
        embed_title = "🎯 فحص أولي - تغريدة" if is_startup else "🐦 تغريدة جديدة"
        embed_color = 0x00FF00 if is_startup else 0x1DA1F2
        
        embed = {
            "title": embed_title,
            "description": tweet_text[:2000] if tweet_text else "_بدون نص_",
            "url": tweet_url,
            "color": embed_color,
            "timestamp": created_at,
            "author": {
                "name": f"{user_info.get('name', username)} (@{username})",
                "url": f"https://twitter.com/{username}",
                "icon_url": user_info.get('profile_image_url', '').replace('_normal', '_400x400') if user_info.get('profile_image_url') else None
            },
            "footer": {
                "text": f"Twitter • {self._format_timestamp(created_at)}",
                "icon_url": "https://abs.twimg.com/icons/apple-touch-icon-192x192.png"
            },
            "fields": []
        }
        
        # إضافة الإحصائيات
        if metrics:
            stats_text = []
            if metrics.get('like_count', 0) > 0:
                stats_text.append(f"❤️ {self._format_numbers(metrics['like_count'])}")
            if metrics.get('retweet_count', 0) > 0:
                stats_text.append(f"🔄 {self._format_numbers(metrics['retweet_count'])}")
            if metrics.get('reply_count', 0) > 0:
                stats_text.append(f"💬 {self._format_numbers(metrics['reply_count'])}")
            
            if stats_text:
                embed["fields"].append({
                    "name": "📊 الإحصائيات",
                    "value": " • ".join(stats_text),
                    "inline": True
                })
        
        # إضافة الهاشتاغات إذا وُجدت
        if hashtags and len(hashtags) <= 5:
            hashtags_text = " ".join(hashtags[:5])
            embed["fields"].append({
                "name": "🏷️ الهاشتاغات",
                "value": hashtags_text,
                "inline": True
            })
        
        # معالجة الميديا المرفقة
        if 'attachments' in tweet_data and 'media_keys' in tweet_data['attachments']:
            media_keys = tweet_data['attachments']['media_keys']
            
            for i, media_key in enumerate(media_keys):
                if media_key in media_info:
                    media = media_info[media_key]
                    media_type = media.get('type', '')
                    
                    if media_type == 'photo' and i == 0:
                        # استخدام أول صورة كـ main image
                        embed["image"] = {"url": media.get('url', '')}
                    elif media_type == 'video' and i == 0:
                        # للفيديو: استخدام preview image
                        if media.get('preview_image_url'):
                            embed["image"] = {"url": media['preview_image_url']}
        
        return embed
    
    def _format_tweet_message(self, tweet_data: dict, username: str, user_info: dict, media_info: dict, max_length: int = 2000, is_startup: bool = False) -> dict:
        """تنسيق رسالة التغريدة لديسكورد"""
        tweet_id = tweet_data['id']
        tweet_url = f"https://twitter.com/{username}/status/{tweet_id}"
        
        # إنشاء المحتوى الرئيسي
        display_name = user_info.get('name', username) if user_info else username
        verified_badge = " ✅" if user_info and user_info.get('verified') else ""
        
        content_parts = []
        
        if is_startup:
            content_parts.append("🎯 **فحص أولي للبوت**")
        else:
            if self.mention_everyone:
                content_parts.append("@everyone")
            content_parts.append(f"**{display_name}**{verified_badge} غرد للتو!")
        
        content_parts.append(f"🔗 **[اقرأ التغريدة الكاملة]({tweet_url})**")
        content = "\n".join(content_parts)
        
        # إنشاء الـ embed
        embed = self._create_embed(tweet_data, username, user_info, media_info, max_length, is_startup)
        
        return {
            "content": content,
            "embeds": [embed],
            "allowed_mentions": {
                "everyone": self.mention_everyone and not is_startup
            }
        }
    
    async def send_tweet(self, tweet_data: dict, username: str, user_info: dict, media_info: dict, max_length: int = 2000, is_startup: bool = False) -> bool:
        """إرسال التغريدة إلى ديسكورد"""
        try:
            message_data = self._format_tweet_message(tweet_data, username, user_info, media_info, max_length, is_startup)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=message_data) as response:
                    if response.status in [200, 204]:
                        tweet_type = "فحص أولي" if is_startup else "تغريدة"
                        logger.info(f"تم إرسال {tweet_type} {tweet_data['id']} بنجاح")
                        return True
                    elif response.status == 429:
                        logger.warning("Rate limit في Discord webhook")
                        await asyncio.sleep(5)
                        return False
                    else:
                        error_text = await response.text()
                        logger.error(f"خطأ في إرسال التغريدة: {response.status} - {error_text}")
                        return False
        except Exception as e:
            logger.error(f"خطأ في إرسال الرسالة: {e}")
            return False

class TwitterDiscordBot:
    """البوت الرئيسي"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.twitter_api = TwitterAPI(config.twitter_bearer_token)
        self.discord_webhook = DiscordWebhook(config.discord_webhook_url, config.mention_everyone)
        self.tweet_tracker = TweetTracker(config.data_dir)
        self.user_info: Optional[Dict] = None
        self.is_running = False
        self.startup_check_done = False
        self.shutdown_requested = False
    
    async def initialize(self) -> bool:
        """تهيئة البوت"""
        logger.info("جاري تهيئة البوت...")
        
        # الحصول على معلومات المستخدم الكاملة
        self.user_info = await self.twitter_api.get_user_info(self.config.twitter_username)
        if not self.user_info:
            logger.error(f"فشل في الحصول على معلومات المستخدم لـ {self.config.twitter_username}")
            return False
        
        logger.info(f"تم العثور على المستخدم {self.user_info['name']} (@{self.config.twitter_username})")
        return True
    
    async def perform_startup_check(self):
        """إجراء الفحص الأولي وإرسال آخر 3 تغريدات"""
        if not self.user_info:
            logger.warning("معلومات المستخدم غير متوفرة للفحص الأولي")
            return
        
        logger.info("🎯 بدء الفحص الأولي - إرسال آخر 3 تغريدات للتأكد من عمل البوت")
        
        user_id = self.user_info['id']
        tweets, media_info = await self.twitter_api.get_recent_tweets(user_id, max_results=5)
        
        if not tweets:
            logger.warning("لم يتم العثور على تغريدات للفحص الأولي")
            return
        
        # إرسال آخر 3 تغريدات (أو أقل إذا لم تكن متوفرة)
        recent_tweets = tweets[:3]
        
        logger.info(f"سيتم إرسال {len(recent_tweets)} تغريدة للفحص الأولي")
        
        for i, tweet in enumerate(recent_tweets):
            tweet_id = tweet['id']
            
            # إرسال التغريدة مع علامة الفحص الأولي
            success = await self.discord_webhook.send_tweet(
                tweet, 
                self.config.twitter_username, 
                self.user_info, 
                media_info, 
                self.config.max_tweet_length,
                is_startup=True
            )
            
            if success:
                # تسجيل التغريدة كمرسلة لتجنب إعادة الإرسال
                self.tweet_tracker.mark_as_sent(tweet_id)
                
                # انتظار 3 ثواني بين الرسائل لتجنب spam
                if i < len(recent_tweets) - 1:
                    await asyncio.sleep(3)
            else:
                logger.error(f"فشل في إرسال تغريدة الفحص الأولي {tweet_id}")
        
        logger.info("✅ تم الانتهاء من الفحص الأولي")
    
    async def check_new_tweets(self):
        """فحص التغريدات الجديدة"""
        if not self.user_info:
            logger.warning("معلومات المستخدم غير متوفرة، محاولة إعادة التهيئة...")
            if not await self.initialize():
                return
        
        user_id = self.user_info['id']
        # استخدام قيمة أقل لتوفير API calls
        tweets, media_info = await self.twitter_api.get_recent_tweets(user_id, max_results=5)
        
        if not tweets:
            logger.debug("لا توجد تغريدات جديدة")
            return
        
        # ترتيب التغريدات من الأقدم للأحدث
        tweets.reverse()
        
        new_tweets_count = 0
        for tweet in tweets:
            if self.shutdown_requested:
                break
                
            tweet_id = tweet['id']
            
            if not self.tweet_tracker.is_sent(tweet_id):
                logger.info(f"تغريدة جديدة وُجدت: {tweet_id}")
                
                # إرسال التغريدة إلى ديسكورد
                success = await self.discord_webhook.send_tweet(
                    tweet, 
                    self.config.twitter_username, 
                    self.user_info, 
                    media_info, 
                    self.config.max_tweet_length
                )
                
                if success:
                    self.tweet_tracker.mark_as_sent(tweet_id)
                    new_tweets_count += 1
                    # انتظار بين الرسائل
                    if not self.shutdown_requested:
                        await asyncio.sleep(3)
                else:
                    logger.error(f"فشل في إرسال التغريدة {tweet_id}")
        
        if new_tweets_count > 0:
            logger.info(f"تم إرسال {new_tweets_count} تغريدة جديدة")
    
    async def send_startup_message(self):
        """إرسال رسالة بدء التشغيل"""
        if not self.user_info:
            return
        
        startup_embed = {
            "title": "🤖 تم تشغيل البوت بنجاح",
            "description": f"بدأت مراقبة حساب **{self.user_info['name']}** (@{self.config.twitter_username})",
            "color": 0x00FF00,  # أخضر
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "thumbnail": {
                "url": self.user_info.get('profile_image_url', '').replace('_normal', '_400x400') if self.user_info.get('profile_image_url') else None
            },
            "fields": [
                {
                    "name": "⏱️ فترة المراقبة",
                    "value": f"كل {self.config.check_interval} ثانية ({self.config.check_interval//60} دقيقة)",
                    "inline": True
                },
                {
                    "name": "📊 إحصائيات الحساب",
                    "value": f"👥 {self._format_numbers(self.user_info.get('public_metrics', {}).get('followers_count', 0))} متابع",
                    "inline": True
                },
                {
                    "name": "🎯 الفحص الأولي",
                    "value": "سيتم إرسال آخر 3 تغريدات للتأكد من عمل البوت",
                    "inline": False
                }
            ],
            "footer": {
                "text": "Twitter Bridge Bot • جاهز للعمل",
                "icon_url": "https://abs.twimg.com/icons/apple-touch-icon-192x192.png"
            }
        }
        
        message_data = {
            "embeds": [startup_embed]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.discord_webhook.webhook_url, json=message_data) as response:
                    if response.status in [200, 204]:
                        logger.info("تم إرسال رسالة بدء التشغيل")
                    else:
                        logger.error(f"خطأ في إرسال رسالة بدء التشغيل: {response.status}")
        except Exception as e:
            logger.error(f"خطأ في إرسال رسالة بدء التشغيل: {e}")
    
    def _format_numbers(self, num: int) -> str:
        """تنسيق الأرقام بشكل جميل"""
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        return str(num)
    
    def shutdown(self):
        """طلب إيقاف البوت بشكل آمن"""
        logger.info("تم طلب إيقاف البوت...")
        self.shutdown_requested = True
        self.is_running = False
    
    async def run(self):
        """تشغيل البوت"""
        # محاولة التهيئة مع إعادة المحاولة
        max_init_attempts = 3
        for attempt in range(max_init_attempts):
            if await self.initialize():
                break
            elif attempt < max_init_attempts - 1:
                logger.info(f"إعادة محاولة التهيئة ({attempt + 2}/{max_init_attempts}) بعد دقيقتين...")
                await asyncio.sleep(120)
            else:
                logger.error("فشل في تهيئة البوت بعد عدة محاولات")
                return
        
        # إرسال رسالة بدء التشغيل
        await self.send_startup_message()
        
        # إجراء الفحص الأولي
        await self.perform_startup_check()
        
        self.is_running = True
        logger.info(f"بدء مراقبة @{self.config.twitter_username} كل {self.config.check_interval} ثانية")
        
        # استخدام فترة المراقبة من الإعدادات
        check_interval = self.config.check_interval
        
        while self.is_running and not self.shutdown_requested:
            try:
                await self.check_new_tweets()
                
                # انتظار بشكل قابل للمقاطعة
                for _ in range(check_interval):
                    if self.shutdown_requested:
                        break
                    await asyncio.sleep(1)
                    
            except asyncio.CancelledError:
                logger.info("تم إلغاء مهمة البوت")
                break
            except KeyboardInterrupt:
                logger.info("تم إيقاف البوت بواسطة المستخدم")
                break
            except Exception as e:
                logger.error(f"خطأ في دورة البوت: {e}")
                # انتظار 5 دقائق عند حدوث خطأ
                for _ in range(300):
                    if self.shutdown_requested:
                        break
                    await asyncio.sleep(1)
        
        # إرسال رسالة إيقاف التشغيل
        await self.send_shutdown_message()
    
    async def send_shutdown_message(self):
        """إرسال رسالة إيقاف التشغيل"""
        shutdown_embed = {
            "title": "⏸️ تم إيقاف البوت",
            "description": f"توقفت مراقبة حساب **@{self.config.twitter_username}**",
            "color": 0xFF0000,  # أحمر
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "footer": {
                "text": "Twitter Bridge Bot • متوقف",
                "icon_url": "https://abs.twimg.com/icons/apple-touch-icon-192x192.png"
            }
        }
        
        message_data = {
            "embeds": [shutdown_embed]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.discord_webhook.webhook_url, json=message_data) as response:
                    if response.status in [200, 204]:
                        logger.info("تم إرسال رسالة إيقاف التشغيل")
        except Exception as e:
            logger.error(f"خطأ في إرسال رسالة إيقاف التشغيل: {e}")

# متغير عام للبوت لاستخدامه في signal handler
bot_instance = None

def signal_handler(signum, frame):
    """معالج إشارات النظام لإيقاف البوت بشكل آمن"""
    global bot_instance
    if bot_instance:
        logger.info(f"تم استلام إشارة {signum}، جاري إيقاف البوت...")
        bot_instance.shutdown()
    else:
        logger.info("تم طلب إيقاف البوت")
        sys.exit(0)

def load_config() -> BotConfig:
    """تحميل إعدادات البوت من ملف .env"""
    from config import load_config as _load_config
    return _load_config()

async def main():
    """الدالة الرئيسية لتشغيل البوت"""
    global bot_instance
    
    try:
        # إعداد معالجات الإشارات
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # تحميل الإعدادات
        config = load_config()
        
        # إعداد التسجيل
        setup_logging(config.log_level, config.data_dir)
        logger.info("🤖 بدء تشغيل Twitter-Discord Bridge Bot")
        logger.info(f"📊 الإعدادات: فترة المراقبة={config.check_interval}ث، منشن الكل={config.mention_everyone}")
        
        # إنشاء وتشغيل البوت
        bot_instance = TwitterDiscordBot(config)
        await bot_instance.run()
        
    except KeyboardInterrupt:
        logger.info("تم إيقاف البوت بواسطة المستخدم (Ctrl+C)")
    except Exception as e:
        logger.error(f"خطأ في تشغيل البوت: {e}")
        raise
    finally:
        logger.info("تم إغلاق البوت بنجاح")

if __name__ == "__main__":
    import os
    import sys
    import uvicorn

    port = int(os.environ.get("PORT", 8000))  # Render يعطيك Port

    try:
        uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف البوت بواسطة المستخدم")
        sys.exit(0)
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")
        sys.exit(1)
