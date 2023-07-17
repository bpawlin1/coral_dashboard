from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from datetime import date, datetime, timedelta
from dashboard.models import apexMeasurments
from django.contrib.auth.models import User


def parse_measurment():
    try:
        xml = parseXML()
        alk = xml[0]
        calc = xml[1]
        mag = xml[2]
        temp = xml[3]
        ph = xml[4]

    except Exception as e:
        print("Failed to parse")
    try:
        print('start')
        print(temp)
        print(ph)
        print(alk)
        print(calc)
        print(mag)

        apexMeasurments.objects.create(
            temp=float(temp),
            ph=float(ph),
            alk=float(alk),
            calc=int(calc),
            mag=int(mag))
    except Exception as e:
        print("Failed to create measurment object")


def index(request):
    xml = parseXML()
    alk = xml[0]
    calc = xml[1]
    mag = xml[2]
    temp = xml[3]
    ph = xml[4]
    # curDate = xml[5]
    # curTime = xml[6]

    currTime = datetime.now() - timedelta(minutes=10)
    currTimeFormated = currTime.strftime("%H:%M %p")
    currDate = date.today().strftime('%Y-%m-%d')

    dosingAlk = calc_alk(xml[0])
    dosingCalc = calc_calc(xml[1])
    dosingMag = calc_mag(xml[2])
    print(xml)

    context = {
        'alkDose': dosingAlk,
        'calcDose': dosingCalc,
        'magDose': dosingMag,
        'alk': alk,
        'calc': calc,
        'mag': mag,
        'temp': temp,
        'ph': ph,
        'curDate': currDate,
        'curTime': currTimeFormated
    }
    return render(request, 'dashboard.html', context=context)


def parseXML():

    currTime = datetime.now() - timedelta(minutes=10)
    print(currTime)
    currTimeFormated = currTime.strftime("%H%M")
    currDate = date.today().strftime('%y%m%d')

    url = 'http://192.168.0.10:80/cgi-bin/datalog.xml?sdate=' + \
        currDate + currTimeFormated
    print(url)
    # url = urllib.parse.quote(urlText, safe='')

    resp = requests.get(url)

    soup = BeautifulSoup(resp.text, "html.parser")

    values = []
    for record in soup.findAll('record'):
        for probe in record.findAll('probe'):
            for name in probe.find('value'):
                values.append(name)

    try:
        temp = values[0]
        ph = values[1]
        alk = values[-3]
        calc = values[-2]
        mag = values[-1]

    except Exception as e:
        print("Dang it")

    return alk, calc, mag, temp, ph, currDate, currTimeFormated


def calc_alk(curAlk):
    desiredAlk = 8.0 / 2.8
    currentAlk = float(curAlk) / 2.8
    volume = 100
    DosingAlk = 0

    DosingAlk = (1 / 0.5) * (desiredAlk - currentAlk) * volume

    return round(DosingAlk, 2)


def calc_calc(curCalc):
    desiredCalc = 440
    currentCalc = float(curCalc)
    volume = 100
    DosingCalc = 0

    DosingCalc = (1 / 9.77) * (desiredCalc - currentCalc) * volume

    return round(DosingCalc, 2)


def calc_mag(curMag):
    desiredMag = 1400
    currentMag = float(curMag)
    volume = 100
    DosingMag = 0

    DosingMag = (desiredMag - currentMag) * volume / 12.4

    return round(DosingMag, 2)


def main():
    try:
        xml = parseXML()
        dosingAlk = calc_alk(xml[0])
        dosingCalc = calc_calc(xml[1])
        dosingMag = calc_mag(xml[2])
    except Exception as e:
        print(e)


if __name__ == "__main__":
    
    # calling main function
    main()
