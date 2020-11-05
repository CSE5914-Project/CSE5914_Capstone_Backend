import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions

authenticator = IAMAuthenticator('gll0qvBJM9VnCJFEsTw6mt1sY6nJN_y7nqjT9Hwdr3My')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator
)

natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2d2f051b-f683-4e06-b513-0c6bbf1341c1')

def get_keywords(user_query):

    response = natural_language_understanding.analyze(
        text=user_query,
        features=Features(keywords=KeywordsOptions(sentiment=True,emotion=True,limit=2))).get_result()
    try:
        kwords = [i['text'] for i in response.get('keywords',[])]

    except KeyError as e:
        return []
    return kwords


if __name__ == '__main__':
    response = get_keywords("I just want something i can watch with my family")
    print(json.dumps(response, indent=2))
    response = get_keywords("I really want some thriller today")
    print(json.dumps(response, indent=2))