from telethon import events, Button
from gtts import gTTS
import asyncio
import os

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "Japanese": "ja",
    "German": "de",
    "Italian": "it",
    "Korean": "ko",
}

# Store text temporarily until user selects a language
pending_tts = {}

async def tts_command(event):
    args = event.text.split(maxsplit=1)
    if len(args) < 2:
        await event.respond("Please provide text to convert to speech. Example: `.tts Hello world`")
        return

    text = args[1]
    # Save text using user ID as key
    pending_tts[event.sender_id] = text

    buttons = [Button.inline(name, data=name) for name in LANGUAGES.keys()]
    # Send buttons in a 2-column layout
    keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    await event.respond("Choose a language for TTS:", buttons=keyboard)

async def tts_button_handler(event):
    lang_name = event.data.decode("utf-8")
    user_id = event.sender_id

    if user_id not in pending_tts:
        await event.respond("No text found. Please use `.tts <text>` first.")
        return

    text = pending_tts.pop(user_id)
    lang_code = LANGUAGES.get(lang_name, "en")

    filename = f"/tmp/tts_{user_id}.mp3"
    tts = gTTS(text, lang=lang_code)
    tts.save(filename)

    await event.respond(file=filename)
    os.remove(filename)

def setup(client):
    client.add_event_handler(tts_command, events.NewMessage(pattern=r"\.tts"))
    client.add_event_handler(tts_button_handler, events.CallbackQuery)
