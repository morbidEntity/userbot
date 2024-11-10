import requests
from telethon import events

async def flirt_command(event):
    try:
        # Fetch a random quote with a romantic theme
        response = requests.get("https://api.quotable.io/random?tags=love")
        data = response.json()

        # Check if the API request was successful
        if response.status_code == 200 and 'content' in data:
            flirt = data['content']
        else:
            flirt = "Couldn't fetch a flirt line right now. Try again later!"

        await event.respond(flirt)
    except Exception as e:
        await event.respond("An error occurred while fetching a flirt line.")
        logging.logger.error(f"Error in .flirt command: {e}")

def setup(client):
    # Register the flirt command
    client.add_event_handler(flirt_command, events.NewMessage(pattern=r"\.flirt"))
