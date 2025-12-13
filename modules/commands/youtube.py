from telethon import events
import yt_dlp
import asyncio

YTDLP_OPTS = {
    "quiet": True,
    "skip_download": True,
    "extract_flat": True,
}

async def youtube_command(event):
    try:
        args = event.text.split(maxsplit=1)

        if len(args) < 2:
            await event.respond("Usage: `.yt <search query>` 😭")
            return

        query = args[1]

        loop = asyncio.get_event_loop()

        def search():
            with yt_dlp.YoutubeDL(YTDLP_OPTS) as ydl:
                return ydl.extract_info(f"ytsearch5:{query}", download=False)

        info = await loop.run_in_executor(None, search)
        results = info.get("entries", [])

        if not results:
            await event.respond("No results found 🥲")
            return

        msg = "**YouTube Search Results:**\n\n"
        for i, video in enumerate(results, start=1):
            title = video.get("title")
            channel = video.get("uploader")
            link = f"https://youtube.com/watch?v={video.get('id')}"
            msg += f"{i}. **{title}**\n👤 {channel}\n🔗 {link}\n\n"

        await event.respond(msg)

    except Exception as e:
        await event.respond(f"Something broke 💀\n`{e}`")
        print(f"YouTube command error: {e}")

def setup(client):
    client.add_event_handler(
        youtube_command,
        events.NewMessage(pattern=r"\.(yt|youtube)")
            )
