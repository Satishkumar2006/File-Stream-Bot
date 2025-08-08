import os
from flask import Flask, send_file
from pyrogram import Client, filters

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

app = Flask(__name__)
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

UPLOAD_FOLDER = "downloads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

files = {}

@bot.on_message(filters.document | filters.video)
async def save_file(client, message):
    file_path = await message.download(file_name=os.path.join(UPLOAD_FOLDER, message.document.file_name))
    file_id = str(message.message_id)
    files[file_id] = file_path

    stream_link = f"https://{os.getenv('RAILWAY_STATIC_URL')}/{file_id}"
    await message.reply(f"✅ File saved!\n🔗 [Click here to stream or download]({stream_link})", disable_web_page_preview=True)

@app.route("/<file_id>")
def download(file_id):
    file_path = files.get(file_id)
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "❌ File not found", 404

bot.start()
app.run(host="0.0.0.0", port=3000)
