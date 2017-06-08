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
        front = line.find("\"$")
        back = line.find(".", front)
        loc = line.find(",", front, back)
        if loc:
            line = list(line)
            line[loc] = ""
            line = "".join(line)

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
def topDonors(donationList, start="", end="", num=10, outLoc=''):
    donations=donationSlicer(donationList,start=start, end=end)
    donors={}
    for donation in donations:
        try:
            donors[donation[2].lower()][1]+=donation[3]
        except:
            donors[donation[2].lower()] = [donation[1],donation[3]]
    listOut=[]
    for item in list(donors.items()):
        listOut.append([item[1][0],item[1][1]])
    listOut = sorted(listOut,key=lambda x:x[1], reverse=True)
    listOut2 = []
    for key, value in listOut:
        listOut2.append([key,'${:,.2f}'.format(value)])
    if outLoc:
        file = open(outLoc,'w')
        for line in listOut2[:num]:
            file.write(line[0]+": "+line[1]+'\n')
    return listOut2[:num]
def hashTagVote(donationList, hashTagList="",start="",end="", outLoc=''):
    donations=donationSlicer(donationList)
    if not hashTagList:
        hashTagList=["#A","#B"]
    totals=[]
    for hashTag in hashTagList:
        temp=0
        for donation in donations:
            if hashTag.lower() in donation[4].lower():
                temp+=donation[3]
        temp = '${:,.2f}'.format(temp)
        totals.append(temp)
    outList= list(zip(hashTagList,totals))
    if outLoc:
        file = open(outLoc,'w')
        for line in outList:
            file.write(line[0]+": "+line[1]+'\n')

    return outList


inLoc = "C:\\Users\\tlsha\\Desktop\\donations.csv"
outLoc = "C:\\Users\\tlsha\\Dropbox\\s2c\\test.txt"
donations=donationParser(inLoc)
totals = hashTagVote(donations, outLoc=outLoc)



print(topDonors(donations, start="2015-01-01T001:00:00+00:00", outLoc=outLoc))


