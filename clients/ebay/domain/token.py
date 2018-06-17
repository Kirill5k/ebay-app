from datetime import datetime, timedelta


class AccessToken:
    token: str
    time_created: datetime

    def __init__(self, token) -> None:
        self.token = token
        self.time_created = datetime.now()

    def is_expired(self) -> bool:
        return datetime.now() >= self.time_created + timedelta(hours=2)