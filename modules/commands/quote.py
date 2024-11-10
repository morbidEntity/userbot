import requests
from telethon import events

async def quote_command(event):
    try:
        response = requests.get("https://api.quotable.io/random")
        data = response.json()

        if response.status_code == 200 and 'content' in data:
            quote = data['content']
            author = data['author']
            await event.respond(f"\"{quote}\" - {author}")
        else:
            await event.respond("Couldn't fetch a quote right now. Try again later!")
    except Exception as e:
        await event.respond("An error occurred while fetching a quote.")
        logging.logger.error(f"Error in .quote command: {e}")

def setup(client):
    client.add_event_handler(quote_command, events.NewMessage(pattern=r"\.quote"))
