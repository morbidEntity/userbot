import time
import json
import os
from datetime import datetime, timezone, timedelta
from telethon import events
from modules import logging

# --- Configuration for Data Storage ---
# We will use a simple JSON file to store the AFK state persistently.
AFK_DATA_FILE = "afk_state.json"
AFK_REPLY_COOLDOWN = 60 # seconds before replying to the same user again

# --- Helper Functions for Data Management ---

def load_afk_state():
    """Loads the AFK state from the JSON file."""
    if os.path.exists(AFK_DATA_FILE):
        try:
            with open(AFK_DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.logger.error("AFK state file is corrupted. Starting fresh.")
            return {"is_afk": False, "reason": None, "start_time": None, "replied_users": {}}
    return {"is_afk": False, "reason": None, "start_time": None, "replied_users": {}}

def save_afk_state(state):
    """Saves the current AFK state to the JSON file."""
    with open(AFK_DATA_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def calculate_duration(start_time_iso):
    """Calculates and formats the AFK duration."""
    try:
        start_time = datetime.fromisoformat(start_time_iso)
        now = datetime.now(timezone.utc)
        duration = now - start_time
        
        total_seconds = int(duration.total_seconds())
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if not parts:
            parts.append(f"{seconds}s")
            
        return " ".join(parts)
        
    except Exception as e:
        logging.logger.error(f"Error calculating duration: {e}")
        return "Unknown Time"

# --- Command Handler: .afk ---

async def afk_command(event, client):
    """Sets the AFK status ON."""
    
    # Check if a reason was provided
    reason = event.text.split(" ", 1)[1] if len(event.text.split()) > 1 else None
    
    # Get current time and format it for JSON storage
    afk_time = datetime.now(timezone.utc).isoformat()
    
    # Update and Save State
    state = load_afk_state()
    state["is_afk"] = True
    state["reason"] = reason
    state["start_time"] = afk_time
    # Clear replied users on new AFK session
    state["replied_users"] = {} 
    save_afk_state(state)

    # Send confirmation message
    if reason:
        response_text = f"😴 **AFK Mode ON.** Reason: `{reason}`"
    else:
        response_text = "😴 **AFK Mode ON.** (No reason provided)"
        
    await event.edit(response_text)
    
# --- The AFK Listener ---

async def afk_listener(event, client):
    """Listens for messages and auto-replies if the user is AFK and mentioned/replied to."""
    
    # 1. Load state and check if AFK is active
    state = load_afk_state()
    if not state.get("is_afk"):
        return

    # 2. Check if the incoming message is from the bot's user (You)
    me = await client.get_me()
    if event.sender_id == me.id:
        # If the AFK user sends a message, they are back. Turn AFK OFF.
        state["is_afk"] = False
        save_afk_state(state)
        
        # Calculate duration of AFK time for the "Welcome Back" message
        if state.get("start_time"):
            duration = calculate_duration(state["start_time"])
            await event.respond(f"👋 **I'm Back!** I was AFK for `{duration}`.")
        else:
            await event.respond("👋 **I'm Back!** AFK mode disabled.")
        return

    # 3. Check for mentions or replies
    is_mention = me.username and f"@{me.username}" in event.raw_text
    is_reply_to_me = event.is_reply and (await event.get_reply_message()).sender_id == me.id
    
    if is_mention or is_reply_to_me:
        sender_id = str(event.sender_id)
        current_time = time.time()
        replied_users = state.get("replied_users", {})
        
        # Check cooldown to prevent reply spamming
        last_reply_time = replied_users.get(sender_id, 0)
        if current_time - last_reply_time < AFK_REPLY_COOLDOWN:
            return # Don't reply, still in cooldown
        
        # Get AFK data
        reason = state.get("reason", "No reason provided.")
        start_time_iso = state.get("start_time")
        
        duration = calculate_duration(start_time_iso) if start_time_iso else "Unknown Time"

        # Construct the AFK message
        afk_message = (
            f"🛑 I am currently **AFK** (Away From Keyboard).\n"
            f"Reason: `{reason}`\n"
            f"I have been away for **{duration}**."
        )

        # Send the reply
        await event.reply(afk_message)
        
        # Update cooldown and save
        replied_users[sender_id] = current_time
        state["replied_users"] = replied_users
        save_afk_state(state)


# --- Setup Function (Hooking into main.py) ---

def setup(client):
    # Command to set AFK state
    client.add_event_handler(lambda e: afk_command(e, client), events.NewMessage(pattern=r".afk(.*)", outgoing=True))
    
    # Listener for all messages
    client.add_event_handler(lambda e: afk_listener(e, client), events.NewMessage(func=lambda e: not e.out))
    
    # Initialize the AFK state file if it doesn't exist
    load_afk_state()


