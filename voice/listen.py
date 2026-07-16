import speech_recognition as sr


def listen():

    recognizer = sr.Recognizer()


    try:

        with sr.Microphone() as source:

            print("Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=5
            )


        text = recognizer.recognize_google(
            audio
        )


        return text


    except sr.WaitTimeoutError:

        return "I did not hear anything."


    except sr.UnknownValueError:

        return "I could not understand."


    except Exception as e:

        return f"Microphone error: {e}"