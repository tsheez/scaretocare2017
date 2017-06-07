import dateutil.parser
from datetime import datetime, timedelta
from re import sub
from decimal import Decimal


def donationParser(inLoc, header=True):
    """Takes a donation csv formatted from twitch alerts. Returns a list of lists for each entry.
    0-Date (datetime object)
    1-Name
    2-Email
    3-Amount (Decimal type)
    4-Comment
    """
    


begin = '2017-05-05T014:08:09+00:00'
x= dateutil.parser.parse(begin)
z = dateutil.parser.parse("6/1/17 2:24pm")

y = x-timedelta(hours=3)
print(x)
print(y.astimezone())
print(z)
print(datetime.now())