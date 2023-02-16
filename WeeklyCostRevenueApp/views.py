from GameTheory_BI_WebApp.models import RowsWeekly

weekly_time_list = []
rows = []
revenueList = {}
weekly_time_list_reversed = []


def get_rows(response):
    global rows
    global weekly_time_list_reversed
    RowsWeekly.objects.all().delete()
    rows = create_weekly_rows(response)

    for i in rows:
        date = str(i.date)
        if date not in weekly_time_list:
            weekly_time_list.append(date)
    weekly_time_list_reversed = list(reversed(sorted(weekly_time_list)))
    RowsWeekly.objects.bulk_create(rows)
    return rows


def get_weekly_time_list():
    return weekly_time_list


def get_revenue_list(revenueResponse):
    revenueListDays = set()
    for i in revenueResponse.get('results'):
        date = str(i.get('day'))
        revenueListDays.add(date)

    revenueListDays = list(revenueListDays)
    revenueListDays.sort(reverse=True)

    revenueList = []
    for date in revenueListDays:
        for i in revenueResponse.get('results'):
            if str(i.get('day')) == date:
                revenueList.append(i.get('estimated_revenue'))

    weeklyCostPerSevenDays = {}
    while revenueList:
        weekTime = weekly_time_list_reversed.pop(0)
        weeklyCost = 0
        for i in range(min(7, len(revenueList))):
            weeklyCost += float(revenueList.pop(0))
        weeklyCostPerSevenDays[weekTime] = str(round(float(weeklyCost), 2))
    sorted_dict = dict(
        sorted(weeklyCostPerSevenDays.items(), key=lambda x: x[0]))

    return sorted_dict


def create_weekly_rows(response):
    RowsWeekly.objects.all().delete()
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
