from telethon import events
from modules import config, logging

# Replace 'YOUR_USER_ID' with your actual user ID
YOUR_USER_ID = 6790833554  # Example: 123456789 (replace with your actual Telegram user ID)
ABUSE_IMAGE_URL = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaxicqMk6tjqJYHBaSWY0tEeMJBK_1O4Fra0Y4nNsfbA&s'

def setup(client):
    @client.on(events.NewMessage(pattern=r"\.abuse\s+(.+)"))
    async def handle_abuse(event):
        try:
            name = event.pattern_match.group(1)
            
            # Check if the sender is you
            if event.sender_id == YOUR_USER_ID:
                # If the sender is you, abuse the mentioned person
                response = f"{name} teri maa ki chut!! 1,2,3,4 {name} ki gand maaro yar!"
            else:
                # If the sender is not you, reply with "muh me lega"
                response = "Muh me lega"
            
            await event.respond(response, file=ABUSE_IMAGE_URL)
        except Exception as e:
            logging.logger.error(f"Error in .abuse command: {e}")
