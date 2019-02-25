from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
import json

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tool import getter

# oauth_callback : Twitter Application Management で設定したコールバックURLsのどれか
t_api_key, t_api_secret, oauth_callback = getter.getTwitterAPIConsumer()

request_token_url = 'https://api.twitter.com/oauth/request_token'

twitter = OAuth1Session(t_api_key, t_api_secret)

response = twitter.post(
    request_token_url,
    params={'oauth_callback': oauth_callback}
)

# responseからリクエストトークンを取り出す
request_token = dict(parse_qsl(response.content.decode("utf-8")))

# リクエストトークンから連携画面のURLを生成
authenticate_url = "https://api.twitter.com/oauth/authenticate"
authenticate_endpoint = '%s?oauth_token=%s' \
    % (authenticate_url, request_token['oauth_token'])

print('access & accept! -> ' + authenticate_endpoint)