import requests
import ApplovinRequestHandler.views as applovinAPIHandler

localOS = ''
localCountry = ''
localApplicationName = ''
localDate = ''
localTimeInterval = ''


def ParameterSetterForAdjust(os, country, applicationName, date, timeInterval):
    global localOS
    global localCountry
    global localApplicationName
    global localDate
    global localTimeInterval
    localOS = os
    localCountry = country
    localApplicationName = applicationName
    localDate = date
    localTimeInterval = timeInterval


header = {
    "Authorization": "Bearer NWzdXy_UzpEuUhppYxxp",
    "Content-Type": "application/json"
}


def MakeAdjustRequest():
    data = {
        "date_period": str(localDate),
        "dimensions": "app,partner"+","+str(localTimeInterval)+","+"os_name,country",
        "ad_spend_mode": 'network',
        "metrics": "installs,cost",
        "campaign__contains": str(localOS),
        "country__in": str(localCountry),
        "app__in": str(localApplicationName),
    }

    parameters = "&".join([f"{k}={v}" for k, v in data.items()])
    url = f"https://dash.adjust.com/control-center/reports-service/report?{parameters}"
    print(url)
    response = requests.get(url, headers=header, params=parameters)
    return response
