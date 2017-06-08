import dateutil.parser
from datetime import datetime, timedelta
from re import sub
from decimal import Decimal
import random, glob, os, time
import selenium


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
        start = dateutil.parser.parse(start).astimezone()
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


#Enter arbitrary number of options for voting
hashtags = ["#OptionA","#OptionB","#OptionC"]
#start time to begin looking at. Use 1/1/17 5pm format. Empty defaults to beginning of s2c 2017
start = '1/1/14 1pm'
#end time to begin looking at. Empty defaults to current.
end = ''

updateFrequency= 10 #seconds
cleanupFrequency=200 #times sleep seconds



flag=cleanupFrequency
while True:
    flag-=1
    try:


        #Files that OBS will use as a source
        outLoc1 = "C:\\Users\\tlsha\\Dropbox\\s2c\\hashvote.txt"
        outLoc2 = "C:\\Users\\tlsha\\Dropbox\\s2c\\blockdonors.txt"

        #Get latest file in download folder
        list_of_files = glob.glob('C:\\Users\\tlsha\\Downloads\\*.csv')
        latest_file = max(list_of_files, key=os.path.getctime)
        inLoc = latest_file

        donations=donationParser(inLoc)
        totals = hashTagVote(donations, hashTagList=hashtags,start = start, end=end, outLoc=outLoc1)
        tops = topDonors(donations, start =start, end=end, outLoc=outLoc2)
        print(totals)
        print(tops)
        time.sleep(updateFrequency)
    except:
        print("Things aren't working. Make sure donation thing exists in downloads. Wait for 5 minutes until new CSV is downloaded")
        time.sleep(updateFrequency)
        flag = cleanupFrequency
        continue
    if not flag:
        files = glob.glob('C:\\Users\\tlsha\\Downloads\\donations*')
        for file in files:
            os.remove(file)
        print("Cleaned up Files")
        flag = cleanupFrequency



