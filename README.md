# 🤖 Universal Telegram Bot

بوت تلغرام متكامل يشغل:
- 🌐 مواقع و APIs و scraping
- 🤖 التفاعل مع بوتات أخرى
- ⌨️ كيبيورد متفاعل
- 🖥️ كل شي على نفس السيرفر

---

## 🚀 التثبيت

```bash
# استنساخ المشروع
git clone https://github.com/mrabt3475-cpu/universal-telegram-bot.git
cd universal-telegram-bot

# تثبيت المتطلبات
pip install -r requirements.txt
```

## ⚙️ الإعداد

1. **أنشئ بوت من @BotFather** واحصل على التوكن

2. **اضبط المتغيرات البيئية:**

```bash
export BOT_TOKEN="توكن_البوت_هنا"
export ADMIN_ID="معرف_الأدمن"
```

أو أنشئ ملف `.env`:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_id_here
```

## ▶️ التشغيل

```bash
python bot.py
```

---

## 📋 الميزات

### 🌐 المواقع
- 🔍 بحث في الإنترنت
- 📊 APIs (طقس، عملات، أخبار)
- 🌍 scraping

### 🤖 البوتات
- 📤 إرسال رسائل لبوتات أخرى
- 📥 استقبال التحديثات
- 🔗 ربط بوتات متعددة

### ⌨️ الكيبيورد
- Reply Keyboard
- Inline Keyboard
- أزرار تفاعلية

### 💾 البيانات
- 📝 إدارة المهام
- 💰 مسجل المصاريف
- 📝 ملاحظات

---

## 🔧 أوامر البوت

| الأمر | الوظيفة |
|-------|---------|
| /start | بدء البوت |
| /help | المساعدة |

---

## 📝 صيغ الأوامر

```
# إضافة مهمة
task:مهمة جديدة
أو
مهمة:مهمة جديدة

# إضافة مصروف
exp:وصف المبلغ
أو
مصرف:وصف المبلغ

# إضافة ملاحظة
note:ملاحظتي
أو
ملاحظة:ملاحظتي

# إرسال رسالة لبوت آخر
bot:TOKEN:CHAT_ID:MESSAGE
```

---

## 🌐 استضافة

### Railway
1. ارفع الكود على GitHub
2. اذهب إلى railway.app
3. أنشئ مشروع جديد من GitHub
4. أضف المتغيرات البيئية
5. انشر!

### Render
1. ارفع الكود على GitHub
2. اذهب إلى render.com
3. أنشئ Web Service
4. أضف المتغيرات
5. انشر!

### VPS
```bash
# تشغيل البوت
python bot.py

# تشغيل في الخلفية
nohup python bot.py &
```

---

## 📧 تواصل مع المطور

حسابي على تليجرام: @Mohammad4648