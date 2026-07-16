import threading


def run_in_background(function, callback):

    def task():

        result = function()

        callback(result)


    thread = threading.Thread(
        target=task,
        daemon=True
    )

    thread.start()