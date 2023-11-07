from dataclasses import dataclass
from datetime import datetime, date
from dateutil import parser

@dataclass
class Event:
    start: float
    location: str
    homeTeam: str
    awayTeam: str

    def __hash__(self) -> int:
        return hash(f"{self.start}{self.location}{self.homeTeam}{self.awayTeam}")

    @classmethod
    def from_ics(cls, ics):
        teams = ics.name.split(' vs. ')
        return Event(ics.begin.datetime.timestamp(), ics.location.split(' - ')[0].replace('(', ''), Event.normalize_team_name(teams[1]), Event.normalize_team_name(teams[0]))

    @classmethod
    def from_sno_king_site(cls, event):
        return Event(parser.parse(event['dateTime']).timestamp(), event['rinkName'], Event.normalize_team_name(event['teamHomeName']), Event.normalize_team_name(event['teamAwayName']))

    def __repr__(self) -> str:
        return f"{datetime.fromtimestamp(self.start)}: {self.homeTeam} vs {self.awayTeam} @ {self.location}"

    @classmethod
    def normalize_team_name(cls, team):
        return team.replace("Shaved Ice: Tiger's Blood", "Tiger's Blood")

