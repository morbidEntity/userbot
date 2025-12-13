from telethon import events, Button
from gtts import gTTS
import asyncio
import os

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Japanese": "ja",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh-cn",
    "Korean": "ko"
}

async def tts_command(event):
    if not event.is_reply:
        await event.respond("Please reply to a message to convert it to speech 😅")
        return

    reply_msg = await event.get_reply_message()
    text = reply_msg.text
    if not text:
        await event.respond("The replied message has no text 😢")
        return

    buttons = [
        [Button.inline(name, f"tts_{code}") for name, code in LANGUAGES.items()]
    ]
    await event.respond("Select language for TTS:", buttons=buttons)

async def button_handler(event):
    if event.data.decode().startswith("tts_"):
        lang_code = event.data.decode().split("_")[1]
        original_msg = await event.get_reply_message()
        text = original_msg.text
        try:
            tts = gTTS(text=text, lang=lang_code)
            file_path = f"tts_{event.sender_id}.mp3"
            tts.save(file_path)
            await event.respond(file=file_path)
            os.remove(file_path)
        except Exception as e:
            await event.respond(f"Error generating TTS: {e}")

def setup(client):
    client.add_event_handler(tts_command, events.NewMessage(pattern=r"\.tts"))
    client.add_event_handler(button_handler, events.CallbackQuery())
