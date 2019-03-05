# Voice To Tweet
## Preparation
### Twitter
1. achieve to useable API of Twitter
2. create `twitter_api.json` into `parts/info/`
3. run `parts/twitter/OAuth_test.py` and access outputted URL
4. accept twitter authenticate with an account you want to tweet
5. parameter is sent to callback URL with GET method, so get OAuth token from that
6. create `twitter_oauth.json` into `parts/info/`
7. run `parts/twitter/get_access.py`, `twitter_access.json` is generated into `parts/info/`
8. test to tweet by to run `parts/twitter/tweet_test.py`

### Watson - Speech to Text
1. achieve to useable API of Watson - Speech to Text
2. create `speech_to_text_api.json` into `parts/info/`
3. run `parts/voice/record_to_text_loop.py` and check availability of able convert voice to text

## Start v2t
after test of above, `product/voice_to_tweet.py` is runnable. 

### Demo Twitter Account
#### @sugoi_majide
[![@sugoi_majide](https://pbs.twimg.com/profile_images/1051660323394973697/3jKTozlj.jpg)](https://twitter.com/sugoi_majide)

## JSON Specification
in `parts/info/`
### **twitter_api.json**
```
{
    "twitter_api_key": "<consumer API key>",
    "twitter_api_secret": "<consumer API secret key>",
    "oauth_callback": "<callback URL>"
}
```
### **twitter_oauth.json**
```
{
    "oauth_token": "<oauth token>",
    "oauth_verifier": "<oauth verifier>"
}
```
### **twitter_access.json**
```
{
    "oauth_token": "<twitter oauth token>",
    "oauth_token_secret": "<twitter oauth token secret>",
    "user_id": "<id number>",
    "screen_name": "<twitter user name (@****) >"
}
```
### **peech_to_text_api.json** and **speech_to_text_api_old.json**
#### **speech_to_text_api.json**
```
    "api_key": "<api key>",
    "url": "<api url, default: `https://gateway-tok.watsonplatform.net/speech-to-text/api`>",
    "lang_model": "ja-JP_BroadbandModel"
```
#### **speech_to_text_api_old.json**
```
{
    "user": "<api user name>",
    "pswd": "<api password>",
    "lang_model": "<language model>"
}
```

#### Allowable values for "lang_model": 
- `ar-AR_BroadbandModel`
- `de-DE_BroadbandModel`
- `en-GB_BroadbandModel`
- `en-GB_NarrowbandModel`
- `en-US_BroadbandModel`
- `en-US_NarrowbandModel`
- `en-US_ShortForm_NarrowbandModel`
- `es-ES_BroadbandModel`
- `es-ES_NarrowbandModel`
- `fr-FR_BroadbandModel`
- `fr-FR_NarrowbandModel`
- `ja-JP_BroadbandModel`
- `ja-JP_NarrowbandModel`
- `ko-KR_BroadbandModel`
- `ko-KR_NarrowbandModel`
- `pt-BR_BroadbandModel`
- `pt-BR_NarrowbandModel`
- `zh-CN_BroadbandModel`
- `zh-CN_NarrowbandModel`

Default: `en-US_BroadbandModel`

## External link
### Twitter Developer Page
[https://developer.twitter.com/en.html](https://developer.twitter.com/en.html)
### IBM Watson Speech to Text
[https://www.ibm.com/watson/services/speech-to-text/](https://www.ibm.com/watson/services/speech-to-text/)