import datetime

def log(message):
  now = datetime.datetime.now()
  timestamp = now.strftime("%H:%M:%S")
  print(f"{timestamp} - {message}")