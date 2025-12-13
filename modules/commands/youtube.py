from telethon import events
from youtubesearchpython import VideosSearch

async def youtube_command(event):
    try:
        args = event.text.split(maxsplit=1)

        if len(args) < 2:
            await event.respond("Usage: `.yt <search query>` 😭")
            return

        query = args[1]
        search = VideosSearch(query, limit=5)
        results = search.result()["result"]

        if not results:
            await event.respond("No results found 🥲")
            return

        msg = "**YouTube Search Results:**\n\n"
        for i, video in enumerate(results, start=1):
            title = video["title"]
            channel = video["channel"]["name"]
            link = video["link"]
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
