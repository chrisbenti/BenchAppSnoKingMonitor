from datetime import datetime, date

class EventGrabber:
    @classmethod
    def future_only(cls, events_list):
        return [event for event in events_list if event.start > datetime.now().timestamp()]
