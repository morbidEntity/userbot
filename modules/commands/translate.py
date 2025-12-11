from telethon import events
from deep_translator import GoogleTranslator

# Mapping common language names to Google Translate codes
LANG_MAP = {
    'english': 'en',
    'hindi': 'hi',
    'japanese': 'ja',
    'spanish': 'es',
    'french': 'fr',
    'german': 'de',
    'chinese': 'zh-cn',
    'korean': 'ko',
    'italian': 'it',
    'arabic': 'ar',
    'russian': 'ru',
    'portuguese': 'pt',
    'turkish': 'tr'
}

async def translate_command(event):
    try:
        # Ensure the command is a reply
        if not event.is_reply:
            await event.respond("Please reply to a message to translate it 😅")
            return

        args = event.text.split()
        if len(args) < 2:
            await event.respond("Please specify the target language. Example: `.tr hindi`")
            return

        lang_name = args[1].lower()
        if lang_name not in LANG_MAP:
            await event.respond(f"Language '{lang_name}' not supported. Try English, Hindi, Japanese, etc.")
            return

        target_lang = LANG_MAP[lang_name]

        reply_msg = await event.get_reply_message()
        text_to_translate = reply_msg.text

        if not text_to_translate:
            await event.respond("The replied message has no text to translate 😢")
            return

        # Use deep-translator for translation
        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text_to_translate)

        await event.respond(f"**Translated ({lang_name}):**\n{translated_text}")

    except Exception as e:
        await event.respond(f"Error while translating: {e}")
        print(f"Translate command error: {e}")

def setup(client):
    client.add_event_handler(translate_command, events.NewMessage(pattern=r"\.tr"))
