#!/usr/bin/env python3
"""
سكريبت تشغيل بوت نقل تغريدات تويتر إلى ديسكورد
مع إعداد تفاعلي لملف .env للمستخدمين الجدد
"""

import asyncio
import os
import sys
from pathlib import Path

def create_env_file():
    """إنشاء ملف .env تفاعلي"""
    print("🔧 إعداد البوت للمرة الأولى")
    print("=" * 50)
    print("سيتم إنشاء ملف .env مع إعداداتك")
    
    # التحقق من وجود .env.example
    if not Path('.env.example').exists():
        print("⚠️  ملف .env.example غير موجود!")
        print("تأكد من وجود جميع ملفات المشروع")
        return False
    
    print("\n📋 يرجى إدخال المعلومات التالية:")
    print("(يمكنك تركها فارغة واستخدام القيم الافتراضية)")
    
    # المتغيرات المطلوبة
    print("\n🔑 المعلومات المطلوبة:")
    
    twitter_token = input("🐦 Twitter Bearer Token: ").strip()
    if not twitter_token:
        print("❌ Twitter Bearer Token مطلوب!")
        return False
    
    discord_webhook = input("💬 Discord Webhook URL: ").strip()
    if not discord_webhook:
        print("❌ Discord Webhook URL مطلوب!")
        return False
    
    twitter_username = input("👤 اسم حساب تويتر (بدون @): ").strip()
    if not twitter_username:
        print("❌ اسم المستخدم مطلوب!")
        return False
    
    # المتغيرات الاختيارية
    print("\n⚙️ الإعدادات الاختيارية (اتركها فارغة للقيم الافتراضية):")
    
    check_interval = input("⏱️  فترة الفحص بالثواني [300]: ").strip()
    if not check_interval:
        check_interval = "300"
    
    mention_everyone = input("📢 تفعيل منشن @everyone؟ (y/n) [y]: ").strip().lower()
    if mention_everyone in ['n', 'no', 'لا', 'false']:
        mention_everyone = "false"
    else:
        mention_everyone = "true"
    
    log_level = input("📊 مستوى السجلات (DEBUG/INFO/WARNING/ERROR) [INFO]: ").strip().upper()
    if not log_level:
        log_level = "INFO"
    
    # إنشاء محتوى ملف .env
    env_content = f"""# ===================================
# Twitter-Discord Bridge Bot Config  
# تم إنشاؤه تلقائياً بواسطة run_bot.py
# ===================================

# 🐦 إعدادات Twitter API (مطلوب)
TWITTER_BEARER_TOKEN={twitter_token}

# 💬 إعدادات Discord (مطلوب)
DISCORD_WEBHOOK_URL={discord_webhook}

# 👤 الحساب المراقب (مطلوب)
TWITTER_USERNAME={twitter_username}

# ⚙️ إعدادات البوت (اختيارية)
CHECK_INTERVAL={check_interval}
MENTION_EVERYONE={mention_everyone}
MAX_TWEET_LENGTH=2000
LOG_LEVEL={log_level}
DATA_DIR=data

# ===================================
# ملاحظات مهمة:
# ===================================
# - لا تشارك هذا الملف مع أحد
# - Bearer Token حساس جداً
# - يمكنك تعديل هذه القيم لاحقاً
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"\n✅ تم إنشاء ملف .env بنجاح!")
        print("🔒 تأكد من عدم مشاركة هذا الملف مع أحد")
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ في إنشاء ملف .env: {e}")
        return False

def validate_env_file():
    """التحقق من صحة ملف .env"""
    env_path = Path('.env')
    if not env_path.exists():
        return False
    
    required_vars = ['TWITTER_BEARER_TOKEN', 'DISCORD_WEBHOOK_URL', 'TWITTER_USERNAME']
    missing_vars = []
    
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for var in required_vars:
            if f"{var}=" not in content:
                missing_vars.append(var)
    
    except Exception:
        return False
    
    if missing_vars:
        print(f"❌ متغيرات مفقودة في .env: {', '.join(missing_vars)}")
        return False
    
    return True

def check_requirements():
    """فحص المتطلبات والملفات"""
    print("🔍 فحص المتطلبات...")
    
    # فحص Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 أو أحدث مطلوب")
        return False
    
    # فحص المكتبات المطلوبة
    try:
        import aiohttp
        print("✅ المتطلبات مثبتة")
    except ImportError:
        print("❌ المتطلبات غير مثبتة")
        print("💡 قم بتشغيل: pip install -r requirements.txt")
        return False
    
    # فحص الملفات المطلوبة
    required_files = ['main.py', 'config.py', 'requirements.txt']
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ ملفات مفقودة: {', '.join(missing_files)}")
        return False
    
    return True

def show_help():
    """عرض تعليمات الاستخدام"""
    print("""
🤖 Twitter-Discord Bridge Bot - دليل الاستخدام

الاستخدام:
  python run_bot.py [OPTIONS]

الخيارات:
  --help, -h          عرض هذه الرسالة
  --setup, -s         إعداد ملف .env جديد
  --check, -c         فحص الإعدادات فقط
  --validate, -v      التحقق من صحة ملف .env

أمثلة:
  python run_bot.py           # تشغيل البوت
  python run_bot.py --setup   # إعداد ملف .env جديد
  python run_bot.py --check   # فحص الإعدادات
""")

def main():
    """الدالة الرئيسية"""
    # معالجة المعاملات
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['--help', '-h']:
            show_help()
            return
        elif arg in ['--setup', '-s']:
            create_env_file()
            return
        elif arg in ['--check', '-c']:
            if validate_env_file():
                print("✅ ملف .env صالح")
            else:
                print("❌ ملف .env غير صالح أو غير موجود")
            return
        elif arg in ['--validate', '-v']:
            try:
                from config import load_config
                config = load_config()
                print("✅ جميع الإعدادات صحيحة!")
                print(f"📍 الحساب المراقب: @{config.twitter_username}")
            except Exception as e:
                print(f"❌ خطأ في الإعدادات: {e}")
            return
    
    # عرض ترحيب
    print("🤖 Twitter-Discord Bridge Bot")
    print("=" * 50)
    print("طور بواسطة: B2nd9R")
    print("GitHub: https://github.com/B2nd9R/twitter-discord-bridge-bot")
    print()
    
    # فحص المتطلبات
    if not check_requirements():
        print("\n💡 نصائح لحل المشاكل:")
        print("1. تأكد من تثبيت Python 3.8+")
        print("2. قم بتشغيل: pip install -r requirements.txt")
        print("3. تأكد من وجود جميع ملفات المشروع")
        sys.exit(1)
    
    # فحص وجود ملف .env
    if not Path('.env').exists():
        print("📝 ملف .env غير موجود")
        print("\nيمكنك إنشاؤه بإحدى الطرق التالية:")
        print("1. نسخ ملف المثال: cp .env.example .env")
        print("2. استخدام الإعداد التفاعلي")
        
        choice = input("\nهل تريد إنشاء ملف .env تفاعلياً؟ (y/n): ").strip().lower()
        if choice in ['y', 'yes', 'نعم']:
            if not create_env_file():
                print("❌ فشل في إنشاء ملف .env")
                sys.exit(1)
        else:
            print("❌ لا يمكن تشغيل البوت بدون ملف .env")
            print("💡 استخدم: python run_bot.py --setup")
            sys.exit(1)
    
    # التحقق من صحة ملف .env
    if not validate_env_file():
        print("❌ ملف .env غير صالح")
        print("💡 استخدم: python run_bot.py --validate")
        sys.exit(1)
    
    print("✅ جميع الفحوصات نجحت!")
    print("\n🚀 جاري تشغيل البوت...")
    print("💡 اضغط Ctrl+C لإيقاف البوت")
    print("📊 راقب السجلات في مجلد logs/")
    
    # استيراد وتشغيل البوت الرئيسي
    try:
        from main import main as bot_main
        asyncio.run(bot_main())
    except KeyboardInterrupt:
        print("\n\n👋 تم إيقاف البوت بواسطة المستخدم")
        print("📊 يمكنك مراجعة السجلات في logs/bot.log")
    except ImportError as e:
        print(f"\n❌ خطأ في استيراد الملفات: {e}")
        print("💡 تأكد من وجود جميع ملفات المشروع")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل البوت: {e}")
        print("📋 راجع logs/bot.log للتفاصيل")
        sys.exit(1)

if __name__ == "__main__":
    main()