import requests
from telethon import events

async def fact_command(event):
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        data = response.json()

        if response.status_code == 200 and 'text' in data:
            fact = data['text']
            await event.respond(f"Fun Fact: {fact}")
        else:
            await event.respond("Couldn't fetch a fun fact right now.")
    except Exception as e:
        await event.respond("An error occurred while fetching a fun fact.")
        logging.logger.error(f"Error in .fact command: {e}")

def setup(client):
    client.add_event_handler(fact_command, events.NewMessage(pattern=r"\.fact"))
