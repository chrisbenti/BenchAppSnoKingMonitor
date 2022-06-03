import pdb
import string
from xmlrpc.client import DateTime
from numpy import number
import requests
import os
from dotenv import load_dotenv
from ics import Calendar
from dataclasses import dataclass
from datetime import datetime
from dateutil import parser


@dataclass
class Event:
    start: number
    location: string
    homeTeam: string
    awayTeam: string

    @classmethod
    def from_ics(cls, ics):
        teams = ics.name.split(' vs. ')
        return Event(ics.begin.datetime.timestamp(), ics.location.split(' - ')[0], teams[1], teams[0])

    @classmethod
    def from_sno_king_site(cls, event):
        return Event(parser.parse(event['dateTime']).timestamp(), event['rinkName'], event['teamHomeName'], event['teamAwayName'])


load_dotenv()


def future_only(events_list):
    return [event for event in events_list if event.start > datetime.now().timestamp()]


def get_bench_app_events():
    cal_url = os.getenv("CALENDAR_URL")
    c = Calendar(requests.get(cal_url).text)
    bench_app_events = [Event.from_ics(event) for event in c.events]
    return future_only(bench_app_events)


def get_sno_king_events():
    team_schedule_url = 'https://snokinghockeyleague.com/api/team/subSchedule/1079/1075?v=1030940'
    games = requests.get(team_schedule_url).json()["games"]
    sno_king_events = [Event.from_sno_king_site(game) for game in games]
    return future_only(sno_king_events)


print("BENCHAPP EVENTS")
print(get_bench_app_events())
print("")
print("SNOKING EVENTS")
print(get_sno_king_events())
