import requests
from requests.auth import HTTPBasicAuth
import json

TEMPLATES_URL = "https://wonderland.atlassian.net/wiki/rest/api/template/{}"

email = 'mikeklimchuck@gmail.com'
api_token = '1eLH9EZnc3ymzVD1TqYd2F7B'

AUTH = HTTPBasicAuth(email, api_token)

HEADERS = {
    "Accept": "application/json"
}


def get_template_by_id(template_id):
    template_url = TEMPLATES_URL.format(template_id)

    response = requests.request(
        "GET",
        template_url,
        headers=HEADERS,
        auth=AUTH
    )

    return json.loads(response.text)

# template_id = '811401235'
#
# template = get_template_by_id(template_id)
# print(template.get('body').get('storage').get('value'))
