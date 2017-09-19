import csv
from .models import (
    DailyCreditCard,
    DailyInteractions,
    DailyWebsiteTraffic,
    MonthEndBalances)


def create(filename, model):
    with open('wf/fake_data/{}.csv'.format(filename)) as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        rows = []
        for row in reader:
            data = dict(zip(headers, row))
            if "Date" in data:
                data["Date"] = "{}-{}-{}".format(data["Date"][4:8],
                                                 data["Date"][0:2],
                                                 data["Date"][2:4])
            if "asof_yyyymm" in data:
                data["asof_yyyymm"] = "{}-{}-{}".format(
                    data["asof_yyyymm"][0:4], data["asof_yyyymm"][4:6], "01")
            if "" in data:
                del data[""]
            rows.append(model(**data))
        model.objects.bulk_create(rows, batch_size=500)


def import_data(request):
    create("DailyInteractions", DailyInteractions)
    create("DailyCreditCard", DailyCreditCard)
    create("DailyWebsiteTraffic", DailyWebsiteTraffic)
    create("MonthEndBalances", MonthEndBalances)
