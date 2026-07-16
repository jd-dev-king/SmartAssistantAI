import requests


def get_weather(city):

    try:
        url = f"https://wttr.in/{city}?format=3"

        response = requests.get(url, timeout=5)

        return response.text

    except Exception:
        return "Unable to retrieve weather."
