from datetime import datetime, date
import requests
from event import Event
from eventGrabber import EventGrabber

class SnoKing(EventGrabber):
    @classmethod
    def get_sno_king_events(cls, seasons_url, season_url):
        all_events = []
        for season_id in cls.get_season_ids(seasons_url):
            games = None
            try:
                team_schedule_url = season_url.format(season_id=season_id)
                games = requests.get(team_schedule_url).json()["games"]
            except Exception:
                # If team is not in season (I.E. Frost Giants don't play BEHL), we get a 500
                # I really should actually figure out if the team is in the season before I query but...
                # This entire script is a lazy hack so who cares if I'm a lazy hack in the script
                pass
            if games is not None:
                events = [Event.from_sno_king_site(game) for game in games]
                all_events += cls.future_only(events)
        return all_events

    @classmethod
    def get_season_ids(cls, seasons_url):
        today_year = str(date.today().year)
        last_year = str(date.today().year - 1)

        seasons = requests.get(seasons_url).json()["seasons"]
        current_seasons = [
            season for season in seasons if today_year in season["name"] or last_year in season["name"]]
        ids = [season["id"] for season in current_seasons]
        return ids
