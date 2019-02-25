import twitter

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tool import getter

text = "【拡散希望】いもむし食べたい!!!"
t_api_key, t_api_secret, _ = getter.getTwitterAPIConsumer()
token, token_secret, _, _ = getter.getTwitterAccess()

# 取得したキーとアクセストークンを設定する
auth = twitter.OAuth(consumer_key=t_api_key,
                     consumer_secret=t_api_secret,
                     token=token,
                     token_secret=token_secret)

t = twitter.Twitter(auth=auth)

# twitterへメッセージを投稿する 
t.statuses.update(status=text)
print("success tweet: " + text)