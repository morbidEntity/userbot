import requests

def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url).json()
    
    if "title" in response and response["title"] == "No Definitions Found":
        return f"Sorry, no definitions found for {word}."
    
    definition = response[0]["meanings"][0]["definitions"][0]["definition"]
    return f"The definition of {word} is: {definition}"
