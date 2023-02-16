from GameTheory_BI_WebApp.models import Rows

daily_time_list = []
rows = []
revenueList = {}


def get_rows(response):
    global rows
    rows = create_daily_rows(response)
    for i in rows:
        if i.date not in daily_time_list:
            daily_time_list.append(str(i.date))

    Rows.objects.bulk_create(rows)
    return rows


def get_daily_time_list(rows):
    return daily_time_list


def get_revenue_list(revenueResponse):
    for i in revenueResponse.get('results'):
        revenueList[str(i.get('day'))] = i.get('estimated_revenue')
    return revenueList


def create_daily_rows(response):
    Rows.objects.all().delete()
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
        day = value.get("day")
        installs = value.get("installs")

        attr_dependency = value.get("attr_dependency")
        if attr_dependency:
            campaign_network = attr_dependency.get("campaign_id_network", "")
        else:
            campaign_network = ""

        row = Rows(app=app, country=country, cost=cost,
                   partner=partner, os_name=os_name, date=day,
                   installs=installs, campaign_network=campaign_network)
        rows.append(row)

    return rows
