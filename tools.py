import dateutil.parser
from datetime import datetime, timedelta
from re import sub
from decimal import Decimal
import random

begin = '2017-01-01T001:00:00+00:00'
def donationParser(inLoc, header=True):
    """Takes a donation csv formatted from twitch alerts. Returns a list of lists for each entry.
    0-Date (datetime object)
    1-Name
    2-Email
    3-Amount (Decimal type)
    4-Comment
    """
    donations=[]
    file =open(inLoc, 'r', encoding='latin1')
    for line in file:
        if header:
            header = False
            continue
        temp = []
        line=line.rstrip().split(',')

        try:
            temp.append(dateutil.parser.parse(line[0]).astimezone())

            temp.append(line[1])
            temp.append(line[2])
            temp.append(Decimal(sub(r'[^\d.]', '', line[3])))
            temp.append("".join(line[4:]))
            donations.append(temp)
        except:
            donations[-1][4]+=" ".join(line)
    return donations
def donationSlicer(donationList, start='', end=""):
    if start:
        start = dateutil.parser.parse(start)
    else:
        start = dateutil.parser.parse('2017-01-01T001:00:00+00:00') #beginning of S2C 2017
    if end:
        end = dateutil.parser.parse(end).astimezone()
    else:
        end = datetime.now().astimezone()

    newDonations = []

    for donation in donationList:
        if donation[0]>=start and donation[0]<=end:
            newDonations.append(donation)
    return newDonations
def blockWinner(donationList, start="", end=""):
    donations = donationSlicer(donationList,start=start,end=end)
    choiceList =[]
    for donation in donations:
        choiceList+=[donation]*int(donation[3])
    return random.choice(choiceList)
def topDonors(donationList, start="", end=""):
    donations=donationSlicer(donationList,start=start, end=end)
    donors={}
    for donation in donations:
        try:
            donors[donation[1]]+=donation[3]
        except:
            donors[donation[1]] = donation[3]
    return donors
def hashTagVote(donationList, hashTagList="",start="",end=""):
    if not hashTagList:
        hashTagList=["#A","#B"]


inLoc = "C:\\Users\\tlsha\\Desktop\\donations.csv"
donations=donationParser(inLoc)
print(blockWinner(donations, start="2016-06-10T22:39:37+00:00"))
print(topDonors(donations, start="2016-06-20T22:41:35+00:00"))


