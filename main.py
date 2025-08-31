import asyncio
import aiohttp
import json
import logging
from datetime import datetime
from typing import Optional, Set
from pathlib import Path

# استيراد إعدادات البوت
from config import load_config, BotConfig

# إعداد التسجيل
def setup_logging(log_level: str = "INFO", data_dir: str = "data"):
    """إعداد نظام التسجيل"""
    # إنشاء مجلد logs
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # تحويل مستوى التسجيل
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/bot.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
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
    
    async def get_user_id(self, username: str) -> Optional[str]:
        """الحصول على معرف المستخدم من اسم المستخدم"""
        url = f"{self.base_url}/users/by/username/{username}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['data']['id']
                    else:
                        logger.error(f"خطأ في الحصول على معرف المستخدم: {response.status}")
                        return None
            except Exception as e:
                logger.error(f"خطأ في الاتصال بـ Twitter API: {e}")
                return None
    
    async def get_recent_tweets(self, user_id: str, max_results: int = 10) -> list:
        """الحصول على التغريدات الحديثة للمستخدم (بدون الردود)"""
        url = f"{self.base_url}/users/{user_id}/tweets"
        params = {
            "max_results": max_results,
            "tweet.fields": "created_at,text,public_metrics,attachments,in_reply_to_user_id",
            "media.fields": "url,type,preview_image_url",
            "expansions": "attachments.media_keys",
            "exclude": "replies,retweets"  # استبعاد الردود والريتويت
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        tweets = data.get('data', [])
                        
                        # فلترة إضافية للتأكد من استبعاد الردود
                        filtered_tweets = []
                        for tweet in tweets:
                            # التحقق من أن التغريدة ليست رد
                            if not tweet.get('in_reply_to_user_id'):
                                # التحقق من أن النص لا يبدأ بـ @
                                text = tweet.get('text', '')
                                if not text.startswith('@'):
                                    filtered_tweets.append(tweet)
                        
                        return filtered_tweets
                    else:
                        logger.error(f"خطأ في الحصول على التغريدات: {response.status}")
                        return []
            except Exception as e:
                logger.error(f"خطأ في الاتصال بـ Twitter API: {e}")
                return []

class DiscordWebhook:
    """للتعامل مع Discord Webhook"""
    
    def __init__(self, webhook_url: str, mention_everyone: bool = True):
        self.webhook_url = webhook_url
        self.mention_everyone = mention_everyone
    
    def _format_tweet_message(self, tweet_data: dict, username: str) -> dict:
        """تنسيق رسالة التغريدة لديسكورد"""
        tweet_text = tweet_data.get('text', '')
        tweet_id = tweet_data['id']
        tweet_url = f"https://twitter.com/{username}/status/{tweet_id}"
        created_at = tweet_data.get('created_at', '')
        
        # تنسيق النص
        content = f"**تغريدة جديدة من @{username}:**\n\n{tweet_text}\n\n🔗 [رابط التغريدة]({tweet_url})"
        
        if self.mention_everyone:
            content = f"@everyone\n\n{content}"
        
        # إنشاء Embed للتغريدة
        embed = {
            "title": f"تغريدة جديدة من @{username}",
            "description": tweet_text[:2000],  # حد Discord
            "url": tweet_url,
            "color": 0x1DA1F2,  # لون تويتر
            "timestamp": created_at,
            "footer": {
                "text": "Twitter Bot",
                "icon_url": "https://abs.twimg.com/icons/apple-touch-icon-192x192.png"
            }
        }
        
        return {
            "content": content if self.mention_everyone else None,
            "embeds": [embed]
        }
    
    async def send_tweet(self, tweet_data: dict, username: str) -> bool:
        """إرسال التغريدة إلى ديسكورد"""
        try:
            message_data = self._format_tweet_message(tweet_data, username)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=message_data) as response:
                    if response.status in [200, 204]:
                        logger.info(f"تم إرسال التغريدة {tweet_data['id']} بنجاح")
                        return True
                    else:
                        logger.error(f"خطأ في إرسال التغريدة: {response.status}")
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
        self.user_id: Optional[str] = None
        self.is_running = False
    
    async def initialize(self) -> bool:
        """تهيئة البوت"""
        logger.info("جاري تهيئة البوت...")
        
        # الحصول على معرف المستخدم
        self.user_id = await self.twitter_api.get_user_id(self.config.twitter_username)
        if not self.user_id:
            logger.error(f"فشل في الحصول على معرف المستخدم لـ {self.config.twitter_username}")
            return False
        
        logger.info(f"تم العثور على المستخدم {self.config.twitter_username} (ID: {self.user_id})")
        return True
    
    async def check_new_tweets(self):
        """فحص التغريدات الجديدة"""
        if not self.user_id:
            return
        
        tweets = await self.twitter_api.get_recent_tweets(self.user_id, max_results=10)
        
        # ترتيب التغريدات من الأقدم للأحدث لإرسالها بالتسلسل الصحيح
        tweets.reverse()
        
        for tweet in tweets:
            tweet_id = tweet['id']
            
            if not self.tweet_tracker.is_sent(tweet_id):
                logger.info(f"تغريدة جديدة وُجدت: {tweet_id}")
                
                # إرسال التغريدة إلى ديسكورد
                if await self.discord_webhook.send_tweet(tweet, self.config.twitter_username):
                    self.tweet_tracker.mark_as_sent(tweet_id)
                    # انتظار قصير بين الرسائل لتجنب rate limiting
                    await asyncio.sleep(2)
                else:
                    logger.error(f"فشل في إرسال التغريدة {tweet_id}")
    
    async def run(self):
        """تشغيل البوت"""
        if not await self.initialize():
            logger.error("فشل في تهيئة البوت")
            return
        
        self.is_running = True
        logger.info(f"بدء مراقبة @{self.config.twitter_username} كل {self.config.check_interval} ثانية")
        
        while self.is_running:
            try:
                await self.check_new_tweets()
                await asyncio.sleep(self.config.check_interval)
            except KeyboardInterrupt:
                logger.info("تم إيقاف البوت بواسطة المستخدم")
                self.is_running = False
                break
            except Exception as e:
                logger.error(f"خطأ في دورة البوت: {e}")
                await asyncio.sleep(60)  # انتظار دقيقة عند حدوث خطأ

def load_config() -> BotConfig:
    """تحميل إعدادات البوت من ملف .env"""
    from config import load_config as _load_config
    return _load_config()

async def main():
    """الدالة الرئيسية لتشغيل البوت"""
    try:
        # تحميل الإعدادات
        config = load_config()
        
        # إعداد التسجيل
        setup_logging(config.log_level, config.data_dir)
        logger.info("🤖 بدء تشغيل Twitter-Discord Bridge Bot")
        
        # إنشاء وتشغيل البوت
        bot = TwitterDiscordBot(config)
        await bot.run()
        
    except Exception as e:
        logger.error(f"خطأ في تشغيل البوت: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())