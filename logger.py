from datetime import datetime
LOG = True
PRINT = False
LOG_FILE = '/var/www/FlaskApp/FlaskApp/log.txt'

def print_or_log(message, log_=LOG, print_=PRINT):
    if log_:
        write_log(message)
    if print_:
        print(message)

def write_log(message):
    with open(LOG_FILE, 'a') as file:
        file.write(f"{datetime.now().strftime('%H:%M:%S %Y-%m-%d')} {message}\n")
