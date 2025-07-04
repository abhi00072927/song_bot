from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from googleapiclient.discovery import build

# ✅ API Keys
YOUTUBE_API_KEY = "AIzaSyBFPXDGqCeKmyde6hvn300iXpr-uQUIAog"
TELEGRAM_BOT_TOKEN = "8041044127:AAGgDaHsxtRg3EBwYqvv3LFWeaGACzQ6XL8"

# ✅ YouTube API Client Setup
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# 🔍 YouTube Search Function
def search_youtube(query):
    request = youtube.search().list(
        part="snippet",
        maxResults=10,
        q=query,
        type="video",
        order="viewCount"
    )
    response = request.execute()

    results = []
    for item in response["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        results.append(f"🎵 {title}\n{url}")
    return "\n\n".join(results)

# 📩 Handle Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is not None:
        user_query = update.message.text
        await update.message.reply_text("🔍 શોધી રહ્યા છીએ... કૃપા કરીને રાહ જુઓ...")
        try:
            result = search_youtube(user_query)
            await update.message.reply_text(result)
        except Exception as e:
            await update.message.reply_text(f"❌ ભૂલ: {str(e)}")

# 🟢 Handle /start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is not None:
        await update.message.reply_text(
            "🎧 Welcome to the YouTube Song Finder Bot!\n\n"
            "✍️ લખો: `top 10 hindi sad songs`, `romantic bollywood songs`, etc.\n"
            "અને હું તમને YouTube પરથી 🎵 ટોપ ગીતો આપીશ!"
        )

# 🧠 Main Entry Point
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()
