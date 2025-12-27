import os
from gtts import gTTS
from telethon import events
from modules import logging

LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "ja": "Japanese",
    "de": "German",
    "it": "Italian",
    "ko": "Korean",
}

async def tts_command(event):
    args = event.text.split(maxsplit=2)
    reply = await event.get_reply_message()
    
    # 1. Show help if no arguments and no reply
    if len(args) == 1 and not reply:
        lang_list = "\n".join([f"**{code}**: {name}" for code, name in LANGUAGES.items()])
        await event.edit(f"ℹ️ **TTS Usage:**\n1. Reply to a message with `.tts <lang_code>`\n2. Or type `.tts <lang_code> <text>`\n\n**Codes:**\n{lang_list}")
        return

    # 2. Determine Language Code
    # If the first arg is a valid code, use it. Otherwise, default to English.
    lang_code = "en"
    text_from_cmd = ""

    if len(args) > 1:
        if args[1].lower() in LANGUAGES:
            lang_code = args[1].lower()
            if len(args) > 2:
                text_from_cmd = args[2]
        else:
            # First arg wasn't a code, so treat the whole thing as text for English
            text_from_cmd = event.text.split(maxsplit=1)[1]

    # 3. Determine the text to convert
    if reply and reply.text:
        text_to_speak = reply.text
    elif text_from_cmd:
        text_to_speak = text_from_cmd
    else:
        await event.edit("❌ I couldn't find any text to convert! Reply to a message or provide text.")
        return

    await event.edit(f"🎙️ **Converting to {LANGUAGES.get(lang_code)}...**")

    try:
        filename = f"tts_{event.id}.mp3"
        tts = gTTS(text=text_to_speak, lang=lang_code)
        tts.save(filename)

        # Upload the audio file
        # We reply to the same message the user replied to, or just send it in chat
        target = reply.id if reply else event.id
        await event.client.send_file(event.chat_id, filename, reply_to=target)
        
        await event.delete() 
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        await event.edit(f"⚠️ **Error:** {str(e)}")
        logging.logger.error(f"TTS Error: {e}")

def setup(client):
    client.add_event_handler(tts_command, events.NewMessage(pattern=r"\.tts", outgoing=True))
    
