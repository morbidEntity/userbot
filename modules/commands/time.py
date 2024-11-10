# modules/commands/time.py

from datetime import datetime
from telethon import events

async def time_command(event):
    # This command responds with the current time
    current_time = datetime.now().strftime("%H:%M:%S")
    await event.respond(f"The current time is {current_time}")

def setup(client):
    # Register the command with the client
    client.add_event_handler(time_command, events.NewMessage(pattern='.time'))
