import psutil


def get_system_status():

    cpu = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()

    ram = memory.percent


    battery = psutil.sensors_battery()


    if battery:

        battery_info = (
            f"Battery: {battery.percent}%\n"
            f"Charging: {battery.power_plugged}"
        )

    else:

        battery_info = "Battery information unavailable."


    return (
        f"CPU Usage: {cpu}%\n"
        f"RAM Usage: {ram}%\n"
        f"{battery_info}"
    )