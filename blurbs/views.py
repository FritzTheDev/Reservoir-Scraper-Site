from django.shortcuts import render
from blurbs.scrapers.shascraper import getShaData
from blurbs.scrapers.oroscraper import getOroData
from blurbs.scrapers.clescraper import getCleData
from blurbs.scrapers.milscraper import getMilData
from blurbs.scrapers.nmlscraper import getNmlData
from blurbs.scrapers.folscraper import getFolData

# Create your views here.
def index(request):
  return render(request, 'blurbs/index.html')

def sha(request):
  context = getShaData()
  sundayStorageInt = int(float(context["sundayStorage"].replace(',', '')))
  lastSunStorageInt = int(float(context["lastSunStorage"].replace(',', '')))
  context["totalCapacityString"] = '4,552,100'
  context["totalCapacity"] = 4552100
  context["sundayPctCap"] = str(
      100 * round(sundayStorageInt / context["totalCapacity"], 2))[:2]
  context["lastSunPctCap"] = str(
      100 * round(lastSunStorageInt / context["totalCapacity"], 2))[:2]
  context["weeklyPctDifference"] = abs(
      int(context["sundayPctCap"]) - int(context["lastSunPctCap"]))
  context["name"] = "Shasta Lake"
  return render(request, 'blurbs/reservoir.html', context)


def oro(request):
  context = getOroData()
  sundayStorageInt = int(float(context["sundayStorage"].replace(',', '')))
  lastSunStorageInt = int(float(context["lastSunStorage"].replace(',', '')))
  context["totalCapacityString"] = '3,538,000'
  context["totalCapacity"] = 3538000
  context["sundayPctCap"] = str(
      100 * round(sundayStorageInt / context["totalCapacity"], 2))[:2]
  context["lastSunPctCap"] = str(
      100 * round(lastSunStorageInt / context["totalCapacity"], 2))[:2]
  context["weeklyPctDifference"] = abs(
      int(context["sundayPctCap"]) - int(context["lastSunPctCap"]))
  context["name"] = "Lake Oroville"
  return render(request, 'blurbs/reservoir.html', context)


def cle(request):
  context = getCleData()
  sundayStorageInt = int(float(context["sundayStorage"].replace(',', '')))
  lastSunStorageInt = int(float(context["lastSunStorage"].replace(',', '')))
  context["totalCapacityString"] = '2,447,650'
  context["totalCapacity"] = 2447650
  context["sundayPctCap"] = str(
      100 * round(sundayStorageInt / context["totalCapacity"], 2))[:2]
  context["lastSunPctCap"] = str(
      100 * round(lastSunStorageInt / context["totalCapacity"], 2))[:2]
  context["weeklyPctDifference"] = abs(
      int(context["sundayPctCap"]) - int(context["lastSunPctCap"]))
  context["name"] = "Trinity Lake"
  return render(request, 'blurbs/reservoir.html', context)


def mil(request):
  context = getMilData()
  sundayStorageInt = int(float(context["sundayStorage"].replace(',', '')))
  lastSunStorageInt = int(float(context["lastSunStorage"].replace(',', '')))
  context["totalCapacityString"] = '520,500'
  context["totalCapacity"] = 520500
  context["sundayPctCap"] = str(
      100 * round(sundayStorageInt / context["totalCapacity"], 2))[:2]
  context["lastSunPctCap"] = str(
      100 * round(lastSunStorageInt / context["totalCapacity"], 2))[:2]
  context["weeklyPctDifference"] = abs(
      int(context["sundayPctCap"]) - int(context["lastSunPctCap"]))
  context["name"] = "Millerton Lake"
  return render(request, 'blurbs/reservoir.html', context)


def nml(request):
  context = getNmlData()
  sundayStorageInt = int(float(context["sundayStorage"].replace(',', '')))
  lastSunStorageInt = int(float(context["lastSunStorage"].replace(',', '')))
  context["totalCapacityString"] = '2,420,000'
  context["totalCapacity"] = 2420000
  context["sundayPctCap"] = str(
      100 * round(sundayStorageInt / context["totalCapacity"], 2))[:2]
  context["lastSunPctCap"] = str(
      100 * round(lastSunStorageInt / context["totalCapacity"], 2))[:2]
  context["weeklyPctDifference"] = abs(
      int(context["sundayPctCap"]) - int(context["lastSunPctCap"]))
  context["name"] = "New Melones"
  return render(request, 'blurbs/reservoir.html', context)


def fol(request):
  context = getFolData()
  sundayStorageInt = int(float(context["sundayStorage"].replace(',', '')))
  lastSunStorageInt = int(float(context["lastSunStorage"].replace(',', '')))
  context["totalCapacityString"] = '977,000'
  context["totalCapacity"] = 977000
  context["sundayPctCap"] = str(
      100 * round(sundayStorageInt / context["totalCapacity"], 2))[:2]
  context["lastSunPctCap"] = str(
      100 * round(lastSunStorageInt / context["totalCapacity"], 2))[:2]
  context["weeklyPctDifference"] = abs(
      int(context["sundayPctCap"]) - int(context["lastSunPctCap"]))
  context["name"] = "Folsom Lake"
  return render(request, 'blurbs/reservoir.html', context)
