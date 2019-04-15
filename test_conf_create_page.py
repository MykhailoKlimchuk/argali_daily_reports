import requests
import json
from requests.auth import HTTPBasicAuth

email = 'mikeklimchuck@gmail.com'
api_token = 'marshalshady'

page_title = 'test page'
page_html = '<p>This page was created with Python!</p>'

parent_page_id = 808648705
space_key = 'DC'

url = 'http://wonderland.atlassian.net/wiki/rest/api/content/'

auth = HTTPBasicAuth(email, api_token)

headers = {
    'Authorization': 'Basic {}'.format(auth),
    'Content-Type': 'application/json',
}

data = {
    'type': 'page',
    'title': page_title,
    'ancestors': [{'id':parent_page_id}],
    'space': {'key':space_key},
    'body': {
        'storage':{
            'value': page_html,
            'representation':'storage',
        }
    }
}

try:
    r = requests.post(url=url, data=json.dumps(data), headers=headers)
    if not r.status_code // 100 == 2:
        print("Error: Unexpected response {}".format(r))
    else:
        print('Page Created!')

except requests.exceptions.RequestException as e:

    print("Error: {}".format(e))