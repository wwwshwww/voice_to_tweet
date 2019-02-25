import json

def getInfo(path, err_msg):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print('Error: ' + err_msg)
        exit()
