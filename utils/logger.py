from datetime import datetime

LOG_FILE = "logs/nova.log"


def write_log(user, response):

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    with open(LOG_FILE, "a") as file:

        file.write(f"[{now}]\n")

        file.write(f"You  : {user}\n")

        file.write(f"Nova : {response}\n")

        file.write("-" * 40 + "\n")