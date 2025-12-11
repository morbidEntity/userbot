from telethon.sessions import StringSession
from telethon import TelegramClient
from modules import config, logging
from modules.commands import alive, abuse, time, define, automate, flirt, quote, joke, fact, afk
import asyncio
from flask import Flask
import os

# ----------------------------------------------
# 1. FLASK SETUP & PORT BINDING
# ----------------------------------------------
app = Flask(__name__)
# Get the port from environment variable, default to 5000 if not set
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

# ----------------------------------------------
# 4. ASYNC BOT EXECUTION FUNCTION (Moved to be DEFINED before main_entry uses it)
# ----------------------------------------------
async def run_bot():
    """Starts the Telethon client and runs until disconnected."""
    # We use 'client.start()' instead of 'async with client' here 
    # to better integrate with the existing event loop that Flask is using.
    # The 'async with client' is cleaner but sometimes causes issues when
    # combined with a background task like this, so we use start/run_until_disconnected.
    await client.start()
    logging.logger.info("Bot is running...")
    await client.run_until_disconnected()

# ----------------------------------------------
# 5. FLASK HEALTH CHECK ENDPOINT
# ----------------------------------------------
@app.route('/', methods=['GET'])
def index():
    # This is a simple health check. Render looks for this to know the app is running.
    return "Userbot is running!", 200

# ----------------------------------------------
# 6. SYNCHRONOUS ENTRY POINT
# ----------------------------------------------
def main_entry():
    """Synchronous entry point to start the async loop and the web server."""
    loop = asyncio.get_event_loop()
    
    # Run the bot in a background task
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
