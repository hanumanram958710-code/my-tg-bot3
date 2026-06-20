import os
import telebot
from flask import Flask, request

# Bot Token aur QR Link
BOT_TOKEN = "8867254832:AAFmOp3sIuc5RPee9I6hHY80zTW9n7Gatpk"
QR_IMAGE_URL = "https://i.ibb.co/23mn37Hx/image.jpg"


bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)

# Webhook URL setup (Render khud apni URL provide karta hai)
RENDER_APP_URL = os.environ.get('RENDER_EXTERNAL_URL') 

@bot.message_handler(commands=['start', 'buy', 'price', 'payment'])
def send_price_list(message):
    price_text = (
        "👋 **Welcome to Our Shop!**\n\n"
        "💰 **Hamari Price List Niche Hai:**\n\n"
        "⏱ 3 DAY ➔ 50 RS ✅\n"
        "⏱ 7 DAY ➔ 100 RS ✅\n"
        "⏱ 14 DAY ➔ 200 RS ✅\n"
        "⏱ 30 DAY ➔ 300 RS ✅\n"
        "👑 FULL SEASON ➔ 400 RS ✅\n\n"
        "👉 **Kaise Kharidein?** Niche diye gaye **Pay Now** button par click karke QR code lein aur payment karein."
    )
    markup = telebot.types.InlineKeyboardMarkup()
    pay_button = telebot.types.InlineKeyboardButton(text="💳 Pay Now (Get QR Code)", callback_data="send_qr")
    markup.add(pay_button)
    bot.send_message(message.chat.id, price_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "send_qr")
def callback_query(call):
    welcome_text = (
        "💳 **Payment QR Code**\n\n"
        "1. Is QR code ko scan karke payment karein.\n"
        "2. Payment hone ke baad **Screenshot** aur apna **Name/Username** isi chat me send karein.\n"
        "3. Hum jald se jald aapka order deliver kar denge! 🙏"
    )
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_document(call.message.chat.id, QR_IMAGE_URL, caption=welcome_text, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(call.message.chat.id, "QR Code load nahi ho paa raha hai.")

# Flask routes Render ke liye
@server.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_APP_URL}/{BOT_TOKEN}")
    return "Bot is Active!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)
