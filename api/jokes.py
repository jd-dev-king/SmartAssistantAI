import requests


def get_joke():

    try:
        response = requests.get(
            "https://official-joke-api.appspot.com/random_joke",
            timeout=5
        )

        joke = response.json()

        return f"{joke['setup']}\n{joke['punchline']}"

    except Exception:
        return "No jokes available right now."
