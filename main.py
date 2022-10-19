import pdb
import string
from xmlrpc.client import DateTime
import requests
import os
from dotenv import load_dotenv
from ics import Calendar
from dataclasses import dataclass
from datetime import datetime, date
from dateutil import parser
import pytz

os.environ['TZ'] = 'America/Vancouver'


@dataclass
class Event:
    start: float
    location: string
    homeTeam: string
    awayTeam: string

    def __hash__(self) -> int:
        return hash(f"{self.start}{self.location}{self.homeTeam}{self.awayTeam}")

    @classmethod
    def from_ics(cls, ics):
        teams = ics.name.split(' vs. ')
        return Event(ics.begin.datetime.timestamp(), ics.location.split(' - ')[0], teams[1], teams[0])

    @classmethod
    def from_sno_king_site(cls, event):
        return Event(parser.parse(event['dateTime']).timestamp(), event['rinkName'], event['teamHomeName'], event['teamAwayName'])

    def __repr__(self) -> str:
        return f"{datetime.fromtimestamp(self.start)}: {self.homeTeam} vs {self.awayTeam} @ {self.location}"


load_dotenv()


def future_only(events_list):
    return [event for event in events_list if event.start > datetime.now().timestamp()]


def get_bench_app_events():
    cal_url = os.getenv("CALENDAR_URL")
    c = Calendar(requests.get(cal_url).text)
    bench_app_events = [Event.from_ics(event) for event in c.events]
    return future_only(bench_app_events)


def get_sno_king_events():
    all_events = []
    for season_id in get_season_ids():
        try:
            team_schedule_url = f"https://snokinghockeyleague.com/api/team/subSchedule/{season_id}/1075?v=1030940"
            games = requests.get(team_schedule_url).json()["games"]
            events = [Event.from_sno_king_site(game) for game in games]
            all_events += future_only(events)
        except Exception:
            # If team is not in season (I.E. Frost Giants don't play BEHL), we get a 500
            # I really should actually figure out if the team is in the season before I query but...
            # This entire script is a lazy hack so who cares if I'm a lazy hack in the script
            pass
    return all_events


def get_season_ids():
    seasons_url = "https://snokinghockeyleague.com/api/season/all/0?v=1030940"
    today_year = str(date.today().year)

    seasons = requests.get(seasons_url).json()["seasons"]
    current_seasons = [
        season for season in seasons if today_year in season["name"]]
    return [season["id"] for season in current_seasons]


print("BENCHAPP EVENTS")
bench_app_events = get_bench_app_events()
print(bench_app_events)
print("")
print("SNOKING EVENTS")
sno_king_events = get_sno_king_events()
print(sno_king_events)
print("")

set_ba = set(bench_app_events)
set_sk = set(sno_king_events)
if set_ba == set_sk:
    print("BenchApp and SnoKing site are in sync")
else:
    print("BenchApp and SnoKing site are not in sync")
    print()
    print("BenchApp, Not Site: ")
    print(set_ba - set_sk)
    print()
    print("Site, Not BenchApp: ")
    print(set_sk - set_ba)
    exit(1)
