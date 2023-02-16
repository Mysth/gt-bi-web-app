from django.shortcuts import render
import requests

start = ''
end = ''
campaing = ''
filter_campaign = ''
application_name = ''
report_type = ''


def applovin_ios_parameter_setter(startDate, endDate, application, reportType):
    global report_type
    global start
    global end
    start = startDate
    end = endDate
    global filter_campaign
    global application_name
    if application == "City Fighter vs Street Gang":
        filter_campaign = 'CF_iOS_AdROAS'
        application_name = 'city fighter'
    if application == 'Milk Crate Challange 3D"':
        filter_campaign = "Milk_Crate_IOS_AdROAS"
        application_name = 'milk crate challange' or 'Milk Crate Challange'

        # AppLovin API URL for access token
url = "https://oauth.applovin.com/oauth/v1/access_token"

# Request headers
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Request body
data = {
    "client_id": "6a495ba030196100261765153acbefa6",
    "client_secret": "cbce7b0e19b2e1449a001c2d1345705ea200f7a4dd30b8f7a73a106d94219544",
    "grant_type": "client_credentials",
    "scope": "campaigns:read creatives:read"
}

api_key = "qTeE-iA6xvqVFi1tikNa8PzkQw-TJL08veMtLXzHQoogVpXCXwngKlPleNDzkE5ctSTD-RVPEH4l5cxcXiIsRh"
columns = "day,cost"
format = "json"
filter_platform = "ios"
report_type = "advertiser"
filter_country = "gb"


def get_report(api_key, start, end, columns, format, filter_platform, report_type, filter_campaign, filter_country):
    url = "https://r.applovin.com/probabilisticReport"
    parameters = {
        "api_key": api_key,
        "start": start,
        "end": end,
        "columns": columns,
        "format": format,
        "filter_platform": filter_platform,
        "report_type": report_type,
        "filter_campaign": filter_campaign,
        "filter_country": filter_country
    }
    response = requests.get(url, params=parameters)
    return response.json()


def make_applovin_revenue_request():
    url = "https://r.applovin.com/maxReport?start={}&end={}&api_key=qTeE-iA6xvqVFi1tikNa8PzkQw-TJL08veMtLXzHQoogVpXCXwngKlPleNDzkE5ctSTD-RVPEH4l5cxcXiIsRh&format=json&columns=estimated_revenue,day,ecpm&filter_platform={}&filter_country={}&filter_application={}".format(
        start, end, filter_platform, filter_country, application_name)
    response = requests.get(url)
    print(url)

    return response.json()


def make_applovin_request_for_usios():
    result = get_report(api_key, start, end, columns, format,
                        filter_platform, report_type, filter_campaign, filter_country)
    return result
