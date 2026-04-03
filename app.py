import os
import telebot
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import logging

# Logging (important for debugging)
logging.basicConfig(level=logging.INFO)

# Environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

if not TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN environment variable")

# Create bot and Flask app
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Webhook setup
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}{WEBHOOK_PATH}" if RENDER_EXTERNAL_URL else None

# Keyboard
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyboard.add(
    KeyboardButton("သင်တန်းစုံစမ်းရန်"),
    KeyboardButton("သင်တန်းကြေး"),
    KeyboardButton("သင်တန်းချိန်များ"),
    KeyboardButton("လိုင်စင်ဝန်ဆောင်မှု"),
    KeyboardButton("အကူအညီ"),
)

# Texts
WELCOME_TEXT = "ဟုတ်ကဲ့ မင်္ဂလာပါ။\nထွန်းတောက်ယာဉ်မောင်းအတတ်သင်တန်းကျောင်းမှ ကြိုဆိုပါတယ်။"
MENU_TEXT = "လုပ်ဆောင်လိုသောအရာကို ရွေးချယ်ပါ။"

ADDRESS_TEXT = (
    "ယာဉ်မောင်းသင်တန်းကျောင်းလိပ်စာ -\n"
    "၅၉လမ်း / ၃၃ + ၃၄ လမ်းကြား၊ မန္တလေးမြို့။\n"
    "ဖုန်း - 09791188863 / 09792288863"
)

COURSE_INFO_TEXT = "သင်တန်းက ၁၁ ရက် သင်ပေးပါတယ်။"
FEES_TEXT = "EV - 350000 Ks\nHonda Fit - 250000 Ks\nPick Up - 230000 Ks"
TIMES_TEXT = "မနက် ၆ နာရီမှ ညနေ ၆ နာရီထိ"
LICENSE_TEXT = "လိုင်စင်ဝန်ဆောင်မှုရှိပါတယ်။"
HELP_TEXT = "Menu မှ တစ်ခုခုကို ရွေးပါ။"

# =========================
# BOT HANDLERS
# =========================

@bot.message_handler(commands=["start", "help"])
def start_handler(message):
    print("START from:", message.chat.id)
    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=keyboard)
    bot.send_message(message.chat.id, MENU_TEXT, reply_markup=keyboard)

@bot.message_handler(commands=["address"])
def address_handler(message):
    print("ADDRESS requested")
    bot.send_message(message.chat.id, ADDRESS_TEXT, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "သင်တန်းစုံစမ်းရန်")
def course_info_handler(message):
    print("COURSE INFO clicked")
    bot.send_message(message.chat.id, COURSE_INFO_TEXT)

@bot.message_handler(func=lambda message: message.text == "သင်တန်းကြေး")
def fees_handler(message):
    print("FEES clicked")
    bot.send_message(message.chat.id, FEES_TEXT)

@bot.message_handler(func=lambda message: message.text == "သင်တန်းချိန်များ")
def times_handler(message):
    print("TIMES clicked")
    bot.send_message(message.chat.id, TIMES_TEXT)

@bot.message_handler(func=lambda message: message.text == "လိုင်စင်ဝန်ဆောင်မှု")
def license_handler(message):
    print("LICENSE clicked")
    bot.send_message(message.chat.id, LICENSE_TEXT)

@bot.message_handler(func=lambda message: message.text == "အကူအညီ")
def help_handler(message):
    print("HELP clicked")
    bot.send_message(message.chat.id, HELP_TEXT)

@bot.message_handler(func=lambda message: True)
def fallback_handler(message):
    print("UNKNOWN message:", message.text)
    bot.send_message(message.chat.id, "နားမလည်ပါ။ Menu ကိုရွေးပါ။", reply_markup=keyboard)

# =========================
# FLASK ROUTES
# =========================

@app.route("/", methods=["GET"])
def index():
    return "Bot is running", 200

@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    if not WEBHOOK_URL:
        return "No Render URL", 500

    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return f"Webhook set to {WEBHOOK_URL}", 200

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    try:
        json_str = request.get_data().decode("utf-8")
        print("UPDATE RECEIVED:", json_str)

        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])

        return "OK", 200
    except Exception as e:
        print("ERROR:", e)
        return "ERROR", 500

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
