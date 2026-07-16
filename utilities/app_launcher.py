import subprocess


apps = {

    "calculator": "Calculator",
    "browser": "Safari",
    "safari": "Safari",
    "notes": "Notes",
    "finder": "Finder",
    "terminal": "Terminal"

}


def open_app(app_name):

    app_name = app_name.lower()


    if app_name in apps:

        try:

            subprocess.Popen(
                [
                    "open",
                    "-a",
                    apps[app_name]
                ]
            )

            return f"Opening {apps[app_name]}..."


        except Exception as e:

            return f"Could not open app: {e}"


    return "I don't know that application."