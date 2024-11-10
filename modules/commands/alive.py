import time
from telethon import events
from modules import config, logging

start_time = time.time()
message_count = 0

def calculate_uptime():
    uptime = time.time() - start_time
    days, hours = divmod(uptime // 3600, 24)
    minutes, seconds = divmod(uptime % 3600, 60)
    return f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"

def setup(client):
    @client.on(events.NewMessage(pattern=r"\.alive"))
    async def handle_alive(event):
        global message_count
        try:
            start_ping = time.time()
            message_count += 1
            ping = round((time.time() - start_ping) * 1000)
            response = (
                f"✨ I am Alive!\n"
                f"Ping: {ping} ms\n"
                f"Messages Sent: {message_count}\n"
                f"Uptime: {calculate_uptime()}"
            )
            await event.reply(response, file=config.ALIVE_IMAGE_PATH)
        except Exception as e:
            logging.logger.error(f"Error in .alive command: {e}")
