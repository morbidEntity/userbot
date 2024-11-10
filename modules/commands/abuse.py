from telethon import events
from modules import config, logging

def setup(client):
    @client.on(events.NewMessage(pattern=r"\.abuse\s+(.+)"))
    async def handle_abuse(event):
        try:
            name = event.pattern_match.group(1)
            response = f"{name} teri maa ki chut!! 1,2,3,4 {name} ki gand maaro yar!"
            await event.reply(response, file=config.ABUSE_IMAGE_PATH)
        except Exception as e:
            logging.logger.error(f"Error in .abuse command: {e}")
