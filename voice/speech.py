import subprocess
import threading


def speak(text):

    def run_speech():

        try:

            subprocess.run(
                [
                    "say",
                    text
                ],
                check=True
            )

        except Exception as e:

            print(
                "Speech error:",
                e
            )


    threading.Thread(
        target=run_speech,
        daemon=True
    ).start()
