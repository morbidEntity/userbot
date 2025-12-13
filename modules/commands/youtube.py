import os
import uuid
import asyncio
from telethon import events, Button
import yt_dlp

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

YTDLP_BASE = {
    "quiet": True,
    "no_warnings": True,
    "outtmpl": f"{DOWNLOAD_DIR}/%(title).60s.%(ext)s"
}

YT_CACHE = {}

def build_message(data, i):
    v = data["results"][i]
    return (
        f"**YouTube Search Result {i+1}/{len(data['results'])}**\n\n"
        f"🎵 **{v['title']}**\n"
        f"👤 {v['channel']}\n"
        f"🔗 https://youtube.com/watch?v={v['id']}"
    )

def build_buttons(sid):
    return [
        [
            Button.inline("◀️", f"yt:prev:{sid}"),
            Button.inline("▶️", f"yt:next:{sid}")
        ],
        [
            Button.inline("🎵 MP3", f"yt:mp3:{sid}"),
            Button.inline("🎬 MP4", f"yt:mp4:{sid}")
        ],
        [
            Button.inline("🔗 Open", f"yt:open:{sid}")
        ]
    ]

async def yt_command(event):
    query = event.text.split(" ", 1)
    if len(query) < 2:
        await event.reply("Usage: `.yt <search>`")
        return

    query = query[1]
    sid = str(uuid.uuid4())

    def search():
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(f"ytsearch5:{query}", download=False)
            return [
                {
                    "id": v["id"],
                    "title": v["title"],
                    "channel": v.get("uploader", "Unknown")
                }
                for v in info["entries"]
            ]

    results = await asyncio.get_event_loop().run_in_executor(None, search)

    if not results:
        await event.reply("No results found 💀")
        return

    YT_CACHE[sid] = {"results": results, "page": 0}

    await event.reply(
        build_message(YT_CACHE[sid], 0),
        buttons=build_buttons(sid)
    )

@events.register(events.CallbackQuery(pattern=b"yt:(.+)"))
async def yt_callback(event):
    _, action, sid = event.data.decode().split(":")

    if sid not in YT_CACHE:
        await event.answer("Expired ❌", alert=True)
        return

    data = YT_CACHE[sid]

    if action == "next":
        data["page"] = (data["page"] + 1) % len(data["results"])
        await event.edit(
            build_message(data, data["page"]),
            buttons=build_buttons(sid)
        )

    elif action == "prev":
        data["page"] = (data["page"] - 1) % len(data["results"])
        await event.edit(
            build_message(data, data["page"]),
            buttons=build_buttons(sid)
        )

    elif action == "open":
        v = data["results"][data["page"]]
        await event.respond(f"https://youtube.com/watch?v={v['id']}")

    elif action in ("mp3", "mp4"):
        await event.answer("Downloading… ⏳")
        await download_and_send(event, data["results"][data["page"]], action)

async def download_and_send(event, video, mode):
    loop = asyncio.get_event_loop()
    url = f"https://youtube.com/watch?v={video['id']}"

    opts = YTDLP_BASE.copy()

    if mode == "mp3":
        opts.update({
            "format": "bestaudio",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }]
        })
    else:
        opts.update({
            "format": "best[filesize<50M]/best"
        })

    def task():
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=True)

    info = await loop.run_in_executor(None, task)

    file = yt_dlp.YoutubeDL(opts).prepare_filename(info)
    if mode == "mp3":
        file = file.rsplit(".", 1)[0] + ".mp3"

    if os.path.getsize(file) > 50 * 1024 * 1024:
        os.remove(file)
        await event.respond("File too large for Telegram 😭")
        return

    await event.respond(file=file)
    os.remove(file)

def setup(client):
    client.add_event_handler(yt_command, events.NewMessage(pattern=r"\.yt"))
