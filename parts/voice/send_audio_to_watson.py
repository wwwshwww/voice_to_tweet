from watson_developer_cloud import SpeechToTextV1
import json

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tool import getter

# define
user, pswd, lang = getter.getSpeechToTextAPIConsumer()
audio_file = open("sample.wav", "rb")
cont_type = "audio/wav"

# watson connection
stt = SpeechToTextV1(username=user, password=pswd)
result = stt.recognize(audio=audio_file,
    content_type=cont_type, model=lang)
    
result_dict = result.get_result()
for i in range(len(result_dict['results'])):
    print(result_dict['results'][i]['alternatives'][0]['transcript'])

# for i in range(len(json_result["results"])):
#     print(json_result["results"][i]["alternatives"][0]["transcript"])

# json file save
with open("result.json", "w") as f:
    json.dump(result_dict, f, indent=4)