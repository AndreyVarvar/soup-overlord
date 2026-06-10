from datetime import datetime
import pytz

UTC0 = pytz.timezone("Europe/London")



def log(message, timestamp: bool = True, log_to_file: bool = False):
    current_time = datetime.now(UTC0).strftime("[UTC+0 %A %d, %B %Y, %H:%M:%S]: ")

    
    _log = ''
    if timestamp:
        _log += current_time
    _log += message
    
    if log_to_file:
        CURRENT_LOG_FILE = "logs/" + datetime.now(UTC0).strftime("%d.%m.%y")

        with open(CURRENT_LOG_FILE, "a") as file:
            file.write(_log + "\n")
    
    print(_log)
