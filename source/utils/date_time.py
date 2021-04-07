from datetime import datetime, timedelta


class DateTime:

    @classmethod
    def current_datetime(cls) -> datetime:
        return datetime.utcnow()

    @classmethod
    def expiration_date(cls, minutes: int = 0, hours: int = 0) -> datetime:
        return cls.current_datetime() + timedelta(minutes=minutes, hours=hours)
