# import pdb
# import string
# from xmlrpc.client import DateTime
# import requests
# from ics import Calendar

# import pytz

# from event import Event

import os
from bench_app import BenchApp
os.environ['TZ'] = 'America/Vancouver'
from SnoKing import SnoKing

from dotenv import load_dotenv
load_dotenv()

CONFIG = [
    {
        'name': "Frost Giants",
        'ba': "https://ics.benchapp.com/eyJwbGF5ZXJJZCI6NjMwODYsInRlYW1JZCI6WzgwNzUzXX0",
        'snoking': {
            'seasons': 'https://snokinghockeyleague.com/api/season/all/0?v=1030940',
            'season': 'https://snokinghockeyleague.com/api/team/subSchedule/{season_id}/1075?v=1030940"'
        },
    },
    #     {
    #     'name': "Frost Mites",
    #     'ba': "https://ics.benchapp.com/eyJwbGF5ZXJJZCI6NjMwODYsInRlYW1JZCI6Wzg1Njk4Nl19",
    #     'snoking': {
    #         'seasons': 'http://snokingpondhockey.com/api/season/all/0?v=1030940',
    #         'season': 'http://snokingpondhockey.com/api/team/subSchedule/{season_id}/2865?v=1030940"'
    #     },
    # }
]

exit_code = 0
for team in CONFIG:
    print(team['name'])

    print("BENCHAPP EVENTS")
    bench_app_events = BenchApp.get_bench_app_events(team['ba'])
    print(bench_app_events)
    print("")

    print("SNOKING EVENTS")
    sno_king_events = SnoKing.get_sno_king_events(team['snoking']['seasons'], team['snoking']['season'])
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
        exit_code = 1

exit(exit_code)