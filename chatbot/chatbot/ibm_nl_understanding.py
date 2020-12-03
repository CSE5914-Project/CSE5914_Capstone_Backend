import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import EmotionOptions, Features, EntitiesOptions, KeywordsOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class NLUnderstand:

    def __init__(self):
        API_KEY = 'gll0qvBJM9VnCJFEsTw6mt1sY6nJN_y7nqjT9Hwdr3My'
        authenticator = IAMAuthenticator(API_KEY)
        self.service = NaturalLanguageUnderstandingV1(
            version='2020-11-11', authenticator=authenticator)
        self.service.set_service_url(
            'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2d2f051b-f683-4e06-b513-0c6bbf1341c1')

    def analyze(self, input):
        return self.service.analyze(text=input, features=Features(
            entities=EntitiesOptions(), keywords=KeywordsOptions(), sentiment=SentimentOptions())).get_result()

    def get_keywords(self, input):
        """Gets keywords from input text.

        Parameters
        ----------
        input: str,

        Returns
        -------
        list
            A list of keywords extracted by NLU
            example: [tom cruise, movie]
        """

        response = self.analyze(input)
        # print(json.dumps(response, indent=2))
        keywords = []
        for value in response['keywords']:
            keywords.append(value['text'])
        return keywords

    def get_sentiment(self, input):
        """Analyze the sentiment of the input sentence

        Parameters
        ----------
        input: str

        Returns
        -------
        int
            The score of sentiment.
            positive number means positive sentiment, 0 means neutural, negative means negative sentiment
            range is [-1, 1]
        """
        response = self.analyze(input)
        if (response['sentiment']):
            return response['sentiment']['document']['score']
        return 0

    def get_people(self, input):
        # get a list of people's name appeared in text

        response = self.analyze(input)
        people = []
        for value in response['entities']:
            if value['type'] == 'Person':
                if 'disambiguation' in value:
                    people.append(value['disambiguation']
                                  ['name'].replace('_', ' '))
                else:
                    people.append(value['text'])
        return people

    def get_movies(self, input):
        # get a list of movie title appeared in text
        # however this function is not very reliable

        response = self.analyze(input)
        movies = []
        for value in response['entities']:
            if value['type'] == 'Movie':
                movies.append(value['text'])

        return movies

# if __name__ == '__main__':
print("\n=======> Example usage of NLU")
# --------------------------
nlu = NLUnderstand()
# text = 'I love watching Tom cruise\'s movies and Star Trek'
# print(f'text1: {text}')
# print(f"Keyword: {nlu.get_keywords(text)}")
# print(f"Sentiment scores: {nlu.get_sentiment(text)}")
# print(f"Cast/Crews: {nlu.get_people(text)}")
# print(f"Target Movie: {nlu.get_movies(text)}")
# print()

text = 'I want to watch Star Trek moives'
print(f'text2: {text}')
print(f"Keyword: {nlu.get_keywords(text)}")
print(f"Sentiment scores: {nlu.get_sentiment(text)}")
print(f"Cast/Crews: {nlu.get_people(text)}")
print(f"Target Movie: {nlu.get_movies(text)}")
print()

# text = 'Search for Transformer'
# print(f'text3: {text}')
# print(f"Keyword: {nlu.get_keywords(text)}")
# print(f"Sentiment scores: {nlu.get_sentiment(text)}")
# print(f"Cast/Crews: {nlu.get_people(text)}")
# print(f"Target Movie: {nlu.get_movies(text)}")
# print()


print(nlu.get_keywords('I want to watch action movie today'))
print(nlu.get_keywords('no i am not'))
print(nlu.get_keywords("show me some sci fi movie"))

# ==> Result:
# Keyword: ['Star Trek', "Tom cruise's movies"]
# Sentiment scores: 0.975645
# Cast/Crews: ['Tom Cruise']
# Target Movie: ['Star Trek']
# Keyword: ['Star Trek moives']
# Sentiment scores: 0.608018
# Cast/Crews: ['Trek moives']
# Target Movie: []

