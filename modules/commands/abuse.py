from telethon import events
from modules import config, logging

ABUSE_IMAGE_URL = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaxicqMk6tjqJYHBaSWY0tEeMJBK_1O4Fra0Y4nNsfbA&s'

def setup(client):
    @client.on(events.NewMessage(pattern=r"\.abuse\s+(.+)"))
    async def handle_abuse(event):
        try:
            # Extract the name from the message
            name = event.pattern_match.group(1)
            
            # Create an abuse message for the mentioned person
            response = f"{name} randichoda !!"
            
            # Send the response with the abuse image
            await event.reply(response, file=ABUSE_IMAGE_URL)
            
        except Exception as e:
            # Log the error for debugging
            if hasattr(logging, 'logger'):
                logging.logger.error(f"Error in .abuse command: {e}")
            else:
                print(f"Error in .abuse command: {e}")
