from datetime import datetime, timedelta
from logger import print_or_log
lessons = {1: {"name": "Salsa", 
               "enroll_from": "2021-04-11T12:15:00+02:00",
               "enroll_until": "2021-04-12T10:15:00+02:00",
               "starts": "2021-04-12T12:15:00+02:00",
               "ends": "2021-04-12T14:00:00+02:00",
               "maxParticipants": 25,
               "countParticipants": 24},
           2: {"name": "Body Combat", 
               "enroll_from": "2021-04-12T18:00:00+02:00",
               "enroll_until": "2021-04-13T16:00:00+02:00",
               "starts": "2021-04-13T18:00:00+02:00",
               "ends": "2021-04-13T18:55:00+02:00",
               "maxParticipants": 25,
               "countParticipants": 25},
           3: {"name": "Salsa", 
               "enroll_from": "2021-04-14T19:15:00+02:00",
               "enroll_until": "2021-04-15T17:15:00+02:00",
               "starts": "2021-04-15T19:15:00+02:00",
               "ends": "2021-04-15T21:00:00+02:00",
               "maxParticipants": 15,
               "countParticipants": 0},
           4: {"name": "Salsa", 
               "enroll_from": "2021-04-18T12:15:00+02:00",
               "enroll_until": "2021-04-19T10:15:00+02:00",
               "starts": "2021-04-19T12:15:00+02:00",
               "ends": "2021-04-19T14:00:00+02:00",
               "maxParticipants": 25,
               "countParticipants": 0},
           }

i = 3
j = 0
def getInfos(lesson_id):
  print_or_log(f'in simulator for lesson {lesson_id}')
  t = lesson_id // 100
  print_or_log(f'following type {t}')
  now = datetime.now().astimezone()
  if t == 5:
    return {"name": "Salsa", 
           "enroll_from": (now-timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "enroll_until": (now+timedelta(hours=23)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "starts": (now+timedelta(hours=25)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "ends": "2021-04-15T21:00:00+02:00",
           "maxParticipants": 15,
           "countParticipants": 12}
  elif t == 6:
    return {"name": "Salsa", 
           "enroll_from": (now+timedelta(minutes=2)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "enroll_until": (now+timedelta(hours=22, minutes=2)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "starts": (now+timedelta(hours=24, minutes=2)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "ends": "2021-04-15T21:00:00+02:00",
           "maxParticipants": 15,
           "countParticipants": 0}
  elif t == 7:
    global i
    i -= 1
    return {"name": "Salsa", 
           "enroll_from": (now-timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "enroll_until": (now+timedelta(hours=23)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "starts": (now+timedelta(hours=25)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "ends": "2021-04-15T21:00:00+02:00",
           "maxParticipants": 15,
           "countParticipants": 12 if i == 0 else 15}
  elif t == 8:
    return {"name": "Salsa", 
           "enroll_from": (now-timedelta(hours=23)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "enroll_until": (now-timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "starts": (now+timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "ends": "2021-04-15T21:00:00+02:00",
           "maxParticipants": 15,
           "countParticipants": 12}
  elif t == 9:
    global j
    j += 1
    return {"name": "Salsa", 
           "enroll_from": (now-timedelta(hours=23)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "enroll_until": (now+timedelta(minutes=2-j)).strftime('%Y-%m-%dT%H:%M:%S%z'), #cannot be tested, every enw check will ive a new due date..
           "starts": (now+timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S%z'),
           "ends": "2021-04-15T21:00+02:00",
           "maxParticipants": 15,
           "countParticipants": 15}
  else:
    return lessons[lesson_id]

