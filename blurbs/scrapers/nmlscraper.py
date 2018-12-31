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
  raw_html = simple_get(f'http://cdec.water.ca.gov/dynamicapp/QueryDaily?s=NML&end={getLastSunday()}')
  html = BeautifulSoup(raw_html, 'html.parser')
  dataNodes = html.find_all("td", align="right")
  dataStrings = list(map(lambda x: x.string, dataNodes))
  slicedNodeList = [dataStrings[-112: -99], dataStrings[-98:-85], dataStrings[-84:-71], dataStrings[-70:-57], dataStrings[-56:-43], dataStrings[-42:-29], dataStrings[-28:-15], dataStrings[-14:]]
  return slicedNodeList

def getNmlData():
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
            dayOutflow = float(day[6].replace(',', ''))
            outflowData.append(dayOutflow)
        except ValueError:
            if (index == 7):
                dayOutflow = float(data[6][6].replace(',', ''))
                outflowData.append(dayOutflow)
            else:
                dayBeforeOutflow = float(data[(index - 1)][6].replace(',', ''))
                dayAfterOutflow = float(data[(index + 1)][6].replace(',', ''))
                smudgedOutflow = ((dayBeforeOutflow + dayAfterOutflow) / 2)
                outflowData.append(smudgedOutflow)
    return int(sum(outflowData)/len(outflowData))

def getAvgWkInflow(data):
    inflowData = []
    for index, day in enumerate(data[1:]):
        try:
            dayInflow = float(day[7].replace(',', ''))
            inflowData.append(dayInflow)
        except ValueError:
            if (index == 7):
                dayInflow = float(data[6][7].replace(',', ''))
                inflowData.append(dayInflow)
            else:
                dayBeforeInflow = float(data[(index - 1)][7].replace(',', ''))
                dayAfterInflow = float(data[(index + 1)][7].replace(',',''))
                smudgedInflow = ((dayBeforeInflow + dayAfterInflow) / 2)
                inflowData.append(smudgedInflow)
    return int(sum(inflowData)/len(inflowData))