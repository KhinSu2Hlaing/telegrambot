import os
import telebot
from flask import Flask, request, abort
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("8329978625:AAFqNQxK_BEra7zuguvjTH6O_7wj28jsjsA")
RENDER_EXTERNAL_URL = os.getenv("https://telegram-driving-school-bot.onrender.com")

if not TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN environment variable")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

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
WELCOME_TEXT = (
    "ဟုတ်ကဲ့ မင်္ဂလာပါ။\n"
    "ထွန်းတောက်ယာဉ်မောင်းအတတ်သင်တန်းကျောင်းမှ ကြိုဆိုပါတယ်။"
)

MENU_TEXT = "လုပ်ဆောင်လိုသောအရာကို ရွေးချယ်ပါ။"

ADDRESS_TEXT = (
    "ယာဉ်မောင်းသင်တန်းကျောင်းလိပ်စာ -\n"
    "၅၉လမ်း / ၃၃ + ၃၄ လမ်းကြား၊ ယာဉ်ပျံဘူတာတောင်ဘက်၊ "
    "ချမ်းအေးသာစံမြို့နယ်၊ မန္တလေးမြို့။\n\n"
    "လူကြီးမင်း သိရှိလိုသောအကြောင်းအရာများအား "
    "အောက်ပါဖုန်းနံပါတ်များကို ဆက်သွယ်၍ မေးမြန်းနိုင်ပါတယ်။\n"
    "09791188863\n"
    "09792288863\n"
    "09256388863"
)

COURSE_INFO_TEXT = (
    "ကျွန်တော်တို့သင်တန်းကျောင်းက ၁၁ ရက်သင်ပေးပါတယ်။\n\n"
    "၁၁ ရက်ထဲမှာ\n"
    "- ပထမဆုံးရက်နဲ့ နောက်ဆုံးရက်က သင်တန်းဖွင့် / ဆင်း ပုံစံမျိုး သင်ကြားပေးပါတယ်။\n"
    "- ၅ ရက်က ကျောင်းအတွင်း စာတွေ့ / လက်တွေ့ သင်ကြားရေးဖြစ်ပါတယ်။\n"
    "- ကျန် ၄ ရက်ကတော့ ပြင်ပမောင်း သင်ကြားရေးဖြစ်ပါတယ်။"
)

FEES_TEXT = (
    "သင်တန်းကြေးများမှာ -\n"
    "EV - 350000 Ks\n"
    "Honda Fit - 250000 Ks\n"
    "Pick Up - 230000 Ks"
)

TIMES_TEXT = (
    "သင်တန်းချိန်တွေကတော့ မနက် ၆ နာရီကနေ ညနေ ၆ နာရီထိရှိပါတယ်။\n"
    "တစ်ချိန်လျှင် -\n"
    "စာတွေ့ - နာရီဝက်\n"
    "လက်တွေ့ - ၁ နာရီ\n"
    "သင်ကြားပေးပါတယ်။"
)

LICENSE_TEXT = (
    "လိုင်စင်ဝန်ဆောင်မှုကို သင်တန်းသူ / သားများသာ ကူညီဆောင်ရွက်ပေးပါသည်။\n\n"
    "လိုင်စင်ကြေး - 130000 Ks\n\n"
    "(ခ) လိုင်စင်ဖြေလိုအပ်ချက်များ -\n"
    "- မှတ်ပုံတင်မိတ္တူ (၁) စုံ\n"
    "- လိုင်စင်မူရင်း / မိတ္တူ (၁) စုံ\n"
    "- လိုင်စင်ဓာတ်ပုံ (၁) ပုံ\n\n"
    "ယူဆောင်လာပေးပါရန်။"
)

HELP_TEXT = (
    "အကူအညီရယူလိုပါက menu မှ အောက်ပါအရာများကို ရွေးချယ်နိုင်ပါတယ် -\n"
    "• သင်တန်းစုံစမ်းရန်\n"
    "• သင်တန်းကြေး\n"
    "• သင်တန်းချိန်များ\n"
    "• လိုင်စင်ဝန်ဆောင်မှု\n"
    "• /address"
)


@bot.message_handler(commands=["start", "help"])
def start_handler(message):
    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=keyboard)
    bot.send_message(message.chat.id, MENU_TEXT, reply_markup=keyboard)


@bot.message_handler(commands=["address"])
def address_handler(message):
    bot.send_message(message.chat.id, ADDRESS_TEXT, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.content_type == "text" and message.text == "သင်တန်းစုံစမ်းရန်")
def course_info_handler(message):
    bot.send_message(message.chat.id, COURSE_INFO_TEXT, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.content_type == "text" and message.text == "သင်တန်းကြေး")
def fees_handler(message):
    bot.send_message(message.chat.id, FEES_TEXT, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.content_type == "text" and message.text == "သင်တန်းချိန်များ")
def times_handler(message):
    bot.send_message(message.chat.id, TIMES_TEXT, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.content_type == "text" and message.text == "လိုင်စင်ဝန်ဆောင်မှု")
def license_handler(message):
    bot.send_message(message.chat.id, LICENSE_TEXT, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.content_type == "text" and message.text == "အကူအညီ")
def help_handler(message):
    bot.send_message(message.chat.id, HELP_TEXT, reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def fallback_handler(message):
    bot.send_message(
        message.chat.id,
        "တောင်းပန်ပါတယ်။ နားမလည်သေးပါ။\nကျေးဇူးပြု၍ menu မှ ရွေးချယ်ပါ။",
        reply_markup=keyboard
    )


@app.route("/", methods=["GET"])
def index():
    return "Telegram bot is running.", 200


@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    if not WEBHOOK_URL:
        return "RENDER_EXTERNAL_URL is not available.", 500

    bot.remove_webhook()
    success = bot.set_webhook(url=WEBHOOK_URL)

    if success:
        return f"Webhook set to: {WEBHOOK_URL}", 200
    return "Failed to set webhook.", 500


@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_str = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "OK", 200

    abort(403)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
