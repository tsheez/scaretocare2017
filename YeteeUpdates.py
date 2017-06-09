from bs4 import BeautifulSoup
import requests
from re import sub
from decimal import Decimal
import time

updateFreq = 30 #seconds
if __name__ == '__main__':
    while True:
        try:
            Tee1 = requests.get("http://theyetee.com/track_item.php?itemid=ScaretoCare-Scaretocare2017&code=J2Joe7NJ5ScDNpfm").text
            Pin = requests.get("http://theyetee.com/track_item.php?itemid=Scaretocare-pin&code=UAEfNYGUhcY0mhEY").text
            Tee2 = requests.get("http://theyetee.com/track_item.php?itemid=ScaretoCare-scaredycat&code=bOgd8sfKGwIggwhR").text

            urls = [Tee1,Tee2,Pin]

            index = "Total Unit Sales: <strong>"

            list = []
            for url in urls:
                front = url.find(index)+len(index)
                end = url.find("</strong>", front)
                list.append(int(url[front:end]))

            yeteeTotal = list[0]*3 +list[1]*3+list[2]*4
            print(yeteeTotal)

            outLoc = "C:\\Users\\tlsha\\Dropbox\\s2c\\realtotal.txt"
            outLoc2 = "C:\\Users\\tlsha\\Dropbox\\s2c\\shirts.txt"
            outLoc3 = "C:\\Users\\tlsha\\Dropbox\\s2c\\pins.txt"
            outLoc4 = "C:\\Users\\tlsha\\Dropbox\\s2c\\kidstocamp.txt"

            extraMoney = 3
            currentTotal = Decimal(sub(r'[^\d.]', '', open("C:\\Users\\tlsha\\Dropbox\\twitchalerts\\30day_donation_amount.txt").read().rstrip()))
            currentTotal+=extraMoney
            currentTotal+= yeteeTotal
            file = open(outLoc, 'w')
            file.write('${:,.2f}'.format(currentTotal))
            file.close()

            file = open(outLoc2, 'w')
            file.write("Shirts Sold: "+str(int(list[0]+list[1]))+"\n")
            file.write("Pins Sold: " + str(int(list[2])))
            file.close()

            file=open(outLoc4,'w')
            file.write(str(int(currentTotal/300)))
            file.close()


            time.sleep(updateFreq)
        except:
            print("Something is wrong, yo")
            time.sleep(5)
