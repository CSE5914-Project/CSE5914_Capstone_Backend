# This program translate a piece
import subprocess
import requests
import json

API = {
  "apikey": "pU-g-4CPjauoZBpVDEC58QMPfXxXl8R06EnmurtIb9QX",
  "iam_apikey_description": "Auto-generated for key e159326d-147d-477f-8c72-fc2735135cb7",
  "iam_apikey_name": "Auto-generated service credentials",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/1e0763c1010f4e268cfe0a32c0c9988f::serviceid:ServiceId-66e6b35d-3825-4d42-91c6-2f9139ca90eb",
  "url": "https://api.us-south.language-translator.watson.cloud.ibm.com/instances/af931a5f-645c-43ee-a82d-2051dce96ed4"
}


SERVICE = '/v3/translate?version=2018-05-01'

def translate(sentence_list, api, src_lang, tgt_lang):
    # request translate from watson
    payload = {
        'text': sentence_list,
        "model_id":"{}-{}".format(src_lang,tgt_lang)
      }
    headers = {
        'apikey':api['apikey'],
        'content-type': 'application/json'
      }
    url = api['url'] + SERVICE

    r = requests.post(url, data=json.dumps(payload), headers=headers, auth=('apikey', api['apikey']))

    return r


# if __name__ == '__main__':
print('\n=========> Translator Testing samples: ')
sentence_list = ["Hello!", "What's going on?"]
source_lang = 'en'
target_lang = 'zh'
api = API
# print([type(i) for i in API.keys()])
# print(API[list(API.keys())[0]])
msg = translate(sentence_list, API, source_lang, target_lang)
translation = [i['translation'] for i in json.loads(msg.text)['translations']]
# print(msg.text)
print('Translate {} to {}:\n'.format(source_lang,target_lang))
for sent, translate in zip(sentence_list, translation):
    print('Original: {}\nTranslate: {}\n'.format(sent,translate))
