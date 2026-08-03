from datetime import datetime

def current_time():
  
  now = datetime.now()
  
  return now.strftime("%A %d %B %Y | %l:%M:%S %p")