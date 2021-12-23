import pandas as pd
import requests
import time
from flask import Flask, render_template, request

def JSONify (data):
    events = []
    user = []

    typeIndex = list(data.columns).index('type.1')
    profileIndex = list(data.columns).index('profileData')
    temp1 = {}
    for i in range(len(data)):
        temp = {}
        temp['identity'] = data.iloc[i][data.columns[0]]
        temp['ts'] = int(round(time.time(), 0))
        temp['type'] = 'event'
        temp['evtName'] = data.iloc[i]['evtName']
        temp1 = {}
        for j in range(5, typeIndex):
            temp1[list(data.columns)[j]] = str(data.iloc[i][list(data.columns)[j]])
        temp['evtData'] = temp1
        events.append(temp)
        temp = {}
        temp['identity'] = data.iloc[i][data.columns[0]]
        temp['ts'] = int(round(time.time(), 0))
        temp['type'] = data.iloc[i]['type.1']
        temp1 = {}
        for j in range(profileIndex+1, len(data.columns)):
            if list(data.columns)[j] == 'parent name.1':
                temp1['parent name'] = data.iloc[i][list(data.columns)[j]]
            else:
                temp1[list(data.columns)[j]] = data.iloc[i][list(data.columns)[j]]
        temp['profileData'] = temp1
        user.append(temp)

    events = {'d': events}
    user = {'d': user}

    headers = {
        'X-CleverTap-Account-Id': '86K-4KR-WR6Z',
        'X-CleverTap-Passcode': 'SMM-AWC-YWUL',
        'Content-Type': 'application/json; charset=utf-8',
    }

    usr = f'''{user}'''
    response1 = requests.post(
        'https://api.clevertap.com/1/upload?dryRun=1', headers=headers, data=usr)

    evt = f'''{events}'''
    response2 = requests.post(
        'https://api.clevertap.com/1/upload?dryRun=1', headers=headers, data=evt)

    
    return response1.json(), usr, response2.json(), evt
    


app = Flask(__name__, template_folder='templates')


@app.route('/')
def upload_files():
    return render_template('upload.html')


@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        data = pd.read_csv(f)
    # data.columns = ["identity",	'ts',	'type',	'evtName',	'evtData',	'category',	'age group',	'course title',	'lesson number','lesson name',	'preferred date',	'parent name',	'email', 	'course url',	'platform',	'transaction date',	'channel',	'zoom link',	'learning material',	'feedback jotform',	'type.1',	'profileData',	'customer type',	'parent name.1',	'child name','child birthdate']

    return f'''{JSONify(data)}'''


if __name__ == '__main__':
    app.debug = True
    app.run()
