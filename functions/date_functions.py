from datetime import datetime as dt, timedelta

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


def daterange2(date1, date2, period, c):
    return [{"timestamp": d.strftime("%Y-%m-%d"),
             "type": period,
             "url": ''} for d in [date1 + timedelta(n) for n in range(int((date2 - date1).days) + 1)]
            if d not in c]

