from datetime import datetime
import pytz

UTC0 = pytz.timezone("Europe/London")



def log(message):
    current_time = datetime.now(UTC0).strftime("[UTC+0 %A %d, %B %Y, %H:%M:%S]: ")

    CURRENT_LOG_FILE = "logs/" + datetime.now(UTC0).strftime("%d.%m.%y")
    try:
        f = open(CURRENT_LOG_FILE, 'x')
        f.close()
    except FileExistsError:
        pass
    
    message = (current_time + message) if message != "\n" else message
    with open(CURRENT_LOG_FILE, "a") as file:
        file.write(message + "\n")
        print(message)
