import requests
import json
import random
from requests.auth import HTTPBasicAuth
import get_template
import datetime
from add_label import add_label

email = 'mikeklimchuck@gmail.com'
api_token = '1eLH9EZnc3ymzVD1TqYd2F7B'

URL = 'https://wonderland.atlassian.net/wiki/rest/api/content/'

AUTH = HTTPBasicAuth(email, api_token)

HEADERS = {
    'Authorization': 'Basic {}'.format(AUTH),
    'Content-Type': 'application/json',
}


def update_storage_data(storage_data, date, project_name):
    value_storage_splited = value_storage.split('time datetime=')
    first_space = value_storage_splited[1].find(' ')
    temp_sec_part = value_storage_splited[1][first_space:]

    year = date.year
    month = date.month if len(str(date.month)) == 2 else '0{}'.format(date.month)
    day = date.day if len(str(date.day)) == 2 else '0{}'.format(date.day)
    date_text = '"{}-{}-{}"'.format(year, month, day)

    finished = value_storage_splited[0] + 'time datetime=' + date_text + temp_sec_part
    value_storage_splited_2 = finished.split('PROJECT_NAME')
    finished = value_storage_splited_2[0] + project_name + value_storage_splited_2[1]
    return finished


def create_new_daily_report(parent_page_id, space_key, storage_data, project_name):
    current_date = datetime.datetime.now()

    year = current_date.year
    month = current_date.month if len(str(current_date.month)) == 2 else '0{}'.format(current_date.month)
    day = current_date.day if len(str(current_date.day)) == 2 else '0{}'.format(current_date.day)
    page_title = 'Daily Report for {}.{}.{}'.format(day, month, year)

    storage_data = update_storage_data(storage_data, current_date, project_name)
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
            add_label(page_id, "daily_report", AUTH, HEADERS)
            return page_id

    except requests.exceptions.RequestException as e:
        print("Error: {}".format(e))


TEMPLATE_ID = 808616025

template = get_template.get_template_by_id(TEMPLATE_ID)
value_storage = template.get('body').get('storage').get('value')

parent_page_id_dungeon = 808648705
space_key_dungeon = 'DC'


page_id = create_new_daily_report(parent_page_id_dungeon, space_key_dungeon, value_storage, 'Dungeon')
