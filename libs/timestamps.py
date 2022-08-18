from datetime import timedelta, datetime

from pytz import timezone


def dt_as_friendly_str(dt, to_tz=None):
    if to_tz:
        dt = dt_in_tz(dt, from_tz=dt.tzname() or 'UTC', to_tz=to_tz)
    dt_now = now(tz=to_tz or 'UTC')
    if dt.date() == dt_now.date():
        date = 'сегодня'
    elif dt.date() - dt_now.date() == timedelta(days=1):
        date = 'завтра'
    elif dt.date() - dt_now.date() == timedelta(days=2):
        date = 'послезавтра'
    elif dt_now.date() - dt.date() == timedelta(days=1):
        date = 'вчера'
    elif dt_now.date() - dt.date() == timedelta(days=2):
        date = 'позавчера'
    else:
        date = dt.strftime('%d.%m.%Y')
    timepoint = dt.strftime(f"%H:%M ") + date
    return timepoint


def dt_in_tz(dt, from_tz='UTC', to_tz='UTC'):
    if dt.tzinfo is None:
        dt = apply_tz(dt, from_tz)
    return dt.astimezone(timezone(to_tz))


def apply_tz(dt, tz='UTC'):
    return timezone(tz).localize(dt)


def now(tz='UTC'):
    return timezone('UTC').localize(datetime.utcnow()).astimezone(timezone(tz))


def dt_as_unix(dt, from_tz='UTC'):
    dt = dt_in_tz(dt, from_tz=from_tz, to_tz='UTC')
    return int((dt - apply_tz(datetime(1970, 1, 1))).total_seconds() * 1000)


def unix_as_dt(unix_in_seconds):
    return apply_tz(datetime(1970, 1, 1)) + timedelta(seconds=int(unix_in_seconds))


def str_date_as_date(date: str):
    return datetime.strptime(date, '%d %B %Y').date()


def badformed_date_as_date(date: str):
    return datetime.strptime(date, '%Y-%m-%d').date()


def datetime_as_datetime(date: str):
    return datetime.strptime(date, '%d %B %Y %H:%M')


def date_as_str_date(date: datetime):
    return datetime.strftime(date, '%d.%m.%Y')


def month_as_ru(month: int):
    return ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'][month - 1]
