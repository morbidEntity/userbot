from googletrans import Translator
from telethon import events

async def translate_command(event):
    parts = event.text.split(' ', 2)
    if len(parts) < 3:
        await event.respond("Please use the format: `.translate <target_language> <text>`")
        return
    
    target_language = parts[1]
    text = parts[2]
    
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    await event.respond(f"Translated Text: {translated.text}")

def setup(client):
    client.add_event_handler(translate_command, events.NewMessage(pattern=r"\.translate"))
