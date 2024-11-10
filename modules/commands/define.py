# modules/commands/define.py

import requests
from telethon import events

async def define_command(event):
    # Extract word to define from message
    word = event.text.split(" ", 1)[1] if len(event.text.split()) > 1 else None
    if not word:
        await event.respond("Please provide a word to define!")
        return

    # API to get word definition (you can replace this with a better source)
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        definition = data[0]['meanings'][0]['definitions'][0]['definition']
        await event.respond(f"Definition of {word}: {definition}")
    else:
        await event.respond(f"Sorry, I couldn't find a definition for {word}.")

def setup(client):
    # Register the command with the client
    client.add_event_handler(define_command, events.NewMessage(pattern='.define'))
