import requests
import json
from requests.auth import HTTPBasicAuth
import datetime
from add_label import add_label

email = ''  # set admin`s email
api_token = ''  # set admin`s api token

URL = 'https://wonderland.atlassian.net/wiki/rest/api/content/'

AUTH = HTTPBasicAuth(email, api_token)

HEADERS = {
    'Authorization': 'Basic {}'.format(AUTH),
    'Content-Type': 'application/json',
}


def update_storage_data(storage_data, date, project_name):
    """
    This method update html code form template and inserts into it project_name and date
    :param storage_data:
    :param date:
    :param project_name:
    :return: updating storage value
    """
    value_storage_splited = storage_data.split('time datetime=')
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
    """
    This method create 'Daily Report page for project'
    :param parent_page_id:
    :param space_key:
    :param storage_data: page`s html code from the template
    :param project_name:
    :return:
    """
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

            daily_label = 'daily_report_{}_{}_{}'.format(day, month, year)
            add_label(page_id, daily_label, AUTH, HEADERS)
            return page_id

    except requests.exceptions.RequestException as e:
        print("Error: {}".format(e))
