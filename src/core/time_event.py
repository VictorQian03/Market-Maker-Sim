from core.event import Event

class TimeEvent(Event):
    def __init__(self, timestamp):
        super().__init__(timestamp)