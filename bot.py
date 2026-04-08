import os
import json
import asyncio
import aiohttp
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# ============== CONFIGURATION ==============
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 'YOUR_ADMIN_ID'))

# ============== DATA STORAGE ==============
DATA_FILE = 'bot_data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'users': {}, 'tasks': [], 'expenses': [], 'notes': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ============== KEYBOARDS ==============
def get_main_menu():
    keyboard = [
        [KeyboardButton("📝 المهام"), KeyboardButton("💰 المصاريف")],
        [KeyboardButton("📝 ملاحظاتي"), KeyboardButton("🌐 المواقع")],
        [KeyboardButton("🤖 البوتات"), KeyboardButton("⚙️ الإعدادات")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_websites_menu():
    keyboard = [
        [InlineKeyboardButton("🔍 بحث", callback_data="web_search")],
        [InlineKeyboardButton("📊 APIs", callback_data="web_apis")],
        [InlineKeyboardButton("🌍 scraping", callback_data="web_scrape")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_bots_menu():
    keyboard = [
        [InlineKeyboardButton("📤 إرسال رسالة", callback_data="bot_send")],
        [InlineKeyboardButton("📥 استقبال", callback_data="bot_receive")],
        [InlineKeyboardButton("🔗 ربط بوت", callback_data="bot_link")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============== WEBSITE HANDLERS ==============
async def fetch_url(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                return await response.text()
    except Exception as e:
        return f"Error: {str(e)}"

async def search_web(query):
    # Using DuckDuckGo API (free, no key needed)
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                data = await response.json()
                return data.get('AbstractText', 'No results found')
    except Exception as e:
        return f"Error: {str(e)}"

# ============== BOT INTERACTION HANDLERS ==============
def send_to_bot(bot_token, chat_id, text):
    """Send message to another bot or user"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {'chat_id': chat_id, 'text': text}
    try:
        response = requests.post(url, json=data, timeout=10)
        return response.json()
    except Exception as e:
        return {'ok': False, 'error': str(e)}"

def forward_to_bot(from_chat_id, message_id, bot_token, to_chat_id):
    """Forward message to another bot"""
    url = f"https://api.telegram.org/bot{bot_token}/forwardMessage"
    data = {'from_chat_id': from_chat_id, 'chat_id': to_chat_id, 'message_id': message_id}
    try:
        response = requests.post(url, json=data, timeout=10)
        return response.json()
    except Exception as e:
        return {'ok': False, 'error': str(e)}"

# ============== COMMAND HANDLERS ==============
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 أهلاً! بوت متكامل بينفذ كل شي\n\n"        "🌐 مواقع - APIs - scraping\n"        "🤖 التفاعل مع بوتات أخرى\n"        "⌨️ كيبيورد متفاعل\n"        "🖥️ كل شي على سيرفر واحد\n\n"        "اختر من القائمة:",
        reply_markup=get_main_menu()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🔧 الأوامر المتاحة:

/start - بدء البوت
/help - المساعدة
📝 المهام - إضافة/عرض المهام
💰 المصاريف - تسجيل المصاريف
🌐 المواقع - APIs و scraping
🤖 البوتات - التفاعل مع بوتات
⚙️ الإعدادات - إعدادات البوت
"""
    await update.message.reply_text(help_text)

# ============== MESSAGE HANDLERS ==============
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    
    data = load_data()
    
    # Tasks
    if text == "📝 المهام":
        tasks = data.get('tasks', [])
        if tasks:
            task_text = "📝 مهامك:\n\n" + "\n".join([f"{i+1}. {t}" for i, t in enumerate(tasks)])
        else:
            task_text = "📝 ما عندك مهام! أضف واحدة"
        await update.message.reply_text(task_text)
        await update.message.reply_text("أضف مهمة جديدة:")
        
    # Expenses
    elif text == "💰 المصاريف":
        expenses = data.get('expenses', [])
        if expenses:
            total = sum(e['amount'] for e in expenses)
            exp_text = "💰 مصاريفك:\n\n" + "\n".join([f"{e['desc']}: {e['amount']} $" for e in expenses])
            exp_text += f"\n\n💵 الإجمالي: {total} $"
        else:
            exp_text = "💰 ما عندك مصاريف! أضف واحدة"
        await update.message.reply_text(exp_text)
        await update.message.reply_text("أضف مصروف (وصف ومبلغ):")
        
    # Notes
    elif text == "📝 ملاحظاتي":
        notes = data.get('notes', [])
        if notes:
            notes_text = "📝 ملاحظاتك:\n\n" + "\n".join([f"{i+1}. {n}" for i, n in enumerate(notes)])
        else:
            notes_text = "📝 ما عندك ملاحظات! أضف واحدة"
        await update.message.reply_text(notes_text)
        await update.message.reply_text("أضف ملاحظة:")
        
    # Websites
    elif text == "🌐 المواقع":
        await update.message.reply_text(
            "🌐 اختر خدمة:\n\n"            "🔍 بحث في الإنترنت\n"            "📊 APIs\n"            "🌍 scraping\n",
            reply_markup=get_websites_menu()
        )
        
    # Bots
    elif text == "🤖 البوتات":
        await update.message.reply_text(
            "🤖 التفاعل مع البوتات:\n\n"            "📤 إرسال رسالة لبوت آخر\n"            "📥 استقبال رسائل\n"            "🔗 ربط بوت\n",
            reply_markup=get_bots_menu()
        )
        
    # Settings
    elif text == "⚙️ الإعدادات":
        await update.message.reply_text(
            "⚙️ الإعدادات:\n\n"            f"👤 معرفك: {user_id}\n"            f"🤖 توكن البوت: {'مضبوط' if BOT_TOKEN != 'YOUR_BOT_TOKEN' else 'غير مضبوط'}\n",
            reply_markup=get_main_menu()
        )
        
    # Add new task
    elif text.startswith("task:") or text.startswith("مهمة:"):
        task = text.replace("task:", "").replace("مهمة:", "").strip()
        if task:
            data.setdefault('tasks', []).append(task)
            save_data(data)
            await update.message.reply_text(f"✅ تم إضافة المهمة: {task}")
            
    # Add new expense (format: description amount)
    elif text.startswith("exp:") or text.startswith("مصرف:"):
        parts = text.replace("exp:", "").replace("مصرف:", "").strip().split()
        if len(parts) >= 2:
            desc = " ".join(parts[:-1])
            try:
                amount = float(parts[-1])
                data.setdefault('expenses', []).append({'desc': desc, 'amount': amount})
                save_data(data)
                await update.message.reply_text(f"✅ تم إضافة المصروف: {desc} - {amount} $")
            except:
                await update.message.reply_text("⚠️ خطأ في الصيغة! اكتب: وصف مبلغ")
                
    # Add new note
    elif text.startswith("note:") or text.startswith("ملاحظة:"):
        note = text.replace("note:", "").replace("ملاحظة:", "").strip()
        if note:
            data.setdefault('notes', []).append(note)
            save_data(data)
            await update.message.reply_text(f"✅ تم إضافة الملاحظة: {note}")
            
    else:
        await update.message.reply_text(
            "❓ ما فهمت! استخدم الأزرار",
            reply_markup=get_main_menu()
        )

# ============== CALLBACK HANDLERS ==============
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "back_main":
        await query.message.reply_text(
            "🔙 رجوع للقائمة الرئيسية:",
            reply_markup=get_main_menu()
        )
        
    elif query.data == "web_search":
        await query.message.reply_text("🔍 اكتب الكلمة للبحث:")
        
    elif query.data == "web_apis":
        await query.message.reply_text(
            "📊 APIs المتاحة:\n\n"            "1. Weather API\n"            "2. Crypto API\n"            "3. News API\n"            "4. Custom API\n\n"            "اكتب اسم الـ API المطلوب"
        )
        
    elif query.data == "web_scrape":
        await query.message.reply_text("🌍 اكتب الرابط للـ scraping:")
        
    elif query.data == "bot_send":
        await query.message.reply_text(
            "📤 لإرسال رسالة لبوت آخر:\n\n"            "اكتب: bot:TOKEN:CHAT_ID:MESSAGE\n"            "مثال: bot:123456:987654:مرحبا"
        )
        
    elif query.data == "bot_receive":
        await query.message.reply_text(
            "📥 لاستقبال الرسائل:\n\n"            "اضبط webhook للبوت\n"            "أو اكتب start لاستقبال التحديثات"
        )
        
    elif query.data == "bot_link":
        await query.message.reply_text(
            "🔗 لربط بوت:\n\n"            "1. احصل على token البوت\n"            "2. أضف البوت في مجموعة\n"            "3. امنح البوت صلاحيات\n\n"            "اكتب token البوت لربطه"
        )

# ============== MAIN ==============
def main():
    app = Application.builder()\
        .token(BOT_TOKEN)\
        .build()
    
    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Callbacks
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    # Set commands
    app.bot.set_my_commands([
        BotCommand("start", "بدء البوت"),
        BotCommand("help", "المساعدة"),
    ])
    
    print("🤖 البوت يعمل...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()