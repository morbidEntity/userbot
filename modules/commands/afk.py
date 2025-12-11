import json
import os
import time
from datetime import datetime, timezone
from telethon import events
from modules import logging

AFK_DATA_FILE = "afk_state.json"
AFK_REPLY_COOLDOWN = 60  # seconds per-user cooldown


# ------------------- STORAGE HELPERS -------------------

def load_afk_state():
    if os.path.exists(AFK_DATA_FILE):
        try:
            with open(AFK_DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.logger.error("AFK file corrupted, resetting.")
    return {"is_afk": False, "reason": None, "start_time": None, "replied": {}}


def save_afk_state(state):
    with open(AFK_DATA_FILE, "w") as f:
        json.dump(state, f, indent=4)


def get_duration(start):
    try:
        start_time = datetime.fromisoformat(start)
    except:
        return "Unknown"

    now = datetime.now(timezone.utc)
    delta = now - start_time
    secs = int(delta.total_seconds())

    d, r = divmod(secs, 86400)
    h, r = divmod(r, 3600)
    m, s = divmod(r, 60)

    out = []
    if d: out.append(f"{d}d")
    if h: out.append(f"{h}h")
    if m: out.append(f"{m}m")
    if not out: out.append(f"{s}s")
    return " ".join(out)


# ------------------- AFK COMMAND -------------------

async def afk_command(event):
    reason = event.text.split(" ", 1)[1] if " " in event.text else None

    state = {
        "is_afk": True,
        "reason": reason,
        "start_time": datetime.now(timezone.utc).isoformat(),
        "replied": {}
    }
    save_afk_state(state)

    if reason:
        await event.edit(f"😴 AFK enabled.\nReason: `{reason}`")
    else:
        await event.edit("😴 AFK enabled.")


# ------------------- MESSAGE LISTENER -------------------

async def afk_listener(event, client):

    # Load current AFK state
    state = load_afk_state()

    # If AFK is OFF → ignore
    if not state.get("is_afk"):
        return

    # If YOU send ANY message → AFK OFF
    if event.out:
        state["is_afk"] = False
        save_afk_state(state)

        # Calculate duration
        dur = get_duration(state.get("start_time"))
        await event.respond(f"👋 I'm back! AFK for `{dur}`.")
        return

    # ------------------- Mention / Reply Check -------------------
    me = await client.get_me()
    is_mention = me.username and f"@{me.username}" in event.raw_text

    is_reply = False
    if event.is_reply:
        try:
            msg = await event.get_reply_message()
            is_reply = (msg.sender_id == me.id)
        except:
            pass

    if not (is_mention or is_reply):
        return  # If they didn’t tag/reply to you → ignore

    # ------------------- Cooldown Check -------------------
    sender = str(event.sender_id)
    now = time.time()
    last_reply = state["replied"].get(sender, 0)

    if now - last_reply < AFK_REPLY_COOLDOWN:
        return  # still in cooldown

    # ------------------- Send AFK Message -------------------
    reason = state.get("reason") or "No reason provided."
    duration = get_duration(state.get("start_time"))

    text = (
        f"🛑 I am AFK.\n"
        f"Reason: `{reason}`\n"
        f"Away for: **{duration}**"
    )

    await event.reply(text)

    # update cooldown
    state["replied"][sender] = now
    save_afk_state(state)


# ------------------- SETUP -------------------

def setup(client):
    client.add_event_handler(afk_command, events.NewMessage(pattern=r"\.afk"))
    client.add_event_handler(lambda e: afk_listener(e, client), events.NewMessage())
