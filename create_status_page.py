import requests
import json
from requests.auth import HTTPBasicAuth
import datetime

email = ''  # set admin`s email
api_token = ''  # set admin`s api token

URL = 'https://wonderland.atlassian.net/wiki/rest/api/content/'

AUTH = HTTPBasicAuth(email, api_token)

HEADERS = {
    'Authorization': 'Basic {}'.format(AUTH),
    'Content-Type': 'application/json',
}


def update_storage_data(storage_data, label):
    value_storage_splited = storage_data.split('SET_LABEL')
    finished = value_storage_splited[0] + label + value_storage_splited[1]
    return finished


def create_status_page(parent_page_id, space_key, storage_data):
    current_date = datetime.datetime.now()

    year = current_date.year
    month = current_date.month if len(str(current_date.month)) == 2 else '0{}'.format(current_date.month)
    day = current_date.day if len(str(current_date.day)) == 2 else '0{}'.format(current_date.day)
    page_title = 'Daily Status for {}.{}.{}'.format(day, month, year)
    label = 'daily_report_{}_{}_{}'.format(day, month, year)
    storage_data = update_storage_data(storage_data, label)
    data = {
        'type': 'page',
        'title': page_title,
        'ancestors': [
            {
                'id': parent_page_id
            }],
        'space': {'key': space_key},
        "body": {
            "storage": {
                "value": storage_data,
                "representation": "storage"

            }
        }
    }

    try:
        response = requests.post(url=URL, data=json.dumps(data), headers=HEADERS, auth=AUTH)

        if not response.status_code // 100 == 2:
            print("Error: Unexpected response {}".format(response))
        else:
            page_id = json.loads(response.text).get('id')
            print('Page Created!')
            return page_id

    except requests.exceptions.RequestException as e:
        print("Error: {}".format(e))
