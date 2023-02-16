from django.template.defaulttags import register
from django.shortcuts import render
from . import forms
import requests
import json
import pandas as pd
from .models import Rows
from .models import RowsWeekly
import ApplovinRequestHandler.views as applovinRequestHandler
import AdjustRequestHandler.views as adjustRequestHandler
import DailyCostRevenueApp.views as dailyCostRevenueHandler
import WeeklyCostRevenueApp.views as weeklyCostRevenueHandler
# Create your views here.
COUNTRY_LIST = [
    ("0", "Afghanistan"),
    ("1", "Albania"),
    ("2", "Algeria"),
    ("3", "American Samoa"),
    ("4", "Andorra"),
    ("5", "Angola"),
    ("6", "Anguilla"),
    ("7", "Antarctica"),
    ("8", "Antigua and Barbuda"),
    ("9", "Argentina"),
    ("10", "Armenia"),
    ("11", "Aruba"),
    ("12", "Australia"),
    ("13", "Austria"),
    ("14", "Azerbaijan"),
    ("15", "Bahamas (the)"),
    ("16", "Bahrain"),
    ("17", "Bangladesh"),
    ("18", "Barbados"),
    ("19", "Belarus"),
    ("20", "Belgium"),
    ("21", "Belize"),
    ("22", "Benin"),
    ("23", "Bermuda"),
    ("24", "Bhutan"),
    ("25", "Bolivia (Plurinational State of)"),
    ("26", "Bonaire, Sint Eustatius and Saba"),
    ("27", "Bosnia and Herzegovina"),
    ("28", "Botswana"),
    ("29", "Bouvet Island"),
    ("30", "Brazil"),
    ("31", "British Indian Ocean Territory (the)"),
    ("32", "Brunei Darussalam"),
    ("33", "Bulgaria"),
    ("34", "Burkina Faso"),
    ("35", "Burundi"),
    ("36", "Cabo Verde"),
    ("37", "Cambodia"),
    ("38", "Cameroon"),
    ("39", "Canada"),
    ("40", "Cayman Islands (the)"),
    ("41", "Central African Republic (the)"),
    ("42", "Chad"),
    ("43", "Chile"),
    ("44", "China"),
    ("45", "Christmas Island"),
    ("46", "Cocos (Keeling) Islands (the)"),
    ("47", "Colombia"),
    ("48", "Comoros (the)"),
    ("49", "Congo (the Democratic Republic of the)"),
    ("50", "Congo (the)"),
    ("51", "Cook Islands (the)"),
    ("52", "Costa Rica"),
    ("53", "Croatia"),
    ("54", "Cuba"),
    ("55", "Curaçao"),
    ("56", "Cyprus"),
    ("57", "Czechia"),
    ("58", "Côte d'Ivoire"),
    ("59", "Denmark"),
    ("60", "Djibouti"),
    ("61", "Dominica"),
    ("62", "Dominican Republic (the)"),
    ("63", "Ecuador"),
    ("64", "Egypt"),
    ("65", "El Salvador"),
    ("66", "Equatorial Guinea"),
    ("67", "Eritrea"),
    ("68", "Estonia"),
    ("69", "Eswatini"),
    ("70", "Ethiopia"),
    ("71", "Falkland Islands (the) [Malvinas]"),
    ("72", "Faroe Islands (the)"),
    ("73", "Fiji"),
    ("74", "Finland"),
    ("75", "France"),
    ("76", "French Guiana"),
    ("77", "French Polynesia"),
    ("78", "French Southern Territories (the)"),
    ("79", "Gabon"),
    ("80", "Gambia (the)"),
    ("81", "Georgia"),
    ("82", "Germany"),
    ("83", "Ghana"),
    ("84", "Gibraltar"),
    ("85", "Greece"),
    ("86", "Greenland"),
    ("87", "Grenada"),
    ("88", "Guadeloupe"),
    ("89", "Guam"),
    ("90", "Guatemala"),
    ("91", "Guernsey"),
    ("92", "Guinea"),
    ("93", "Guinea-Bissau"),
    ("94", "Guyana"),
    ("95", "Haiti"),
    ("96", "Heard Island and McDonald Islands"),
    ("97", "Holy See (the)"),
    ("98", "Honduras"),
    ("99", "Hong Kong"),
    ("100", "Hungary"),
    ("101", "Iceland"),
    ("102", "India"),
    ("103", "Indonesia"),
    ("104", "Iran (Islamic Republic of)"),
    ("105", "Iraq"),
    ("106", "Ireland"),
    ("107", "Isle of Man"),
    ("108", "Israel"),
    ("109", "Italy"),
    ("110", "Jamaica"),
    ("111", "Japan"),
    ("112", "Jersey"),
    ("113", "Jordan"),
    ("114", "Kazakhstan"),
    ("115", "Kenya"),
    ("116", "Kiribati"),
    ("117", "Korea (the Democratic People's Republic of)"),
    ("118", "Korea (the Republic of)"),
    ("119", "Kuwait"),
    ("120", "Kyrgyzstan"),
    ("121", "Lao People's Democratic Republic (the)"),
    ("122", "Latvia"),
    ("123", "Lebanon"),
    ("124", "Lesotho"),
    ("125", "Liberia"),
    ("126", "Libya"),
    ("127", "Liechtenstein"),
    ("128", "Lithuania"),
    ("129", "Luxembourg"),
    ("130", "Macao"),
    ("131", "Madagascar"),
    ("132", "Malawi"),
    ("133", "Malaysia"),
    ("134", "Maldives"),
    ("135", "Mali"),
    ("136", "Malta"),
    ("137", "Marshall Islands (the)"),
    ("138", "Martinique"),
    ("139", "Mauritania"),
    ("140", "Mauritius"),
    ("141", "Mayotte"),
    ("142", "Mexico"),
    ("143", "Micronesia (Federated States of)"),
    ("144", "Moldova (the Republic of)"),
    ("145", "Monaco"),
    ("146", "Mongolia"),
    ("147", "Montenegro"),
    ("148", "Montserrat"),
    ("149", "Morocco"),
    ("150", "Mozambique"),
    ("151", "Myanmar"),
    ("152", "Namibia"),
    ("153", "Nauru"),
    ("154", "Nepal"),
    ("155", "Netherlands (the)"),
    ("156", "New Caledonia"),
    ("157", "New Zealand"),
    ("158", "Nicaragua"),
    ("159", "Niger (the)"),
    ("160", "Nigeria"),
    ("161", "Niue"),
    ("162", "Norfolk Island"),
    ("163", "Northern Mariana Islands (the)"),
    ("164", "Norway"),
    ("165", "Oman"),
    ("166", "Pakistan"),
    ("167", "Palau"),
    ("168", "Palestine, State of"),
    ("169", "Panama"),
    ("170", "Papua New Guinea"),
    ("171", "Paraguay"),
    ("172", "Peru"),
    ("173", "Philippines (the)"),
    ("174", "Pitcairn"),
    ("175", "Poland"),
    ("176", "Portugal"),
    ("177", "Puerto Rico"),
    ("178", "Qatar"),
    ("179", "Republic of North Macedonia"),
    ("180", "Romania"),
    ("181", "Russian Federation (the)"),
    ("182", "Rwanda"),
    ("183", "Réunion"),
    ("184", "Saint Barthélemy"),
    ("185", "Saint Helena, Ascension and Tristan da Cunha"),
    ("186", "Saint Kitts and Nevis"),
    ("187", "Saint Lucia"),
    ("188", "Saint Martin (French part)"),
    ("189", "Saint Pierre and Miquelon"),
    ("190", "Saint Vincent and the Grenadines"),
    ("191", "Samoa"),
    ("192", "San Marino"),
    ("193", "Sao Tome and Principe"),
    ("194", "Saudi Arabia"),
    ("195", "Senegal"),
    ("196", "Serbia"),
    ("197", "Seychelles"),
    ("198", "Sierra Leone"),
    ("199", "Singapore"),
    ("200", "Sint Maarten (Dutch part)"),
    ("201", "Slovakia"),
    ("202", "Slovenia"),
    ("203", "Solomon Islands"),
    ("204", "Somalia"),
    ("205", "South Africa"),
    ("206", "South Georgia and the South Sandwich Islands"),
    ("207", "South Sudan"),
    ("208", "Spain"),
    ("209", "Sri Lanka"),
    ("210", "Sudan (the)"),
    ("211", "Suriname"),
    ("212", "Svalbard and Jan Mayen"),
    ("213", "Sweden"),
    ("214", "Switzerland"),
    ("215", "Syrian Arab Republic"),
    ("216", "Taiwan"),
    ("217", "Tajikistan"),
    ("218", "Tanzania, United Republic of"),
    ("219", "Thailand"),
    ("220", "Timor-Leste"),
    ("221", "Togo"),
    ("222", "Tokelau"),
    ("223", "Tonga"),
    ("224", "Trinidad and Tobago"),
    ("225", "Tunisia"),
    ("226", "Turkey"),
    ("227", "Turkmenistan"),
    ("228", "Turks and Caicos Islands (the)"),
    ("229", "Tuvalu"),
    ("230", "Uganda"),
    ("231", "Ukraine"),
    ("232", "United Arab Emirates (the)"),
    ("233", "United Kingdom"),
    ("234", "United States Minor Outlying Islands (the)"),
    ("235", "United States"),
    ("236", "Uruguay"),
    ("237", "Uzbekistan"),
    ("238", "Vanuatu"),
    ("239", "Venezuela (Bolivarian Republic of)"),
    ("240", "Viet Nam"),
    ("241", "Virgin Islands (British)"),
    ("242", "Virgin Islands (U.S.)"),
    ("243", "Wallis and Futuna"),
    ("244", "Western Sahara"),
    ("245", "Yemen"),
    ("246", "Zambia"),
    ("247", "Zimbabwe"),
    ("248", "Åland Islands"),

]
GAME_LIST = [
    ("0", "City Fighter vs Street Gang"),
    ("1", "Milk Crate Challange 3D"),
]
REPORT_TYPE = [
    ("0", "day"),
    ("1", "week"),
    ("2", "month"),
]

partners = set()
dateList = []
totalCostDict = {}
revenueList = {}
revenueListWeekly = {}
revenueWeekly = 0

# Request Variables
os = ''
country = ''
applicationName = ''
date = ''
timeInterval = ''
partners = set()
dateList = []
rows = []


def HomePage(request):
    return render(request, 'index.html')


def GetCountryName(number):
    country_dict = {item[0]: item[1] for item in COUNTRY_LIST}
    return country_dict.get(number, "Invalid number")


def GetApplicationName(number):
    game_dict = {item[0]: item[1] for item in GAME_LIST}
    return game_dict.get(number, "Invalid number")


def GetReportTimeInterval(number):
    report_dict = {item[0]: item[1] for item in REPORT_TYPE}
    return report_dict.get(number, "Invalid number")


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


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def CostRevenueReport(request):
    global os
    global country
    global applicationName
    global date
    global timeInterval
    global partners
    global dateList
    global rows
    global revenueList
    rows = []

    Rows.objects.all().delete()
    RowsWeekly.objects.all().delete()
    dateList.clear()
    revenueList.clear()
    country = ""
    form = forms.CostRevenueReportForm(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():
            if form.cleaned_data['ios'] == 1:
                os = 'ios'
            if form.cleaned_data['android'] == 1:
                os = 'android'
            if form.cleaned_data['ios'] == 1 and form.cleaned_data['android'] == 1:
                os = 'ios,android'

            date = str(form.cleaned_data['startDate']) + \
                ":" + str(form.cleaned_data['endDate'])
            country = GetCountryName(form.cleaned_data['country'])
            applicationName = GetApplicationName(
                form.cleaned_data['applicationName'])
            timeInterval = GetReportTimeInterval(
                form.cleaned_data['reportType'])
            adjustRequestHandler.ParameterSetterForAdjust(
                os, country, applicationName, date, timeInterval)
            adjustResponse = adjustRequestHandler.MakeAdjustRequest()
            if os == "ios":
                applovinRequestHandler.applovin_ios_parameter_setter(str(
                    form.cleaned_data['startDate']), str(form.cleaned_data['endDate']), applicationName, str(timeInterval))
                applovinResponse = applovinRequestHandler.make_applovin_request_for_usios()

            rows.clear()

            if (timeInterval == "day"):
                rows = []
                rows = dailyCostRevenueHandler.get_rows(
                    adjustResponse)
                dateList = dailyCostRevenueHandler.get_daily_time_list(rows)
                for row in rows:
                    partners.add(row.partner)
                    if row.date not in dateList:
                        dateList.append(str(row.date))
                revenueRes = applovinRequestHandler.make_applovin_revenue_request()
                revenueList = dailyCostRevenueHandler.get_revenue_list(
                    revenueRes)

            if (timeInterval == "week"):
                rows = weeklyCostRevenueHandler.get_rows(adjustResponse)
                weeklyDate = []
                for row in rows:
                    partners.add(row.partner)
                    date = str(row.date).replace(" ", "")
                    if row.date not in dateList:
                        dateList.append(str(row.date))
                        weeklyDate.append(date)
                revenueRes = applovinRequestHandler.make_applovin_revenue_request()
                revenueList = weeklyCostRevenueHandler.get_revenue_list(
                    revenueRes)

            if os == "ios":
                
                index = 0
                applovinRequestHandler.applovin_ios_parameter_setter(str(
                    form.cleaned_data['startDate']), str(form.cleaned_data['endDate']), applicationName, str(timeInterval))
                applovinResponse = applovinRequestHandler.make_applovin_request_for_usios()
            
            
            if timeInterval == 'week':
                    for i in rows:
                        if i.partner == 'applovin':
                            print(i.cost)
                            i.cost = 0
                            for j in applovinResponse.get('results'):
                                i.cost += float(j.get('cost'))
            index = 0
            for i in dateList:
                for j in applovinResponse.get('results'):
                    if i == j.get('day'):
                        rows[index].cost = round(float(j.get('cost')), 2)
                        index += 1

            for date in dateList:
                cost = 0
                for row in rows:
                    if row.date == date:
                        cost += float(float(row.cost))
                totalCostDict[date] = round(float(cost), 2)

    context = {'form': form, 'rows': rows, 'totalCostList': totalCostDict,
               'partners': partners, 'dates': dateList, 'revenueList': revenueList, }

    return render(request, 'costrevenuereport.html', context)


...


@ register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def create_weekly_rows(response):
    parsed = response.json()
    first_key = list(parsed.keys())[0]
    values = parsed[first_key]

    rows = []
    for value in values:
        app = value.get("app")
        country = value.get("country")
        cost = value.get("cost")
        partner = value.get("partner")
        os_name = value.get("os_name")
        week = value.get("week")
        installs = value.get("installs")

        attr_dependency = value.get("attr_dependency")
        if attr_dependency:
            campaign_network = attr_dependency.get("campaign_id_network", "")
        else:
            campaign_network = ""

        row = RowsWeekly(app=app, country=country, cost=cost,
                         partner=partner, os_name=os_name, date=week,
                         installs=installs, campaign_network=campaign_network)
        rows.append(row)

    return rows
