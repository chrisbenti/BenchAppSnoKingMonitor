import os

from ics import Calendar
import requests

from event import Event
from eventGrabber import EventGrabber


class BenchApp(EventGrabber):
    @classmethod
    def get_bench_app_events(cls, cal_url):
        c = Calendar(requests.get(cal_url).text)
        bench_app_events = [Event.from_ics(
            event) for event in c.events if not event.name.startswith('Practice')]
        return cls.future_only(bench_app_events)
