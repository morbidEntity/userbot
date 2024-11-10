import requests
from telethon import events

API_KEY = "YOUR_API_KEY"  # Get an API key from Giphy
GIF_URL = "https://api.giphy.com/v1/gifs/random?tag=inspirational&api_key={}"

async def inspire_command(event):
    try:
        response = requests.get(GIF_URL.format(API_KEY))
        data = response.json()

        if response.status_code == 200 and 'data' in data:
            gif_url = data['data'][0]['images']['original']['url']
            await event.respond(gif_url)
        else:
            await event.respond("Couldn't fetch an inspirational GIF right now.")
    except Exception as e:
        await event.respond("An error occurred while fetching the GIF.")
        logging.logger.error(f"Error in .inspire command: {e}")

def setup(client):
    client.add_event_handler(inspire_command, events.NewMessage(pattern=r"\.inspire"))
