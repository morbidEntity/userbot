from telethon.sessions import StringSession
from telethon import TelegramClient
from modules import config, logging
from modules.commands import alive, abuse, time, define, automate, flirt, quote, joke, fact, afk, owo
from modules.commands import translate
import asyncio
from flask import Flask
import os
import threading 

# ----------------------------------------------
# 1. FLASK SETUP & PORT BINDING
# ----------------------------------------------
app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

# ----------------------------------------------
# 2. TELETHON CLIENT INITIALIZATION
# ----------------------------------------------
client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

# ----------------------------------------------
# 3. COMMAND SETUP
# ----------------------------------------------
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

# ----------------------------------------------
# 4. ASYNC BOT EXECUTION FUNCTION (Simplified for better startup)
# ----------------------------------------------
async def run_bot():
    """Starts the Telethon client and keeps the loop running."""
    # We use 'await client.run_until_disconnected()' which handles the loop internally
    await client.start()
    logging.logger.info("Bot is running and listening for commands...")
    await client.run_until_disconnected()


# ----------------------------------------------
# 5. FLASK HEALTH CHECK ENDPOINT
# ----------------------------------------------
@app.route('/', methods=['GET'])
def index():
    # We can check if the client is connected for a better health check
    if client.is_connected():
        return "Userbot is running and connected to Telegram!", 200
    else:
        return "Userbot is running but client is disconnected.", 500


# ----------------------------------------------
# 6. SYNCHRONOUS ENTRY POINT (MODIFIED)
# ----------------------------------------------
def main_entry():
    """Starts the Telethon client in a separate thread and runs Flask in the main thread."""
    
    # 🚨 FIX 1: Start the Async Bot in a Separate Thread 🚨
    # This is the most reliable way to run a synchronous web server (Flask/Werkzeug)
    # alongside a continuous asynchronous task (Telethon) without Gunicorn.
    def bot_thread_target():
        # Telethon needs its own event loop to run here
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot())

    bot_thread = threading.Thread(target=bot_thread_target)
    bot_thread.start()
    
    # 🚨 FIX 2: Run Flask in the Main Thread 🚨
    logging.logger.info(f"Flask is binding to 0.0.0.0:{port} for Render health check.")
    # The Flask server will block this thread, keeping the process alive.
    app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    main_entry()
    loop.create_task(run_bot()) # <-- run_bot is now defined above, fixing the NameError
    
    # Start the Flask app, blocking the main thread until it's stopped.
    # Flask will run using the main loop's thread.
    logging.logger.info(f"Flask is binding to 0.0.0.0:{port} for Render health check.")
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main_entry()
    loop.create_task(run_bot())
    
    # Start the Flask app, blocking the main thread until it's stopped.
    # Flask will run using the main loop's thread.
    logging.logger.info(f"Flask is binding to 0.0.0.0:{port} for Render health check.")
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main_entry()
