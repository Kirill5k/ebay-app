from datetime import datetime, timedelta, timezone


class Date:
    def __init__(self) -> None:
        self.time = datetime.now(timezone.utc)

    def minus_minutes(self, minutes):
        self.time = self.time - timedelta(minutes=minutes)
        return self

    def minus_days(self, days):
        self.time = self.time - timedelta(days=days)
        return self

    def as_date(self):
        return self.time

    def as_iso(self):
        return self.time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
