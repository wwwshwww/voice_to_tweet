from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
import json
import os
import sys
this_path = os.path.dirname(__file__)
sys.path.append(os.path.join(this_path, '..'))
from tool import getter

t_api_key, t_api_secret, _ = getter.getTwitterAPIConsumer()

oauth_token, oauth_verifier = getter.getOAuth()

access_token_url = 'https://api.twitter.com/oauth/access_token'

twitter = OAuth1Session(
    t_api_key,
    t_api_secret,
    oauth_token,
    oauth_verifier,
)

response = twitter.post(
    access_token_url,
    params={'oauth_verifier': oauth_verifier}
)

# responseからアクセストークンを取り出す
print(response.content)
access_token = dict(parse_qsl(response.content.decode("utf-8")))

with open(this_path + '/../info/twitter_access.json', 'w') as file:
    json.dump(access_token, file, indent=4)

print(access_token)
print('success get access token!')