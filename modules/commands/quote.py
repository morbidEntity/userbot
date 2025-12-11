import aiohttp
import logging
from telethon import events

async def quote_command(event):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.quotable.io/random") as response:
                if response.status == 200:
                    data = await response.json()
                    quote = data.get('content', None)
                    author = data.get('author', 'Unknown')

                    if quote:
                        await event.respond(f"\"{quote}\" - {author}")
                        return

        # fallback
        await event.respond("Couldn't fetch a quote right now, bro 😭")
    except Exception as e:
        logging.error(f"Error in .quote command: {e}")
        await event.respond("Bro something exploded while fetching a quote 💀")

def setup(client):
    client.add_event_handler(quote_command, events.NewMessage(pattern=r"\.quote"))
