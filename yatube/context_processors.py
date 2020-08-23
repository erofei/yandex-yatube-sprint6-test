import datetime as dt


def year(request):
    date = dt.datetime.today()
    return {'year': date.year}