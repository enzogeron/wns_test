from datetime import date, datetime, timedelta


def validate_date_last_30_days(date_str: str) -> None:
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    today = date.today()
    if d > today:
        raise ValueError("date cannot be in the future")
    if d < today - timedelta(days=30):
        raise ValueError("date must be within the last 30 days")
    