import random
import re
from telethon import events

# --- Word & Face maps can be global ---
word_map = {
    'love': 'wuv', 'friend': 'fwiend', 'hello': 'hewwo', 'hi': 'hai',
    'cute': 'kawaii~', 'yes': 'yus', 'no': 'nu', 'ok': 'oki', 'thanks': 'fankyu',
    'please': 'pwease', 'cool': 'cwoo~', 'good': 'gwoot', 'bad': 'baddie~',
    'happy': 'happuw', 'sad': 'sadsies', 'angry': 'grrr~', 'cry': 'bawww~',
    'dog': 'doggo', 'cat': 'kitteh', 'night': 'nyite~', 'day': 'dayo~',
    'lol': 'rawr~', 'omg': 'omwgee~', 'bye': 'bai~', 'okay': 'oki~',
    'wow': 'wooow~', 'omg': 'omgosh~', 'food': 'nomnom~', 'sleep': 'snoozy~',
    'dance': 'boogiewoogie~', 'hug': 'huggies~', 'kiss': 'smoochie~',
    'yay': 'yaaay~', 'oops': 'uwu~', 'drink': 'sip~', 'play': 'pway~',
    'money': 'moneh~', 'smile': 'smiley~', 'friendship': 'fwiendship~',
    'game': 'gamework~', 'fun': 'funnywunny~', 'music': 'tunesies~',
    'sing': 'singy~', 'run': 'runnies~', 'jump': 'bouncy~', 'fight': 'pow~',
    'sleepy': 'snoozie~', 'dream': 'dreamy~', 'cuteee': 'kawaiiii~',
    'loveeee': 'wuvvvy~', 'angryyy': 'grrrrawr~', 'sadness': 'sadsies~',
    'heart': '❤', 'star': '✨', 'shine': 'shiny~', 'rain': 'rainy~', 'storm': 'stormy~',
    'snow': 'snowy~', 'sun': 'sunny~', 'moon': 'moony~', 'fire': 'fwoar~',
    'water': 'waww~', 'light': 'lite~', 'dark': 'darkie~', 'hello?': 'hewwo?'
}

face_map = {
    'happy': ['(^_^)', '(✿^‿^)', '(*^▽^*)', 'UwU', '>w<', '^w^', '(*≧ω≦)', '(*≧∀≦*)'],
    'sad': ['(T_T)', '(;_;)', '(ಥ_ಥ)', '(╥_╥)', '(ಥ﹏ಥ)', '(-_-;)', '(｡•́︿•̀｡)'],
    'angry': ['>:( ', '(ง\'̀-\'́)ง', '(-`_´-)', '(ಠ_ಠ)', '(ノಠ益ಠ)ノ', '(งಠ_ಠ)ง'],
    'love': ['❤', '💖', '💕', '💞', '💘', '💝', '(*♥ω♥*)', '(*≧ω≦)ﾉ💖'],
    'cat': ['=^.^=', '(=①ω①=)', '(ฅ^•ﻌ•^ฅ)', '(=^・^=)', '(=^･ω･^=)'],
    'dog': ['U・ᴥ・U', '(U・x・U)', 'ʕ•ᴥ•ʔ', '(⌒◡⌒)♡', '(*ᵔᴥᵔ*)'],
    'confused': ['(o_O)', '(O_o)', '(¬_¬)', '(•ิ_•ิ)?', '(゜ロ゜;)', '(・_・;)', '(＠_＠;)'],
    'excited': ['(*≧▽≦)', '＼(≧▽≦)／', '(ﾉ^_^)ﾉ', '(*≧ω≦)ﾉ', 'ヽ(*・ω・)ﾉ'],
    'sleepy': ['(-_-) zzz', '(∪｡∪)｡｡｡zzz', '(˘ω˘)', '(*￣︿￣)', '(︶︹︺)'],
    'shock': ['(ﾟﾛﾟ)', 'Σ(゜゜)', '⚡😳', '(@_@)', '(°ロ°) !', 'Σ(⊙_⊙;)'],
    'embarrassed': ['(⁄⁄⁄ω⁄⁄⁄)', '(//ω//)', '(*/ω＼*)', '(>///<)'],
    'thinking': ['(¬‿¬)', '(•_•)?', '(゜-゜)', '(・・;)'],
    'silly': ['(≧▽≦)', '(≧∇≦)/', '(*≧ω≦)', '(⌒▽⌒)☆', '(≧ω≦)'],
    'crying_happy': ['(*T▽T*)', '(T▽T)', '(ToT)', '(；⌣̀_⌣́)']
}

async def owo_command(event):
    try:
        # --- Get text ---
        if event.is_reply:
            reply_msg = await event.get_reply_message()
            text = reply_msg.text
            if not text:
                await event.respond("The replied message has no text to owo-ify 😭")
                return
        else:
            args = event.text.split(" ")[1:]
            if not args:
                await event.respond("Bruh gimme some text to owo-ify 😭 or reply to a message")
                return
            text = ' '.join(args)

        # --- letter replacements ---
        letter_map = {
            'r': 'w', 'l': 'w', 'R': 'W', 'L': 'W',
            'no': 'nyo', 'na': 'nya', 'ne': 'nye', 'ni': 'nyi', 'nu': 'nyu',
            'ove': 'uv', 'th': 'd', 'er': 'ew', 'you': 'yuu'
        }
        for k, v in letter_map.items():
            text = text.replace(k, v)

        # --- word replacements ---
        for k, v in word_map.items():
            text = re.sub(rf'\b{k}\b', v, text, flags=re.IGNORECASE)

        # --- sentence chaos ---
        sentences = re.split(r'([.!?])', text)
        owo_sentences = []
        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            punct = sentences[i+1] if i+1 < len(sentences) else ''

            # random stutter effect
            def stutter(word):
                if random.random() < 0.3:
                    return word[0] + '-' + word
                return word
            sentence = ' '.join([stutter(w) for w in sentence.split()])

            # random suffix
            suffixes = [' uwu', ' owo', ' >w<', ' ^w^', ' (✿◕‿◕)', ' rawr x3', ' nyaa~', ' :3', ' hehe~', ' nya~']
            sentence += random.choice(suffixes)

            # random casing
            sentence = ''.join([c.upper() if random.random() < 0.1 else c for c in sentence])

            owo_sentences.append(sentence + punct)

        owo_text = ' '.join(owo_sentences)

        # --- add face emojis ---
        for k, v_list in face_map.items():
            if k in owo_text.lower():
                owo_text += ' ' + random.choice(v_list)

        await event.respond(owo_text)

    except Exception as e:
        print(f"Error in owo command: {e}")

# --- Setup for Telethon ---
def setup(client):
    client.add_event_handler(owo_command, events.NewMessage(pattern=r".owo"))
