import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Logging setup taaki errors ya status terminal par dikhe
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ek keyboard button banate hain jo user ki live/current location share karne ki request karega
    keyboard = [
        [KeyboardButton("📍 Share Location", request_location=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "👋 Hello! Main aapka Location & Camera/Photo Bot hoon.\n\n"
        "1. Niche diye gaye button se apni **Location** share karein.\n"
        "2. Ya direct koi bhi **Photo / Camera se click ki gayi image** bhejein.",
        reply_markup=reply_markup
    )

# Location handle karne ka function
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_location = update.message.location
    lat = user_location.latitude
    lon = user_location.longitude
    
    # Google Maps ka direct link generate karna
    maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    
    response_text = (
        f"📍 **Location Recieved!**\n"
        f"• Latitude: `{lat}`\n"
        f"• Longitude: `{lon}`\n\n"
        f"🗺️ [Google Maps Link]({maps_link})"
    )
    
    await update.message.reply_text(response_text, parse_mode="Markdown")

# Photo / Camera image handle karne ka function
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # User ne jo photo bheji hai usme se sabse high resolution wali photo ka file_id lete hain
    photo_file = update.message.photo[-1]
    file_id = photo_file.file_id
    
    await update.message.reply_text(
        f"📸 **Photo Received Successfully!**\n"
        f"File ID: `{file_id}`\n\n"
        f"Aapne bohot acchi photo bheji hai!",
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    # YAHAN APNA BOT TOKEN DAALEIN (BotFather se mila hua token)
    BOT_TOKEN = "8822956129:AAEizfD0a5dpCei2y8r30TDgZ9RvlUc2uZ4"
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers register karna
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 Bot is up and running...")
    # Bot ko start karne ke liye polling shuru karein
    app.run_polling()
