from datetime import datetime
from pytz import timezone
from telethon import events

async def time_command(event):
    # This command responds with the current time in IST
    ist_timezone = timezone("Asia/Kolkata")
    current_time = datetime.now(ist_timezone).strftime("%H:%M:%S")
    await event.respond(f"The current time (IST) is {current_time}")

def setup(client):
    # Register the command with the client
    client.add_event_handler(time_command, events.NewMessage(pattern=r"\.time"))
