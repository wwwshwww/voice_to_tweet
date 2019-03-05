from . import opener
import os
import sys

this_path = os.path.dirname(__file__)

def getTwitterAPIConsumer():
    path = this_path + '/../info/twitter_api.json'
    msg = 'please create `twitter_api.json` that have twitter API info to info/'
    data = opener.getInfo(path, msg)
    return data['twitter_api_key'], data['twitter_api_secret'], data['oauth_callback']

def getOAuth():
    path = this_path + '/../info/twitter_oauth.json'
    msg = 'please create `twitter_oauth.json` that have OAuth info to info/'
    data = opener.getInfo(path, msg)
    return data['oauth_token'], data['oauth_verifier']

def getTwitterAccess():
    path = this_path + '/../info/twitter_access.json'
    msg = 'please run `get_access.py` for get twitter_access.json'
    data = opener.getInfo(path, msg)
    return data['oauth_token'], data['oauth_token_secret'], data['user_id'], data['screen_name']

def getSpeechToTextAPIConsumer_old():
    path = this_path + '/../info/speech_to_text_api_old.json'
    msg = 'please create `speech_to_text_api_old.json` that have SpeechToText API info to info/'
    data = opener.getInfo(path, msg)
    return data['user'], data['pswd'], data['lang_model']

def getSpeechToTextAPIConsumer():
    path = this_path + '/../info/speech_to_text_api.json'
    msg = 'please create `speech_to_text_api.json` that have SpeechToText API info to info/'
    data = opener.getInfo(path, msg)
    return data['api_key'], data['url'], data['lang_model']