import json
from datetime import datetime, timedelta
from urllib.request import urlopen
import pause
from time import sleep

import asvz_simulator
import enroll
from logger import print_or_log

WAITING_FOR_SIGNUP = 0
MONITORING_FOR_SLOTS = 1
SIGN_UP_SUCCESSFUL = 2
SIGN_UP_MISSED = 3
STATUS_PENDING = 4
ERROR_OCCURRED = 5

#just for testing with custom data
def get_infos_fake(lesson):
    data = asvz_simulator.getInfos(lesson)
    participantsMax = data.get('maxParticipants')
    participantCount = data.get('countParticipants')
    free_spots = participantsMax - participantCount
    enrollmentFrom = data.get('enroll_from')
    enrollmentUntil = data.get('enroll_until')
    enroll_from = datetime.strptime(enrollmentFrom, '%Y-%m-%dT%H:%M:%S%z')
    enroll_till = datetime.strptime(enrollmentUntil, '%Y-%m-%dT%H:%M:%S%z')
    print_or_log(f'got fake data for lesson {lesson}')
    return free_spots, enroll_from, enroll_till

def get_infos(lesson):
    print_or_log(f'id={lesson} in get_infos')
    api_url = 'https://schalter.asvz.ch/tn-api/api/Lessons/' + str(lesson)
    timestamp = str(datetime.now().timestamp() * 1000)[0:13]
    api_url = api_url + '?t=' + timestamp
    with urlopen(api_url) as response:
        response = json.loads(response.read().decode())

    participantsMax = response.get('data').get('participantsMax')
    participantCount = response.get('data').get('participantCount')
    free_spots = 1
    if participantsMax is not None and participantCount is not None:
        free_spots = participantsMax - participantCount
    enrollmentFrom = response.get('data').get('enrollmentFrom')
    enrollmentUntil = response.get('data').get('enrollmentUntil')
    enroll_from = datetime.strptime(enrollmentFrom, '%Y-%m-%dT%H:%M:%S%z')
    enroll_till = datetime.strptime(enrollmentUntil, '%Y-%m-%dT%H:%M:%S%z')
    return free_spots, enroll_from, enroll_till

def handle_lesson(session, model, lesson):
    print_or_log(f'id={lesson} in handle_lesson')
    try:
        free_spots, enroll_from, enroll_till = get_infos(lesson)
        now = datetime.now().astimezone()
        if now < enroll_from:
            print_or_log(f'option 1 {lesson}')
            hold(session, model, lesson, enroll_from)
        elif now < enroll_till:
            print_or_log(f'option 2 {lesson}')
            watch(session, model, lesson)
        else:
            print_or_log(f'option 3 {lesson}')
            give_up(session, model, lesson)
    except Exception as e:
        print_or_log(f'some error occurred in lesson {lesson}')
        print_or_log(e)
        model.query.filter_by(lesson_id=lesson).first().status = ERROR_OCCURRED
        session.commit()


def hold(session, model, lesson, enroll_time):
    print_or_log(f'id={lesson} in hold')
    model.query.filter_by(lesson_id=lesson).first().status = WAITING_FOR_SIGNUP
    session.commit()
    pause.until(enroll_time.replace(tzinfo=None)-timedelta(seconds=55))
    if model.query.filter_by(lesson_id=lesson).first() is not None:
        print_or_log(f'sending lesson {lesson} from hold to enroll')
        model.query.filter_by(lesson_id=lesson).first().status = SIGN_UP_SUCCESSFUL #TODO check this later
        enroll.enroll(lesson, enroll_time.replace(tzinfo=None)) 
        session.commit()
    else:
        print_or_log(f'id={lesson} deleted while in hold')

def watch(session, model, lesson):
    print_or_log(f'id={lesson} in watch')
    model.query.filter_by(lesson_id=lesson).first().status = MONITORING_FOR_SLOTS
    session.commit()
    while model.query.filter_by(lesson_id=lesson).first():
        free_spots, enroll_from, enroll_till = get_infos(lesson)
        if datetime.now().astimezone() >= enroll_till:
            print_or_log(f'id={lesson} has timed out in watch')
            give_up(session, model, lesson)
            return
        if free_spots > 0:
            print_or_log(f'id={lesson} has {free_spots} free spots in watch')
            model.query.filter_by(lesson_id=lesson).first().status = SIGN_UP_SUCCESSFUL #TODO check this later
            enroll.enroll(lesson, enroll_from.replace(tzinfo=None))
            session.commit()
            return
        sleep(60)
    print_or_log(f'id={lesson} deleted while in watch')

def give_up(session, model, lesson):
    print_or_log(f'id={lesson} in give_up')
    model.query.filter_by(lesson_id=lesson).first().status = SIGN_UP_MISSED
    session.commit()
