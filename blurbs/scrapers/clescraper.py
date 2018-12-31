from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import urllib
from datetime import date

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response:
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)


def getLastSunday():
    today = date.today()
    if today.isoweekday == 7:
        return date.isoformat(today)
    elif today.isoweekday() == 1 or today.isoweekday() == 2 or today.isoweekday() == 3 or today.isoweekday() == 4 or today.isoweekday() == 5 or today.isoweekday():
        return date.isoformat(date.fromordinal(today.toordinal() - today.isoweekday()))
    else:
        return "Error"
        
def scrape():
  raw_html = simple_get(f'http://cdec.water.ca.gov/dynamicapp/QueryDaily?s=CLE&end={getLastSunday()}')
  html = BeautifulSoup(raw_html, 'html.parser')
  dataNodes = html.find_all("td", align="right")
  dataStrings = list(map(lambda x: x.string, dataNodes))
  slicedNodeList = [dataStrings[-96: -85], dataStrings[-84:-73], dataStrings[-72:-61], dataStrings[-60:-49], dataStrings[-48:-37], dataStrings[-36:-25], dataStrings[-24:-13], dataStrings[-12:]]
  return slicedNodeList

def getCleData():
    dataList = scrape()
    lastWkStorage = float(dataList[0][2].replace(',', ''))
    thisWkStorage = float(dataList[7][2].replace(',', ''))
    dataDict = {
    "mondayDate": dataList[1][0],
    "sundayDate": dataList[7][0],
    "lastSunStorage": dataList[0][2],
    "sundayStorage": dataList[7][2],
    "storageDirection": 'down' if lastWkStorage > thisWkStorage else 'up',
    "weeklyDifference": '{:,.2f}'.format(abs(int(lastWkStorage - thisWkStorage)))[:-3],
    "avgWkOutflow": '{:,.2f}'.format(getAvgWkOutflow(dataList))[:-3],
    "avgWkInflow": '{:,.2f}'.format(getAvgWkInflow(dataList))[:-3],
    }
    return dataDict

def getAvgWkOutflow(data):
    outflowData = []
    for index, day in enumerate(data[1:]):
        try:
            dayOutflow = float(day[4].replace(',', ''))
            outflowData.append(dayOutflow)
        except ValueError:
            if (index == 7):
                dayOutflow = float(data[6][4].replace(',', ''))
                outflowData.append(dayOutflow)
            else:
                dayBeforeOutflow = float(data[(index - 1)][4].replace(',', ''))
                dayAfterOutflow = float(data[(index + 1)][4].replace(',', ''))
                smudgedOutflow = ((dayBeforeOutflow + dayAfterOutflow) / 2)
                outflowData.append(smudgedOutflow)
    return int(sum(outflowData)/len(outflowData))

def getAvgWkInflow(data):
    inflowData = []
    for index, day in enumerate(data[1:]):
        try:
            dayInflow = float(day[5].replace(',', ''))
            inflowData.append(dayInflow)
        except ValueError:
            if (index == 7):
                dayInflow = float(data[6][5].replace(',', ''))
                inflowData.append(dayInflow)
            else:
                dayBeforeInflow = float(data[(index - 1)][5].replace(',', ''))
                dayAfterInflow = float(data[(index + 1)][5].replace(',',''))
                smudgedInflow = ((dayBeforeInflow + dayAfterInflow) / 2)
                inflowData.append(smudgedInflow)
    return int(sum(inflowData)/len(inflowData))