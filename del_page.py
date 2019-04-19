import requests
from requests.auth import HTTPBasicAuth

ids_ = [811401261, 811237419, 811368504]
id_ = '811237381'
url = "https://wonderland.atlassian.net/wiki/rest/api/content/{}".format(id_)

email = ''  # set admin`s email
api_token = ''  # set admin`s api token


AUTH = HTTPBasicAuth(email, api_token)


response = requests.request(
    "DELETE",
    url,
    auth=AUTH
)

print(response.text)
