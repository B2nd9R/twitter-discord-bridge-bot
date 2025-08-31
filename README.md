# Twitter-Discord Bridge Bot 🤖

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

**بوت احترافي لنقل تغريدات تويتر إلى ديسكورد تلقائياً**

*طور بواسطة [B2nd9R](https://github.com/B2nd9R)*

[التثبيت](#-التثبيت) • [الإعداد](#️-الإعداد) • [الاستخدام](#-الاستخدام) • [المساهمة](#-المساهمة)

</div>

---

## 📖 نظرة عامة

**Twitter-Discord Bridge Bot** هو بوت Python متقدم يقوم بمراقبة حسابات تويتر المحددة وإرسال التغريدات الجديدة تلقائياً إلى قنوات ديسكورد باستخدام Webhooks. البوت مصمم ليكون خفيف الوزن، موثوق، وسهل الإعداد.

### ✨ الميزات الرئيسية

- 🔄 **مراقبة تلقائية** للتغريدات الجديدة
- 🚫 **تجنب التكرار** مع نظام تتبع ذكي
- 🎨 **تنسيق جميل** مع Discord Embeds
- ⚙️ **إعدادات مرنة** قابلة للتخصيص
- 📊 **سجلات مفصلة** لمراقبة الأداء
- 🐳 **دعم Docker** للنشر السهل
- 🔒 **أمان عالي** مع دعم متغيرات البيئة

## 🛠️ المتطلبات الأساسية

| المتطلب | الوصف |
|---------|--------|
| 🐍 Python | الإصدار 3.8 أو أحدث |
| 🐦 Twitter API | حساب مطور مع Bearer Token |
| 💬 Discord Server | صلاحيات إنشاء Webhooks |
| 💾 تخزين | 50MB لتخزين البيانات |

## 🚀 التثبيت السريع

### الطريقة الأولى: تثبيت عادي

```bash
# استنساخ المستودع
git clone https://github.com/B2nd9R/twitter-discord-bridge-bot.git
cd twitter-discord-bridge-bot

# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل الإعداد التفاعلي
python run_bot.py
```

### الطريقة الثانية: Docker (مُفضل)

```bash
# استنساخ المستودع
git clone https://github.com/B2nd9R/twitter-discord-bridge-bot.git
cd twitter-discord-bridge-bot

# بناء الصورة
docker build -t twitter-discord-bot .

# تشغيل البوت
docker run -d --name twitter-bot \
  -e TWITTER_BEARER_TOKEN="your_token" \
  -e DISCORD_WEBHOOK_URL="your_webhook" \
  -e TWITTER_USERNAME="target_account" \
  twitter-discord-bot
```

## ⚙️ الإعداد التفصيلي

### 🐦 إعداد Twitter API

<details>
<summary><strong>اضغط لعرض خطوات الإعداد التفصيلية</strong></summary>

1. **التسجيل كمطور:**
   - اذهب إلى [Twitter Developer Portal](https://developer.twitter.com)
   - سجل دخول بحساب تويتر
   - قدم طلب للحصول على حساب مطور

2. **إنشاء تطبيق:**
   ```
   Project Name: Discord Twitter Bot
   App Name: twitter-discord-bridge
   Description: Bot to forward tweets to Discord
   ```

3. **الحصول على Bearer Token:**
   - في لوحة التحكم → "Keys and Tokens"
   - انسخ "Bearer Token"
   - احتفظ به في مكان آمن

</details>

### 💬 إعداد Discord Webhook

<details>
<summary><strong>اضغط لعرض خطوات الإعداد التفصيلية</strong></summary>

1. **إنشاء Webhook:**
   - اذهب للقناة المطلوبة
   - إعدادات القناة → "Integrations"
   - "Create Webhook"

2. **تكوين Webhook:**
   ```
   Name: Twitter Gaming News
   Avatar: صورة مناسبة (اختياري)
   Channel: #gaming-news
   ```

3. **نسخ URL:**
   - انسخ "Webhook URL"
   - احتفظ به في مكان آمن

</details>

## 🎯 الاستخدام

### تشغيل البوت

#### الطريقة الأولى: تشغيل مباشر
```bash
python run_bot.py
```

#### الطريقة الثانية: تشغيل البوت فقط
```bash
python main.py
```

#### الطريقة الثالثة: Docker
```bash
docker-compose up -d
```

### 📊 مراقبة البوت

```bash
# عرض السجلات المباشرة
tail -f bot.log

# فحص حالة البوت (Docker)
docker logs twitter-bot --follow
```

## 🔧 التكوين المتقدم

### متغيرات البيئة

| المتغير | الوصف | القيمة الافتراضية |
|---------|--------|------------------|
| `TWITTER_BEARER_TOKEN` | رمز تويتر المميز | **مطلوب** |
| `DISCORD_WEBHOOK_URL` | رابط Discord Webhook | **مطلوب** |
| `TWITTER_USERNAME` | اسم حساب تويتر | **مطلوب** |
| `CHECK_INTERVAL` | فترة الفحص بالثواني | `300` |
| `MENTION_EVERYONE` | تفعيل منشن الكل | `true` |

### ملف الإعدادات (config.json)

```json
{
  "twitter_bearer_token": "YOUR_TOKEN_HERE",
  "discord_webhook_url": "YOUR_WEBHOOK_URL_HERE",
  "twitter_username": "gaming_news_account",
  "check_interval": 300,
  "mention_everyone": true
}
```

## 🐳 النشر باستخدام Docker

### إنشاء docker-compose.yml

```yaml
version: '3.8'
services:
  twitter-bot:
    build: .
    container_name: twitter-discord-bot
    restart: unless-stopped
    environment:
      - TWITTER_BEARER_TOKEN=${TWITTER_BEARER_TOKEN}
      - DISCORD_WEBHOOK_URL=${DISCORD_WEBHOOK_URL}
      - TWITTER_USERNAME=${TWITTER_USERNAME}
      - CHECK_INTERVAL=${CHECK_INTERVAL:-300}
      - MENTION_EVERYONE=${MENTION_EVERYONE:-true}
    volumes:
      - ./data:/app/data
```

### ملف .env للإنتاج

```bash
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
DISCORD_WEBHOOK_URL=your_discord_webhook_url_here
TWITTER_USERNAME=target_twitter_account
CHECK_INTERVAL=300
MENTION_EVERYONE=true
```

## 🔧 التشغيل كخدمة (Linux)

### إنشاء خدمة systemd

1. **إنشاء ملف الخدمة:**
   ```bash
   sudo nano /etc/systemd/system/twitter-discord-bot.service
   ```

2. **محتوى ملف الخدمة:**
   ```ini
   [Unit]
   Description=Twitter Discord Bridge Bot
   After=network.target
   Wants=network.target

   [Service]
   Type=simple
   User=your_username
   WorkingDirectory=/path/to/twitter-discord-bridge-bot
   ExecStart=/usr/bin/python3 main.py
   Restart=always
   RestartSec=10
   Environment=PYTHONUNBUFFERED=1

   [Install]
   WantedBy=multi-user.target
   ```

3. **تفعيل وبدء الخدمة:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable twitter-discord-bot.service
   sudo systemctl start twitter-discord-bot.service
   ```

## 📊 المراقبة والصيانة

### فحص السجلات

```bash
# سجل ملف البوت
tail -f bot.log

# سجل الخدمة
sudo journalctl -u twitter-discord-bot.service -f

# سجل Docker
docker logs twitter-discord-bot --follow
```

### فحص حالة البوت

```bash
# حالة الخدمة
sudo systemctl status twitter-discord-bot.service

# حالة Docker
docker ps | grep twitter-discord-bot
```

## 🛠️ استكشاف الأخطاء

### مشاكل شائعة وحلولها

| المشكلة | السبب المحتمل | الحل |
|---------|---------------|------|
| `خطأ في Twitter API` | Bearer Token خاطئ | تحقق من صحة الرمز المميز |
| `خطأ في Discord Webhook` | رابط Webhook خاطئ | تحقق من صحة الرابط |
| `البوت لا يرسل تغريدات` | لا توجد تغريدات جديدة | تحقق من `sent_tweets.json` |
| `Rate Limit Exceeded` | كثرة الطلبات | زيادة `check_interval` |

### سجلات مفصلة

البوت يسجل جميع العمليات في:
- `bot.log` - سجل عام
- `sent_tweets.json` - تتبع التغريدات المرسلة

## 🔒 الأمان والخصوصية

### 🛡️ أفضل الممارسات الأمنية

- ✅ **استخدم متغيرات البيئة** للمعلومات الحساسة
- ✅ **لا تشارك** Bearer Token أو Webhook URL
- ✅ **قم بعمل backup منتظم** لملف `sent_tweets.json`
- ✅ **راقب استخدام API** لتجنب تجاوز الحدود
- ✅ **استخدم HTTPS** دائماً للاتصالات

### 🔐 حماية المعلومات الحساسة

```bash
# إنشاء ملف .env
echo "TWITTER_BEARER_TOKEN=your_token" >> .env
echo "DISCORD_WEBHOOK_URL=your_webhook" >> .env
echo "TWITTER_USERNAME=target_account" >> .env

# حماية الملف
chmod 600 .env
```

## 🚀 التطوير والمساهمة

### هيكل المشروع

```
twitter-discord-bridge-bot/
├── 📄 main.py              # البوت الرئيسي
├── 🔧 run_bot.py           # سكريبت التشغيل التفاعلي
├── ⚙️ config.json          # ملف الإعدادات
├── 📦 requirements.txt     # المتطلبات
├── 🐳 Dockerfile          # إعداد Docker
├── 📋 docker-compose.yml   # إعداد Docker Compose
├── 📚 README.md           # هذا الملف
├── 📊 bot.log             # سجل البوت (يُنشأ تلقائياً)
└── 💾 sent_tweets.json    # تتبع التغريدات (يُنشأ تلقائياً)
```

### 🤝 المساهمة في المشروع

1. **Fork المستودع**
2. **إنشاء branch جديد** (`git checkout -b feature/amazing-feature`)
3. **Commit التغييرات** (`git commit -m 'Add amazing feature'`)
4. **Push للـ branch** (`git push origin feature/amazing-feature`)
5. **إنشاء Pull Request**

### 🐛 الإبلاغ عن الأخطاء

إذا واجهت أي مشاكل، يرجى [إنشاء issue جديد](https://github.com/B2nd9R/twitter-discord-bridge-bot/issues) مع:
- وصف المشكلة
- خطوات إعادة الإنتاج
- سجل الأخطاء (إن وجد)
- نظام التشغيل وإصدار Python

## ⭐ الميزات المستقبلية

- [ ] دعم عدة حسابات تويتر
- [ ] فلترة التغريدات حسب الكلمات المفتاحية
- [ ] إرسال لعدة قنوات ديسكورد
- [ ] واجهة ويب للإدارة
- [ ] دعم Twitter Spaces
- [ ] إحصائيات مفصلة

## 📞 الدعم والتواصل

- 🐛 **الأخطاء والمشاكل**: [GitHub Issues](https://github.com/B2nd9R/twitter-discord-bridge-bot/issues)
- 💡 **اقتراحات ميزات**: [GitHub Discussions](https://github.com/B2nd9R/twitter-discord-bridge-bot/discussions)
- 👨‍💻 **المطور**: [B2nd9R](https://github.com/B2nd9R)

## 📝 الترخيص

هذا المشروع مرخص تحت [MIT License](LICENSE).

---

<div align="center">

**إذا أعجبك المشروع، لا تنس إعطاءه ⭐**

صنع بـ ❤️ بواسطة [B2nd9R](https://github.com/B2nd9R)

</div>