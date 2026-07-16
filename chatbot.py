from datetime import datetime

from api.weather import get_weather
from api.dictionary import define_word
from api.jokes import get_joke
from api.wiki import search_wiki
from system.monitor import get_system_status
from calculator.math_engine import calculate
from utilities.file_search import search_files
from utilities.app_launcher import open_app
from memory.memory import (
    load_profile,
    save_profile,
    export_history,
    clear_profile
)


def get_response(message):

    original = message
    message = message.lower().strip()

    profile = load_profile()


    # =========================
    # MEMORY FUNCTIONS
    # =========================

    if "my name is" in message:

        name = original.split(
            "is",
            1
        )[1].strip()

        name = name.title()

        profile["name"] = name

        profile["name"] = name

        save_profile(profile)

        save_profile(profile)

        return f"Nice to meet you {name}! I will remember your name."


    elif "my favorite color is" in message:

        color = message.split(
            "my favorite color is",
            1
        )[1].strip()

        color = color.title()

        profile["favorite_color"] = color

        save_profile(profile)

        return f"I'll remember that your favorite color is {color}."


    elif "i work as" in message:

        job = message.split(
            "i work as",
            1
        )[1].strip()

        job = job.title()

        profile["job"] = job

        save_profile(profile)

        return f"I'll remember that you work as a {job}."


    elif "i am a" in message:

        role = message.split(
            "i am a",
            1
        )[1].strip()

        role = role.title()

        profile["job"] = role

        save_profile(profile)

        return f"I'll remember that you are a {role}."


    elif "what is my name" in message:

        if "name" in profile:

            return f"Your name is {profile['name']}."

        return "I don't know your name yet."


    elif "what is my favorite color" in message:

        if "favorite_color" in profile:

            return (
                f"Your favorite color is "
                f"{profile['favorite_color']}."
            )

        return "I don't know your favorite color yet."


    elif "what do i do" in message:

        if "job" in profile:

            return (
                f"You told me that you are a "
                f"{profile['job']}."
            )

        return "I don't know your occupation yet."



    # =========================
    # GREETINGS
    # =========================

    elif message in [
        "hi",
        "hello",
        "hey"
    ]:

        return "Hello! How can I assist you today?"



    # =========================
    # TIME / DATE
    # =========================

    elif "time" in message:

        return datetime.now().strftime(
            "%I:%M %p"
        )


    elif "date" in message:

        return datetime.now().strftime(
            "%B %d, %Y"
        )



    # =========================
    # JOKES
    # =========================

    elif "joke" in message:

        return get_joke()



    # =========================
    # DICTIONARY
    # =========================

    elif message in ["define ", "what is", "whats the definition of"]:

        word = original[7:].strip()

        return define_word(word)



    # =========================
    # WEATHER
    # =========================

    elif "weather" in message:

        city = original[8:].strip()

        return get_weather(city)



    # =========================
    # WIKIPEDIA
    # =========================

    elif message.startswith("wiki "):

        topic = original[5:].strip()

        return search_wiki(topic)


    elif message.startswith("tell me about "):

        topic = original[14:].strip()

        return search_wiki(topic)


    elif message.startswith("who is "):

        topic = original[7:].strip()

        return search_wiki(topic)



    # =========================
    # CALCULATOR
    # =========================

    elif message.startswith("calculate"):

        expression = original.replace(
            "calculate",
            ""
        ).strip()

        return calculate(expression)


    elif message.startswith("solve"):

        expression = original.replace(
            "solve",
            ""
        ).strip()

        return calculate(expression)


    elif "percent of" in message:

        try:

            parts = message.split()

            percent = float(parts[0])

            number = float(parts[-1])

            answer = (percent / 100) * number

            return f"{percent}% of {number} = {answer}"


        except:

            return "I couldn't calculate that percentage."



    # =========================
    # SYSTEM MONITOR
    # =========================

    elif "cpu" in message or "computer" in message:

        return get_system_status()


    elif "ram" in message or "memory usage" in message:

        return get_system_status()


    elif "battery" in message:

        return get_system_status()



    # =========================
    # FILE SEARCH
    # =========================

    elif message.startswith("find "):

        filename = original.replace(
            "find",
            ""
        ).strip()

        return search_files(filename)



    elif message.startswith("search "):

        filename = original.replace(
            "search",
            ""
        ).strip()

        return search_files(filename)



    # =========================
    # APP LAUNCHER
    # =========================

    elif message.startswith("open "):

        app = original.replace(
            "open",
            ""
        ).strip()

        return open_app(app)



    # =========================
    # EXPORT / CLEAR MEMORY
    # =========================

    elif "export chat" in message:

        file = export_history()

        return f"Conversation exported as {file}"


    elif "clear memory" in message:

        return clear_profile()


    elif "clear history" in message:

        from memory.memory import clear_history

        clear_history()

        return "Chat history cleared."



    # =========================
    # EXIT
    # =========================

    elif message == "bye":

        return "Goodbye!"



    # =========================
    # UNKNOWN
    # =========================

    return (
        "Try:\n"
        "• joke\n"
        "• weather Philadelphia\n"
        "• define engineer\n"
        "• wiki Nikola Tesla\n"
        "• cpu usage\n"
        "• battery status\n"
        "• my name is Jeremiah"
    )