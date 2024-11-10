import asyncio
from telethon import events
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
import datetime
from modules import logging

# Set up the scheduler
scheduler = AsyncIOScheduler()
ist_timezone = timezone("Asia/Kolkata")  # IST timezone

async def send_message_at_scheduled_time(message, group_or_bot, scheduled_time):
    now = datetime.datetime.now(ist_timezone)
    delay = (scheduled_time - now).total_seconds()

    if delay < 0:
        logging.logger.warning("Scheduled time is in the past. Unable to send message.")
        return

    await asyncio.sleep(delay)
    try:
        await client.send_message(group_or_bot, message)
        logging.logger.info(f"Message sent to {group_or_bot} at {scheduled_time.strftime('%I:%M %p')}")
    except Exception as e:
        logging.logger.error(f"Error sending message: {e}")

def setup(client):
    @client.on(events.NewMessage(pattern=r"\.automate\s+(.+?)\s+(\S+)\s+(@\S+)"))
    async def handle_automate_command(event):
        try:
            message = event.pattern_match.group(1)
            scheduled_time_str = event.pattern_match.group(2)
            group_or_bot = event.pattern_match.group(3)

            try:
                # Parse the scheduled time and convert to IST timezone
                scheduled_time = datetime.datetime.strptime(scheduled_time_str, "%I:%M%p")
                now = datetime.datetime.now(ist_timezone)
                scheduled_time = ist_timezone.localize(scheduled_time.replace(year=now.year, month=now.month, day=now.day))

                if scheduled_time < now:
                    scheduled_time += datetime.timedelta(days=1)
            except ValueError:
                await event.reply("Invalid time format. Please use 12-hour format (e.g., 12:00pm).")
                return

            scheduler.add_job(send_message_at_scheduled_time, 'date', run_date=scheduled_time, args=[message, group_or_bot, scheduled_time])
            scheduler.start()

            await event.reply(f"Message scheduled to be sent to {group_or_bot} at {scheduled_time.strftime('%I:%M %p IST')}")
            logging.logger.info(f"Automated message scheduled: {message} at {scheduled_time.strftime('%I:%M %p IST')}")
        except Exception as e:
            logging.logger.error(f"Error in .automate command: {e}")
            await event.reply("An error occurred while processing the command.")
