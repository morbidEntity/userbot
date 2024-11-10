from bot import client
from bot.commands import alive, abuse
from bot.logging import logger

async def main():
    async with client:
        logger.info("Bot started successfully.")
        await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
