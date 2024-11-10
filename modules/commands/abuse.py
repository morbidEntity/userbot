from telethon import events
from modules import config, logging
ABUSE_IMAGE_URL='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaxicqMk6tjqJYHBaSWY0tEeMJBK_1O4Fra0Y4nNsfbA&s'

def setup(client):
    @client.on(events.NewMessage(pattern=r"\.abuse\s+(.+)"))
    async def handle_abuse(event):
        try:
            name = event.pattern_match.group(1)
            response = f"{name} teri maa ki chut!! 1,2,3,4 {name} ki gand maaro yar!"
            await event.reply(response, file=ABUSE_IMAGE_URL)
        except Exception as e:
            logging.logger.error(f"Error in .abuse command: {e}")
