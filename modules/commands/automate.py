import asyncio
from datetime import datetime
from telethon import TelegramClient

# Function to schedule a message to be sent at the specified time
async def automate_message(client, message, time_str, target):
    # Parse the time string to a datetime object
    target_time = datetime.strptime(time_str, "%I:%M%p").replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)

    # Check if the time is already passed today, if so, set it for tomorrow
    if target_time < datetime.now():
        target_time = target_time.replace(day=datetime.now().day + 1)

    # Calculate the delay until the target time
    delay = (target_time - datetime.now()).total_seconds()

    await asyncio.sleep(delay)  # Wait until the scheduled time
    try:
        if target.startswith("@"):
            # Send the message to a group or channel
            await client.send_message(target, message)
        else:
            # Send the message to a bot
            await client.send_message(target, message)
    except Exception as e:
        print(f"Error sending automated message: {e}")
