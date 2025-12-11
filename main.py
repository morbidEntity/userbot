from telethon.sessions import StringSession
from telethon import TelegramClient
from modules import config, logging
from modules.commands import (
    alive, abuse, time, define, automate, flirt, quote, joke, fact, afk, owo, translate
)
import asyncio
from flask import Flask
import os
import threading

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

alive.setup(client)
abuse.setup(client)
time.setup(client)
define.setup(client)
automate.setup(client)
flirt.setup(client)
quote.setup(client)
joke.setup(client)
fact.setup(client)
afk.setup(client)
owo.setup(client)
translate.setup(client)

async def run_bot():
    await client.start()
    logging.logger.info("Bot is running and listening for commands...")
    await client.run_until_disconnected()

@app.route("/", methods=["GET"])
def index():
    if client.is_connected():
        return "Userbot is running and connected to Telegram!", 200
    return "Userbot is running but client is disconnected.", 500

def main_entry():
    def bot_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot())

    threading.Thread(target=bot_thread).start()
    logging.logger.info(f"Flask is binding to 0.0.0.0:{port} for health check.")
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main_entry()
