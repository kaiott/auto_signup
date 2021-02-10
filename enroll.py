import requests
import pause
from datetime import datetime, timedelta
from pprint import pprint
from logger import print_or_log
import time

def enroll(lesson, enroll_time):
    with open('/var/www/FlaskApp/FlaskApp/token') as file:
        access_token = file.read()
    timestamp = str(datetime.now().timestamp()*1000)[0:13]
    url = f'https://schalter.asvz.ch/tn-api/api/Lessons/{lesson}/enroll??t={timestamp}'
    headers = {
        'Host': 'schalter.asvz.ch',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'https://schalter.asvz.ch',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': f'https://schalter.asvz.ch/tn/lessons/{lesson}',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Length': '2'
    }
    print_or_log(f'id={lesson} has url {url}')
    pause.until(enroll_time-timedelta(milliseconds = 10))
    for i in range(10):
        try:
            print_or_log(f'id={lesson} sending request')
            requests.post(url, headers = headers, timeout = 0.2)
        except requests.exceptions.ReadTimeout:
            print_or_log(f'id={lesson} deliberate timeout')
            pass

    print_or_log(f'id={lesson} done, waiting 15 seconds')
    time.sleep(15)
    try:
        return check_enrollment(lesson)
    except Exception as e:
        print_or_log(f'id={lesson} failed {str(e)}')
        return False


def check_enrollment(lesson):
    with open('/var/www/FlaskApp/FlaskApp/token') as file:
        access_token = file.read()
    timestamp = str(datetime.now().timestamp()*1000)[0:13]
    url = f'https://schalter.asvz.ch/tn-api/api/Lessons/{lesson}/MyEnrollment??t={timestamp}'
    headers = {
        'Host': 'schalter.asvz.ch',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'Origin': 'https://schalter.asvz.ch',
        'Referer': f'https://schalter.asvz.ch/tn/lessons/{lesson}',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'DNT': '1'
    }
    print_or_log(f'id={lesson} trying to check enrollment')
    response = requests.get(url, headers = headers)
    print_or_log(f'id={lesson} got response {str(response)}')
    if response.status_code == 404:
        return False
    elif response.status_code == 500:
        return False
    return True
