from telethon import events, Button
import requests
from bs4 import BeautifulSoup

async def google_command(event):
    if event.is_reply:
        query = (await event.get_reply_message()).text
    else:
        args = event.text.split(maxsplit=1)
        if len(args) < 2:
            await event.respond("Please provide a query to search. Example: `.google Garou theme`")
            return
        query = args[1]

    search_url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for g in soup.find_all('div', class_='tF2Cxc')[:5]:  # top 5 results
            title = g.find('h3').text if g.find('h3') else "No title"
            link = g.find('a')['href'] if g.find('a') else ""
            if link:
                results.append((title, link))

        if not results:
            await event.respond("No results found 😢")
            return

        buttons = [Button.url(f"{title}", link) for title, link in results]
        await event.respond("Google Search Results:", buttons=buttons)

    except Exception as e:
        await event.respond(f"Error searching Google: {e}")

def setup(client):
    client.add_event_handler(google_command, events.NewMessage(pattern=r"\.google"))
