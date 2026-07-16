import requests


def define_word(word):

    try:

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        response = requests.get(url, timeout=5)

        data = response.json()

        definition = (
            data[0]
            ["meanings"][0]
            ["definitions"][0]
            ["definition"]
        )

        return definition

    except Exception:
        return "Definition not found."