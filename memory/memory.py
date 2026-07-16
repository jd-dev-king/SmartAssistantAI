import json
import os
import sys


# Determine application directory

if getattr(sys, "frozen", False):

    BASE_DIR = os.path.join(
        os.path.expanduser("~"),
        "Library",
        "Application Support",
        "SmartAssistantAI"
   )

else:

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )


if not os.path.exists(BASE_DIR):

    os.makedirs(
        BASE_DIR
    )


HISTORY_PATH = os.path.join(
    BASE_DIR,
    "history.json"
)


PROFILE_PATH = os.path.join(
    BASE_DIR,
    "profile.json"
)



# -------------------------
# CHAT HISTORY
# -------------------------

def load_history():

    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    if not os.path.exists(HISTORY_PATH):

        with open(HISTORY_PATH, "w") as file:
            json.dump([], file)


    try:

        with open(HISTORY_PATH, "r") as file:
            return json.load(file)


    except (json.JSONDecodeError, OSError):

        with open(HISTORY_PATH, "w") as file:
            json.dump([], file)

        return []



def save_message(sender, message):

    history = load_history()


    history.append(
        {
            "sender": sender,
            "message": message
        }
    )


    with open(
        HISTORY_PATH,
        "w"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )



def clear_history():

    with open(
        HISTORY_PATH,
        "w"
    ) as file:

        json.dump(
            [],
            file,
            indent=4
        )



def export_history():

    history = load_history()


    filename = "conversation_export.txt"


    with open(
        filename,
        "w"
    ) as file:

        for item in history:

            file.write(
                f"{item['sender']}: {item['message']}\n\n"
            )


    return filename



# -------------------------
# USER PROFILE
# -------------------------

def load_profile():

    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    if not os.path.exists(PROFILE_PATH):

        with open(PROFILE_PATH, "w") as file:
            json.dump({}, file)


    try:

        with open(PROFILE_PATH, "r") as file:
            data = json.load(file)

            if data == "":
                return {}

            return data


    except (json.JSONDecodeError, OSError):

        with open(PROFILE_PATH, "w") as file:
            json.dump({}, file)

        return {}



def save_profile(profile):

    with open(
        PROFILE_PATH,
        "w"
    ) as file:

        json.dump(
            profile,
            file,
            indent=4
        )



def clear_profile():

    with open(
        PROFILE_PATH,
        "w"
    ) as file:

        json.dump(
            {},
            file,
            indent=4
        )
