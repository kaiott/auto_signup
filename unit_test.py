import requests
from time import sleep
import asvz_simulator
from datetime import datetime, timedelta

BASE = 'http://95.217.133.138/'

def add_lesson(lesson_id):
    try:
        requests.put(BASE + f'lessons/{lesson_id}', timeout = 0.5)
    except requests.exceptions.ReadTimeout:
        pass

def retrieve_all_lessons():
    response = requests.get(BASE + "lessons")
    try:
      print(response.json())
    except:
      if response.text == '':
        print(response.status_code)
      else:
        print(response.text)

def retrieve_lesson(lesson_id):
    response = requests.get(BASE + f"lessons/{lesson_id}")
    try:
      print(response.json())
    except:
      if response.text == '':
        print(response.status_code)
      else:
        print(response.text)

def delete_lesson(lesson_id):
    response = requests.delete(BASE + f"lessons/{lesson_id}")
    print(response.status_code)

def direct_signup(round_):
    now = datetime.now().astimezone()
    lesson_id = 500 + round_
    data = {"name": "Salsa", 
           "enroll_from": (now-timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "enroll_until": (now+timedelta(hours=23)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "starts": (now+timedelta(hours=25)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "ends": "2021-04-15T21:00+02:00",
           "maxParticipants": 15,
           "countParticipants": 12}
    add_lesson(lesson_id)
    sleep(1)
    retrieve_lesson(lesson_id)

def wait_until_signup(round_):
    now = datetime.now().astimezone()
    lesson_id = 600 + round_
    data = {"name": "Salsa", 
           "enroll_from": (now+timedelta(minutes=2)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "enroll_until": (now+timedelta(hours=22, minutes=2)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "starts": (now+timedelta(hours=24, minutes=2)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "ends": "2021-04-15T21:00+02:00",
           "maxParticipants": 15,
           "countParticipants": 0}
    add_lesson(lesson_id)
    sleep(40)
    retrieve_lesson(lesson_id)
    sleep(40)
    retrieve_lesson(lesson_id)
    sleep(40)
    retrieve_lesson(lesson_id)

def wait_for_free_spots(round_):
    now = datetime.now().astimezone()
    lesson_id = 700 + round_
    data = {"name": "Salsa", 
           "enroll_from": (now-timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "enroll_until": (now+timedelta(hours=23)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "starts": (now+timedelta(hours=25)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "ends": "2021-04-15T21:00+02:00",
           "maxParticipants": 15,
           "countParticipants": 15}
    add_lesson(lesson_id)
    retrieve_lesson(lesson_id)
    sleep(40)
    retrieve_lesson(lesson_id)
    sleep(40)
    retrieve_lesson(lesson_id)
    sleep(40)
    retrieve_lesson(lesson_id)

def directly_too_late(round_):
    now = datetime.now().astimezone()
    lesson_id = 800 + round_
    data = {"name": "Salsa", 
           "enroll_from": (now-timedelta(hours=23)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "enroll_until": (now-timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "starts": (now+timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "ends": "2021-04-15T21:00+02:00",
           "maxParticipants": 15,
           "countParticipants": 12}
    add_lesson(lesson_id)
    sleep(1)
    retrieve_lesson(lesson_id)

def full_and_timeout(round_):
    now = datetime.now().astimezone()
    lesson_id = 900 + round_
    data = {"name": "Salsa", 
           "enroll_from": (now-timedelta(hours=23)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "enroll_until": (now+timedelta(minutes=2)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "starts": (now+timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "ends": "2021-04-15T21:00+02:00",
           "maxParticipants": 15,
           "countParticipants": 15}
    add_lesson(lesson_id)
    sleep(1)
    retrieve_lesson(lesson_id)
    sleep(40)
    retrieve_lesson(lesson_id)
    sleep(40)
    retrieve_lesson(lesson_id)
    sleep(40)
    retrieve_lesson(lesson_id)


def main():
    round_ = 3
    retrieve_all_lessons()
    delete_lesson(601)
    retrieve_all_lessons()
    direct_signup(round_)
    wait_until_signup(round_)
    wait_for_free_spots(round_)
    directly_too_late(round_)
    full_and_timeout(round_)
    retrieve_all_lessons()

if __name__ == "__main__":
    main()