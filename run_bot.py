#!/usr/bin/env python3
"""
سكريبت تشغيل بوت نقل تغريدات تويتر إلى ديسكورد
مع إعداد تفاعلي للمستخدمين الجدد
"""

import asyncio
import json
import os
import sys
from pathlib import Path


def create_config_file():
    """إنشاء ملف إعدادات تفاعلي"""
    print("🔧 إعداد البوت للمرة الأولى")
    print("=" * 50)

    print("\n📱 إعدادات تويتر:")
    twitter_token = input("أدخل Twitter Bearer Token: ").strip()
    twitter_username = input("أدخل اسم حساب تويتر (بدون @): ").strip()

    print("\n💬 إعدادات ديسكورد:")
    discord_webhook = input("أدخل Discord Webhook URL: ").strip()

    print("\n⚙️ إعدادات إضافية:")
    check_interval = input("فترة فحص التغريدات بالثواني (افتراضي: 300): ").strip()
    if not check_interval:
        check_interval = "300"

    mention_everyone = input("تفعيل منشن @everyone؟ (y/n) [افتراضي: y]: ").strip().lower()
    if mention_everyone in ['n', 'no', 'لا']:
        mention_everyone = False
    else:
        mention_everyone = True

    config = {
        "twitter_bearer_token": twitter_token,
        "discord_webhook_url": discord_webhook,
        "twitter_username": twitter_username,
        "check_interval": int(check_interval),
        "mention_everyone": mention_everyone
    }

    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print("\n✅ تم حفظ الإعدادات في config.json")
    return True


def check_requirements():
    """فحص المتطلبات والملفات"""
    try:
        import aiohttp
        print("✅ المتطلبات مثبتة")
        return True
    except ImportError:
        print("❌ المتطلبات غير مثبتة")
        print("قم بتشغيل: pip install -r requirements.txt")
        return False


def main():
    """الدالة الرئيسية"""
    print("🤖 بوت نقل تغريدات تويتر إلى ديسكورد")
    print("=" * 50)

    # فحص المتطلبات
    if not check_requirements():
        sys.exit(1)

    # فحص وجود ملف الإعدادات
    if not Path('config.json').exists():
        print("📝 ملف الإعدادات غير موجود")
        if input("هل تريد إنشاء ملف إعدادات جديد؟ (y/n): ").strip().lower() in ['y', 'yes', 'نعم']:
            if not create_config_file():
                sys.exit(1)
        else:
            print("❌ لا يمكن تشغيل البوت بدون ملف إعدادات")
            sys.exit(1)

    print("\n🚀 جاري تشغيل البوت...")
    print("اضغط Ctrl+C لإيقاف البوت")

    # استيراد وتشغيل البوت الرئيسي
    try:
        from main import main as bot_main
        asyncio.run(bot_main())
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف البوت بنجاح")
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل البوت: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()