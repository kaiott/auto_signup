import requests
from time import sleep
import asvz_simulator
from datetime import datetime, timedelta

BASE = 'http://95.217.133.138/'

def check_server_status():
    response = requests.get(BASE + 'status')
    try:
      print(response.json())
    except:
      if response.text == '':
        print(response.status_code)
      else:
        print(response.text)

def delete_all_entries():
    response = requests.delete(BASE + 'lessons')
    try:
      print(response.json())
    except:
      if response.text == '':
        print(response.status_code)
      else:
        print(response.text)

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
    add_lesson(lesson_id)
    sleep(1)
    retrieve_lesson(lesson_id)

def wait_until_signup(round_):
    now = datetime.now().astimezone()
    lesson_id = 600 + round_
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
    add_lesson(lesson_id)
    sleep(1)
    retrieve_lesson(lesson_id)

def full_and_timeout(round_):
    now = datetime.now().astimezone()
    lesson_id = 900 + round_
    add_lesson(lesson_id)
    sleep(1)
    retrieve_lesson(lesson_id)
    sleep(40)
    retrieve_lesson(lesson_id)
    sleep(40)
    retrieve_lesson(lesson_id)
    sleep(40)
    retrieve_lesson(lesson_id)

def test_on_fakes():
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


def real_test():
    check_server_status()
    add_lesson(174930) # body combat 09/02
    add_lesson(174938) # muscle pump 10/02

def main():
    #test_on_fakes()
    check_server_status()
    retrieve_all_lessons()
    delete_all_entries()
    retrieve_all_lessons()
    #real_test()

if __name__ == "__main__":
    main()