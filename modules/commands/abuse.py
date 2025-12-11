from telethon import events
from modules import config, logging

YOUR_USER_ID = 6790833554  # Replace with your actual Telegram user ID
ABUSE_IMAGE_URL = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaxicqMk6tjqJYHBaSWY0tEeMJBK_1O4Fra0Y4nNsfbA&s'

def setup(client):
    @client.on(events.NewMessage(pattern=r"\.abuse\s+(.+)"))
    async def handle_abuse(event):
        try:
            # Extract the name from the message
            name = event.pattern_match.group(1)
            
            # Check if the bot is in a private chat or group
            if event.is_private and event.sender_id == YOUR_USER_ID:
                # Abuse response for private chat when sender is you
                response = f"{name} Teri maa ki chut Madharchod bahen ke lude teri maa chunda saale bhosdivaale bhn chod teri maa kothe pe chudvati hai 2 rupye me Madharchod tera papa hu mai bhn chod"
            elif not event.is_private and event.sender_id == YOUR_USER_ID:
                # Abuse response for group chat when sender is you
                response = f"{name} Teri maa ki chut Madharchod bahen ke lude teri maa chunda saale bhosdivaale bhn chod teri maa kothe pe chudvati hai 2 rupye me Madharchod tera papa hu mai bhn chod"
            else:
                # If the sender is not you, reply with "muh me lega"
                response = "Muh me lega"
            
            # Send the response
            await event.reply(response, file=ABUSE_IMAGE_URL)
            
        except Exception as e:
            if hasattr(logging, 'logger'):
                logging.logger.error(f"Error in .abuse command: {e}")
            else:
                print(f"Error in .abuse command: {e}")
