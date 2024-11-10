from telethon.sessions import StringSession
from telethon import TelegramClient
from modules import config, logging
from modules.commands import alive, abuse, time, define, automate, flirt, quote, joke, fact, inspire, translate 
import asyncio

client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

# Set up commands
alive.setup(client)
abuse.setup(client)
time.setup(client)
define.setup(client)
automate.setup(client)
flirt.setup(client)
quote.setup(client)
joke.setup(client)
fact.setup(client)
inspire.setup(client)
translate.setuo(client)

async def main():
    async with client:
        logging.logger.info("Bot is running...")
        await client.run_until_disconnected()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
