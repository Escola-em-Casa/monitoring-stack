import requests
import json
from datetime import datetime, timedelta

DATAMI_USERNAME = "edf"
DATAMI_PASSWORD = "edf"
ELASTIC_USER = "elastic"
ELASTIC_PASSWORD = "elastic"
URL_ELASTIC = "127.0.0.1:9200"


def get_data(from_date, to_date):

    cookies = { '_ga': 'GA1.2.1460178628.1605022849' }

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'https://developer.datami.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://developer.datami.com/',
        'Accept-Language': 'en-US,en;q=0.9,pt;q=0.8',
    }

    data = {
        "userName": DATAMI_USERNAME,
        "userId": DATAMI_PASSWORD,
        "durationType": "RANGE",
        "fromDate": from_date,
        "toDate": to_date,
        "apps": ["SEDUC-DF-Escola-em-Casa-DF"],
        "operators": [],
        "countries": [],
        "osType": "Both",
        "isNewUser": False,
        "isRepeatUser": False,
        "isProductionCampaign": True,
        "filterType": "OPERATOR",
        "campaignUserType": "USER"
    }

    response = requests.post('https://developer.datami.com/gcp_global/gp/v2/analytics/op/brand/datausage',
                             headers=headers, cookies=cookies, data=json.dumps(data))

    return json.loads(response.text)


def main():
    today = datetime.today()
    yesterday = today - timedelta(days=1)

    to_date = str(yesterday.day) + str(yesterday.month) + str(yesterday.year)

    response = get_data(to_date, to_date)
    results = response['results']['data']

    for key in results:
        for day in results[key]:
            if day == 'alias':
                continue

            dt = day.split('/')
            data = {
                'company': key,
                'data_usage': results[key][day],
                'timestamp': dt[2] + '-' + dt[1] + '-' + dt[0] + "T03:00:00.0000"
            }

            headers = {'Content-type': 'application/json'}

            elastic_url = "http://" + ELASTIC_USER + ":" + ELASTIC_PASSWORD + "@" + URL_ELASTIC + "/escola_em_casa_datausage_2/_doc/"
            response_elastic = requests.post(
                elastic_url, headers=headers, data=json.dumps(data))


if __name__ == "__main__":
    main()
