from tools import blockWinner, donationParser
import os, glob

if __name__ == '__main__':
    start = ''
    end = ''

    #Get latest file in download folder
    list_of_files = glob.glob('C:\\Users\\tlsha\\Downloads\\*.csv')
    latest_file = max(list_of_files, key=os.path.getctime)
    latest_file
    donations = donationParser(latest_file)

    print(blockWinner(donations, start=start, end=end))