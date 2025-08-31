"""
ملف إدارة الإعدادات للبوت
يركز على استخدام ملف .env بشكل أساسي
"""

import os
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# إعداد logger للإعدادات
logger = logging.getLogger(__name__)

@dataclass
class BotConfig:
    """كلاس إعدادات البوت"""
    twitter_bearer_token: str
    discord_webhook_url: str
    twitter_username: str
    check_interval: int = 300
    mention_everyone: bool = True
    max_tweet_length: int = 2000
    log_level: str = "INFO"
    data_dir: str = "data"

class ConfigLoader:
    """فئة تحميل وإدارة الإعدادات"""
    
    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self._load_env_file()
    
    def _load_env_file(self) -> None:
        """تحميل متغيرات البيئة من ملف .env"""
        env_path = Path(self.env_file)
        
        if not env_path.exists():
            logger.warning(f"ملف .env غير موجود في: {env_path.absolute()}")
            logger.info("سيتم الاعتماد على متغيرات البيئة الموجودة")
            return
        
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # تجاهل الأسطر الفارغة والتعليقات
                    if not line or line.startswith('#'):
                        continue
                    
                    # التحقق من صيغة الخط
                    if '=' not in line:
                        logger.warning(f"صيغة غير صحيحة في السطر {line_num}: {line}")
                        continue
                    
                    # تقسيم المفتاح والقيمة
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # إزالة علامات الاقتباس إن وجدت
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    # تعيين متغير البيئة فقط إذا لم يكن موجوداً
                    if key not in os.environ:
                        os.environ[key] = value
                        logger.debug(f"تم تحميل: {key}")
            
            logger.info(f"تم تحميل ملف .env بنجاح: {env_path}")
            
        except Exception as e:
            logger.error(f"خطأ في تحميل ملف .env: {e}")
            raise
    
    def _get_env_var(self, key: str, default: Optional[str] = None, required: bool = True) -> Optional[str]:
        """الحصول على متغير بيئة مع التحقق"""
        value = os.getenv(key, default)
        
        if required and not value:
            raise ValueError(f"متغير البيئة المطلوب '{key}' غير موجود")
        
        return value
    
    def _get_env_bool(self, key: str, default: bool = False) -> bool:
        """تحويل متغير البيئة إلى boolean"""
        value = os.getenv(key, str(default)).lower()
        return value in ['true', '1', 'yes', 'on', 'نعم']
    
    def _get_env_int(self, key: str, default: int = 0) -> int:
        """تحويل متغير البيئة إلى integer"""
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            logger.warning(f"قيمة غير صحيحة لـ {key}، سيتم استخدام القيمة الافتراضية: {default}")
            return default
    
    def load_config(self) -> BotConfig:
        """تحميل جميع الإعدادات وإنشاء كائن BotConfig"""
        try:
            # المتغيرات المطلوبة
            twitter_token = self._get_env_var('TWITTER_BEARER_TOKEN', required=True)
            discord_webhook = self._get_env_var('DISCORD_WEBHOOK_URL', required=True)
            twitter_username = self._get_env_var('TWITTER_USERNAME', required=True)
            
            # المتغيرات الاختيارية
            check_interval = self._get_env_int('CHECK_INTERVAL', 300)
            mention_everyone = self._get_env_bool('MENTION_EVERYONE', True)
            max_tweet_length = self._get_env_int('MAX_TWEET_LENGTH', 2000)
            log_level = self._get_env_var('LOG_LEVEL', 'INFO', required=False)
            data_dir = self._get_env_var('DATA_DIR', 'data', required=False)
            
            # التحقق من صحة القيم
            self._validate_config(twitter_token, discord_webhook, twitter_username, check_interval)
            
            config = BotConfig(
                twitter_bearer_token=twitter_token,
                discord_webhook_url=discord_webhook,
                twitter_username=twitter_username,
                check_interval=check_interval,
                mention_everyone=mention_everyone,
                max_tweet_length=max_tweet_length,
                log_level=log_level,
                data_dir=data_dir
            )
            
            logger.info("تم تحميل الإعدادات بنجاح")
            logger.info(f"الحساب المراقب: @{twitter_username}")
            logger.info(f"فترة الفحص: {check_interval} ثانية")
            logger.info(f"منشن الكل: {'مفعل' if mention_everyone else 'معطل'}")
            
            return config
            
        except Exception as e:
            logger.error(f"خطأ في تحميل الإعدادات: {e}")
            raise
    
    def _validate_config(self, token: str, webhook: str, username: str, interval: int) -> None:
        """التحقق من صحة الإعدادات الأساسية"""
        # التحقق من Twitter Bearer Token
        if not token.startswith(('AAAAAAAAAA', 'Bearer ')):
            logger.warning("تنسيق Twitter Bearer Token قد يكون غير صحيح")
        
        # التحقق من Discord Webhook URL
        if not webhook.startswith('https://discord.com/api/webhooks/'):
            raise ValueError("رابط Discord Webhook غير صحيح")
        
        # التحقق من اسم المستخدم
        if username.startswith('@'):
            raise ValueError("اسم المستخدم يجب أن يكون بدون @ في البداية")
        
        # التحقق من فترة الفحص
        if interval < 60:
            logger.warning("فترة الفحص أقل من دقيقة واحدة قد تتسبب في تجاوز حدود API")
        
        if interval > 3600:
            logger.warning("فترة الفحص أكثر من ساعة قد تفوت تغريدات مهمة")

def create_env_file_template(file_path: str = ".env") -> None:
    """إنشاء ملف .env كمثال إذا لم يكن موجوداً"""
    env_path = Path(file_path)
    
    if env_path.exists():
        logger.info(f"ملف .env موجود بالفعل: {env_path}")
        return
    
    template = '''# إعدادات Twitter API
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here

# إعدادات Discord
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your/webhook/url/here

# إعدادات الحساب المراقب  
TWITTER_USERNAME=gaming_news_account

# إعدادات البوت (اختيارية)
CHECK_INTERVAL=300
MENTION_EVERYONE=true
MAX_TWEET_LENGTH=2000
LOG_LEVEL=INFO
DATA_DIR=data

# ملاحظات مهمة:
# 1. احرص على عدم مشاركة هذا الملف مع أحد
# 2. أدخل المعلومات الحقيقية بدلاً من القيم التجريبية
# 3. تأكد من إضافة .env إلى .gitignore
'''
    
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(template)
        logger.info(f"تم إنشاء ملف .env في: {env_path}")
        logger.info("يرجى تعديل الملف وإدخال المعلومات الحقيقية")
    except Exception as e:
        logger.error(f"خطأ في إنشاء ملف .env: {e}")
        raise

def setup_directories(config: BotConfig) -> None:
    """إنشاء المجلدات المطلوبة"""
    directories = [
        config.data_dir,
        "logs"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"تم إنشاء المجلد: {directory}")

def load_config(env_file: str = ".env") -> BotConfig:
    """دالة مساعدة لتحميل الإعدادات بسرعة"""
    config_loader = ConfigLoader(env_file)
    config = config_loader.load_config()
    setup_directories(config)
    return config

# دالة للاختبار السريع
if __name__ == "__main__":
    # إعداد تسجيل بسيط للاختبار
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    try:
        # إنشاء ملف .env إذا لم يكن موجوداً
        create_env_file_template()
        
        # محاولة تحميل الإعدادات
        config = load_config()
        print("✅ تم تحميل الإعدادات بنجاح!")
        print(f"الحساب المراقب: @{config.twitter_username}")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        print("تأكد من تعديل ملف .env بالمعلومات الصحيحة")