from lxml import html
import requests
import xml.etree.ElementTree as et
from datetime import datetime
from time import time, sleep
import schedule
import numpy as np
import csv
import sys

# have parameters interval and duration, and name file using date and parameters
# wrap in error handling

interval = int(sys.argv[1])
duration = int(sys.argv[2])

def getstate():
    page = requests.get('http://insolation.physics.carleton.edu/stateFull.xml')
    root = et.fromstring(page.content)
    state = [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(int(time())),
            str(float(root[0].text)), str(float(root[1].text)), str(float(root[2].text)),
            str(float(root[3].text)), str(float(root[4].text)), str(float(root[5].text)),
            str(float(root[6].text)), str(float(root[7].text))]
    return state

starttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
startepoch = int(time())

myData = [["Date/Time","Epoch","V1","V2","V3","T1","T2","T3","T4","Sol"]]

myFile = open(starttime+'.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(myData)

    def job():
        newData = [getstate()]
        writer = csv.writer(myFile)
        writer.writerows(newData)
        if (int(time()) > int(startepoch + duration)):
            return quit()

    schedule.every(interval).seconds.do(job)

    while True:
        schedule.run_pending()
        sleep(1)
