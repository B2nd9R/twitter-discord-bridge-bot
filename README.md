# Twitter-Discord Bridge Bot 🤖

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![Config](https://img.shields.io/badge/Config-.env-orange.svg)

**بوت احترافي لنقل تغريدات تويتر إلى ديسكورد تلقائياً**

*طور بواسطة [B2nd9R](https://github.com/B2nd9R)*

[التثبيت السريع](#-التثبيت-السريع) • [إعداد .env](#️-إعداد-env) • [الاستخدام](#-الاستخدام) • [المساهمة](#-المساهمة)

</div>

---

## 📖 نظرة عامة

**Twitter-Discord Bridge Bot** هو بوت Python متقدم يقوم بمراقبة حسابات تويتر المحددة وإرسال التغريدات الجديدة تلقائياً إلى قنوات ديسكورد باستخدام Webhooks. البوت مصمم ليكون خفيف الوزن، موثوق، وسهل الإعداد **مع التركيز الكامل على ملف `.env`**.

### ✨ الميزات الرئيسية

- 🔄 **مراقبة تلقائية** للتغريدات الجديدة
- 🚫 **تجنب التكرار** مع نظام تتبع ذكي
- 🎨 **تنسيق جميل** مع Discord Embeds
- ⚙️ **إعدادات مرنة** عبر ملف `.env`
- 📊 **سجلات مفصلة** لمراقبة الأداء
- 🐳 **دعم Docker** للنشر السهل
- 🔒 **أمان عالي** مع حماية البيانات الحساسة
- 🛠️ **تحقق ذكي** من صحة الإعدادات

## 🛠️ المتطلبات الأساسية

| المتطلب | الوصف |
|---------|--------|
| 🐍 Python | الإصدار 3.8 أو أحدث |
| 🐦 Twitter API | حساب مطور مع Bearer Token |
| 💬 Discord Server | صلاحيات إنشاء Webhooks |
| 💾 تخزين | 50MB لتخزين البيانات |

## 🚀 التثبيت السريع

### الطريقة المفضلة: تثبيت عادي

```bash
# استنساخ المستودع
git clone https://github.com/B2nd9R/twitter-discord-bridge-bot.git
cd twitter-discord-bridge-bot

# تثبيت المتطلبات
pip install -r requirements.txt

# نسخ وتعديل ملف الإعدادات
cp .env.example .env
nano .env  # أدخل معلوماتك الحقيقية

# تشغيل البوت
python main.py
```

### الطريقة البديلة: Docker

```bash
# استنساخ المستودع
git clone https://github.com/B2nd9R/twitter-discord-bridge-bot.git
cd twitter-discord-bridge-bot

# تحضير ملف .env
cp .env.example .env
nano .env  # أدخل معلوماتك

# تشغيل بـ Docker Compose
docker-compose up -d
```

## ⚙️ إعداد `.env` (الطريقة الوحيدة)

### 📝 إنشاء ملف `.env`

البوت يعتمد **بشكل كامل** على ملف `.env` للإعدادات:

```bash
# نسخ المثال
cp .env.example .env

# تعديل الملف
nano .env  # أو أي محرر تفضله
```

### 🔧 محتوى ملف `.env`

```bash
# 🐦 إعدادات Twitter API (مطلوب)
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAMLheAAAAAAA0%2BuSeid...

# 💬 إعدادات Discord (مطلوب) 
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1234567890...

# 👤 الحساب المراقب (مطلوب)
TWITTER_USERNAME=PlayStation

# ⚙️ إعدادات إضافية (اختيارية)
CHECK_INTERVAL=300
MENTION_EVERYONE=true
LOG_LEVEL=INFO
```

## 🐦 إعداد Twitter API

<details>
<summary><strong>📋 خطوات تفصيلية للحصول على Bearer Token</strong></summary>

### 1. التسجيل كمطور
- اذهب إلى [Twitter Developer Portal](https://developer.twitter.com)
- سجل دخول بحساب تويتر
- اضغط "Sign up for free account"

### 2. إنشاء تطبيق
```
Project Name: Discord Twitter Bot  
App Name: twitter-discord-bridge
Description: Bot to forward tweets to Discord
Website URL: https://github.com/B2nd9R/twitter-discord-bridge-bot
```

### 3. الحصول على Bearer Token
- في لوحة التحكم → "Keys and Tokens"
- تحت "Bearer Token" اضغط "Generate"
- انسخ الرمز واحفظه في `.env`

### 4. أذونات API
- تأكد من أن التطبيق لديه أذونات "Read" فقط
- لا تحتاج أذونات كتابة أو DM

</details>

## 💬 إعداد Discord Webhook

<details>
<summary><strong>📋 خطوات تفصيلية لإنشاء Webhook</strong></summary>

### 1. إنشاء Webhook
- اذهب للقناة المطلوبة في ديسكورد
- اضغط على ⚙️ إعدادات القناة
- اختر "Integrations" → "Webhooks"
- اضغط "Create Webhook"

### 2. تكوين Webhook
```
Name: Twitter Bot
Avatar: (اختياري - صورة تويتر)  
Channel: #gaming-news (أو القناة المطلوبة)
```

### 3. نسخ URL
- اضغط "Copy Webhook URL" 
- الصق الرابط في ملف `.env`
- احفظ الإعدادات

⚠️ **هام**: Webhook URL حساس جداً - لا تشاركه مع أحد!

</details>

## 🎯 الاستخدام

### 🏃‍♂️ تشغيل البوت

```bash
# الطريقة الأساسية
python main.py

# مع اختبار الإعدادات أولاً
python config.py

# تشغيل مع Docker
docker-compose up -d
```

### 📊 مراقبة البوت

```bash
# عرض السجلات المباشرة
tail -f logs/bot.log

# فحص البيانات المحفوظة  
ls -la data/

# حالة Docker (إذا كنت تستخدمه)
docker logs twitter-discord-bridge --follow
```

### 🛠️ اختبار الإعدادات

```bash
# اختبار سريع للإعدادات
python -c "from config import load_config; print('✅ الإعدادات صحيحة!')"

# اختبار شامل
python config.py
```

## 🔧 متغيرات ملف `.env`

### المتغيرات المطلوبة

| المتغير | الوصف | مثال |
|---------|--------|-------|
| `TWITTER_BEARER_TOKEN` | رمز Twitter API | `AAAAAAAAAA...` |
| `DISCORD_WEBHOOK_URL` | رابط Discord Webhook | `https://discord.com/api/webhooks/...` |
| `TWITTER_USERNAME` | الحساب المراقب (بدون @) | `PlayStation` |

### المتغيرات الاختيارية

| المتغير | الوصف | القيمة الافتراضية |
|---------|--------|------------------|
| `CHECK_INTERVAL` | فترة الفحص بالثواني | `300` (5 دقائق) |
| `MENTION_EVERYONE` | تفعيل منشن @everyone | `true` |
| `MAX_TWEET_LENGTH` | الحد الأقصى لطول النص | `2000` |
| `LOG_LEVEL` | مستوى التسجيل | `INFO` |
| `DATA_DIR` | مجلد البيانات | `data` |

### 📝 نصائح لـ `.env`

```bash
# ✅ صيغة صحيحة
TWITTER_USERNAME=PlayStation
MENTION_EVERYONE=true
CHECK_INTERVAL=300

# ❌ صيغة خاطئة  
TWITTER_USERNAME = PlayStation  # مسافات حول =
TWITTER_USERNAME="PlayStation"  # علامات اقتباس غير ضرورية
```

## 🐳 النشر باستخدام Docker

### إعداد Docker Compose

البوت يأتي مع `docker-compose.yml` جاهز:

```bash
# تحضير البيئة
cp .env.example .env
nano .env  # أدخل معلوماتك

# بناء وتشغيل
docker-compose up -d

# مراقبة السجلات
docker-compose logs -f

# إيقاف البوت
docker-compose down
```

### ملف `docker-compose.yml`

```yaml
version: '3.8'
services:
  twitter-discord-bot:
    build: .
    container_name: twitter-discord-bridge
    restart: unless-stopped
    env_file: .env
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
```

## 🔧 التشغيل كخدمة (Linux)

### إنشاء خدمة systemd

```bash
# إنشاء ملف الخدمة
sudo nano /etc/systemd/system/twitter-discord-bot.service
```

```ini
[Unit]
Description=Twitter Discord Bridge Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/twitter-discord-bridge-bot
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10
EnvironmentFile=/path/to/twitter-discord-bridge-bot/.env

[Install]
WantedBy=multi-user.target
```

```bash
# تفعيل وبدء الخدمة
sudo systemctl daemon-reload
sudo systemctl enable twitter-discord-bot.service
sudo systemctl start twitter-discord-bot.service

# مراقبة الحالة
sudo systemctl status twitter-discord-bot.service
```

## 📊 المراقبة والصيانة

### 📁 هيكل الملفات

```
twitter-discord-bridge-bot/
├── 📄 main.py              # البوت الرئيسي
├── 🔧 config.py            # إدارة الإعدادات
├── ⚙️ .env                 # ملف الإعدادات (تُنشئه بنفسك)
├── 📋 .env.example         # مثال الإعدادات
├── 📦 requirements.txt     # المتطلبات
├── 🐳 docker-compose.yml   # إعداد Docker
├── 🗂️ data/                # بيانات البوت
│   └── sent_tweets.json   # تتبع التغريدات
├── 📊 logs/                # سجلات البوت  
│   └── bot.log           # السجل الرئيسي
└── 📚 README.md           # هذا الملف
```

### 📋 فحص الحالة

```bash
# حالة البوت العامة
python config.py

# السجلات الحديثة
tail -20 logs/bot.log

# التغريدات المرسلة
cat data/sent_tweets.json | jq .

# استخدام المساحة
du -sh data/ logs/
```

## 🛠️ استكشاف الأخطاء

### مشاكل شائعة وحلولها

| المشكلة | السبب المحتمل | الحل |
|---------|---------------|------|
| `ملف .env غير موجود` | لم تنسخ .env.example | `cp .env.example .env` |
| `خطأ في Twitter API` | Bearer Token خاطئ | تحقق من الرمز في .env |
| `خطأ في Discord Webhook` | URL خاطئ أو منتهي الصلاحية | أنشئ webhook جديد |
| `البوت لا يرسل تغريدات` | الحساب لا ينشر تغريدات | تحقق من النشاط أو جرب حساب آخر |
| `Rate Limit Exceeded` | كثرة الطلبات | زيادة CHECK_INTERVAL في .env |

### 🔍 التشخيص المتقدم

```bash
# اختبار شامل للإعدادات
python config.py

# فحص الاتصال بـ Twitter
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.twitter.com/2/users/by/username/PlayStation"

# فحص Discord Webhook
curl -X POST "YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"content":"اختبار البوت"}'
```

### 📝 السجلات المفصلة

لتفعيل السجلات المفصلة، عدل `.env`:

```bash
LOG_LEVEL=DEBUG
```

## 🔒 الأمان والخصوصية

### 🛡️ أفضل الممارسات

- ✅ **استخدم ملف `.env`** فقط للإعدادات
- ✅ **أضف `.env` لـ .gitignore** (موجود بالفعل)
- ✅ **لا تشارك Bearer Token** مع أحد
- ✅ **راجع Webhook URL** بانتظام
- ✅ **قم بعمل backup** لمجلد `data/`
- ✅ **راقب استخدام API** لتجنب تجاوز الحدود

### 🔐 حماية الملفات

```bash
# حماية ملف .env
chmod 600 .env

# حماية مجلد البيانات
chmod 750 data/

# فحص الأذونات
ls -la .env data/
```

### 🚨 علامات تحذيرية

البوت سيحذرك عند:
- Bearer Token بتنسيق مشبوه
- فترة فحص أقل من دقيقة
- فترة فحص أكثر من ساعة
- Webhook URL غير صحيح

## 💡 نصائح للاستخدام الأمثل

### 🎯 اختيار الحسابات

**حسابات مقترحة للمراقبة:**

```bash
# الألعاب والتقنية
TWITTER_USERNAME=PlayStation     # أخبار PlayStation
TWITTER_USERNAME=Xbox           # أخبار Xbox  
TWITTER_USERNAME=Steam          # عروض وألعاب Steam
TWITTER_USERNAME=elonmusk       # تحديثات إيلون ماسك

# الأخبار
TWITTER_USERNAME=BBCBreaking    # أخبار عاجلة
TWITTER_USERNAME=CNN            # أخبار CNN
TWITTER_USERNAME=Reuters        # أخبار رويترز

# الرياضة  
TWITTER_USERNAME=FIFAcom        # أخبار FIFA
TWITTER_USERNAME=ChampionsLeague # دوري الأبطال
```

### ⚡ تحسين الأداء

```bash
# للحسابات النشطة (تغريدات كثيرة)
CHECK_INTERVAL=180  # 3 دقائق

# للحسابات العادية
CHECK_INTERVAL=300  # 5 دقائق

# للحسابات قليلة النشاط  
CHECK_INTERVAL=600  # 10 دقائق
```

### 📱 تخصيص الرسائل

```bash
# إيقاف منشن الكل للحسابات كثيرة النشاط
MENTION_EVERYONE=false

# تقليل طول النص للتغريدات الطويلة
MAX_TWEET_LENGTH=1000
```

## 🚀 التطوير والمساهمة

### 🏗️ هيكل الكود

البوت مقسم لملفات منطقية:

- **`config.py`**: إدارة شاملة للإعدادات من `.env`
- **`main.py`**: البوت الرئيسي مع جميع الوظائف  
- **Classes**: كل وظيفة في class منفصل ومنظم

### 🤝 المساهمة في المشروع

1. **Fork المستودع** على GitHub
2. **إنشاء branch جديد**: `git checkout -b feature/amazing-feature`
3. **تعديل الكود** وإضافة الميزة
4. **اختبار التغييرات**: `python config.py && python main.py`
5. **Commit التغييرات**: `git commit -m 'Add amazing feature'`
6. **Push للـ branch**: `git push origin feature/amazing-feature`
7. **إنشاء Pull Request**

### 🐛 الإبلاغ عن الأخطاء

عند مواجهة مشاكل، أنشئ [issue جديد](https://github.com/B2nd9R/twitter-discord-bridge-bot/issues) مع:

```
**وصف المشكلة:**
وصف واضح للمشكلة

**خطوات إعادة الإنتاج:**
1. افعل هذا...
2. ثم هذا...
3. النتيجة...

**السلوك المتوقع:**
ما الذي توقعته أن يحدث

**البيئة:**
- نظام التشغيل: Windows 10 / Ubuntu 20.04 / macOS
- إصدار Python: 3.9.7  
- هل تستخدم Docker؟ نعم/لا

**سجل الأخطاء:**
```لصق سجل الأخطاء هنا```
```

## ⭐ الميزات المستقبلية

- [ ] **دعم عدة حسابات** في ملف .env واحد
- [ ] **فلترة الكلمات المفتاحية** لتغريدات محددة  
- [ ] **عدة قنوات ديسكورد** لحساب واحد
- [ ] **واجهة ويب** لإدارة الإعدادات
- [ ] **إحصائيات مفصلة** ولوحة مراقبة
- [ ] **دعم Twitter Spaces** والبث المباشر
- [ ] **تنبيهات Slack/Telegram** بدلاً من ديسكورد
- [ ] **API خاصة** للتحكم عن بُعد

## 📞 الدعم والتواصل

- 🐛 **الأخطاء والمشاكل**: [GitHub Issues](https://github.com/B2nd9R/twitter-discord-bridge-bot/issues)
- 💡 **اقتراحات ميزات**: [GitHub Discussions](https://github.com/B2nd9R/twitter-discord-bridge-bot/discussions)  
- 📧 **التواصل المباشر**: إنشاء Issue مع تاج `@B2nd9R`
- 👨‍💻 **المطور**: [B2nd9R](https://github.com/B2nd9R)

## 📝 الترخيص

هذا المشروع مرخص تحت **MIT License** - راجع ملف [LICENSE](LICENSE) للتفاصيل.

### ملخص الترخيص:
- ✅ **استخدام تجاري** مسموح
- ✅ **تعديل الكود** مسموح  
- ✅ **توزيع الكود** مسموح
- ✅ **استخدام خاص** مسموح
- ⚠️ **بدون ضمان** - استخدم على مسؤوليتك

---

<div align="center">

**🌟 إذا أعجبك المشروع، لا تنس إعطاءه نجمة! 🌟**

<br>

![GitHub stars](https://img.shields.io/github/stars/B2nd9R/twitter-discord-bridge-bot?style=social)
![GitHub forks](https://img.shields.io/github/forks/B2nd9R/twitter-discord-bridge-bot?style=social)

<br>

صُنع بـ ❤️ و ☕ بواسطة [B2nd9R](https://github.com/B2nd9R)

*"نقل التغريدات أصبح أسهل من أي وقت مضى!"*

</div>

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