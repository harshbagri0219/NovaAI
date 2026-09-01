from datetime import datetime

def current_time():
    now = datetime.now()
    return now.strftime("%A %d %B %Y | %I:%M:%S %p")