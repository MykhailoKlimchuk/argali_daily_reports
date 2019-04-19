import requests
import json


def add_label(page_id, label_name, auth, headers):
    url = "https://wonderland.atlassian.net/wiki/rest/api/content/{}/label".format(page_id)

    payload = json.dumps([{
        "prefix": "global",
        "name": label_name
    }])
    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )
    print(json.loads(response.text))
