import requests
from telethon import events

async def joke_command(event):
    try:
        response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
        data = response.json()

        if response.status_code == 200 and 'joke' in data:
            joke = data['joke']
            await event.respond(joke)
        else:
            await event.respond("Couldn't fetch a joke right now. Try again later!")
    except Exception as e:
        await event.respond("An error occurred while fetching a joke.")
        logging.logger.error(f"Error in .joke command: {e}")

def setup(client):
    client.add_event_handler(joke_command, events.NewMessage(pattern=r"\.joke"))
