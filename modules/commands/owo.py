import random import re from telethon import events

async def owo_command(event): try: args = event.text.split(" ")[1:] if not args: await event.respond("Bruh gimme some text to owo-ify 😭") return

text = ' '.join(args)


    letter_map = {
        'r': 'w', 'l': 'w', 'R': 'W', 'L': 'W',
        'no': 'nyo', 'na': 'nya', 'ne': 'nye', 'ni': 'nyi', 'nu': 'nyu',
        'ove': 'uv', 'th': 'd', 'er': 'ew', 'you': 'yuu'
    }
    for k, v in letter_map.items():
        text = text.replace(k, v)


    word_map = {
        'love': 'wuv', 'friend': 'fwiend', 'hello': 'hewwo', 'hi': 'hai',
        'cute': 'kawaii~', 'yes': 'yus', 'no': 'nu', 'ok': 'oki', 'thanks': 'fankyu',
        'please': 'pwease', 'cool': 'kawaii~', 'good': 'gwoot', 'bad': 'baddie~',
        'happy': 'happuw', 'sad': 'sadsies', 'dog': 'doggo', 'cat': 'kitteh',
        'night': 'nyite~', 'day': 'dayo~', 'lol': 'rawr~', 'omg': 'omwgee~',
        'bye': 'bai~', 'okay': 'oki~', 'wow': 'wooow~', 'omg': 'omgosh~'
    }
    for k, v in word_map.items():
        text = re.sub(rf'\b{k}\b', v, text, flags=re.IGNORECASE)


    sentences = re.split(r'([.!?])', text)
    owo_sentences = []
    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        punct = sentences[i+1] if i+1 < len(sentences) else ''

        def stutter(word):
            if random.random() < 0.3:
                return word[0] + '-' + word
            return word
        sentence = ' '.join([stutter(w) for w in sentence.split()])


        suffixes = [' uwu', ' owo', ' >w<', ' ^w^', ' (✿◕‿◕)', ' rawr x3', ' nyaa~', ' :3', ' hehe~', ' nya~']
        sentence += random.choice(suffixes)

        
        sentence = ''.join([c.upper() if random.random() < 0.1 else c for c in sentence])

        owo_sentences.append(sentence + punct)

    owo_text = ' '.join(owo_sentences)

    face_map = {
        'happy': ['(^_^)', '(✿^‿^)', '(*^▽^*)'],
        'sad': ['(T_T)', '(;_;)', '(ಥ_ಥ)'],
        'angry': ['>:( ', '(ง'̀-'́)ง'],
        'love': ['❤', '💖', '💕'],
        'cat': ['=^.^='],
        'dog': ['U・ᴥ・U']
    }
    for k, v_list in face_map.items():
        if k in owo_text.lower():
            owo_text += ' ' + random.choice(v_list)

    await event.respond(owo_text)

except Exception as e:
    print(f"Error in owo command: {e}")

--- Setup for Telethon ---

def setup(client): client.add_event_handler(owo_command, events.NewMessage(pattern=r".owo"))
