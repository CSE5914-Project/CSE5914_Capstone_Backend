import json
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class Translator:

    def __init__(self):
        API_KEY = 'pU-g-4CPjauoZBpVDEC58QMPfXxXl8R06EnmurtIb9QX'
        authenticator = IAMAuthenticator(API_KEY)
        self.language_translator = LanguageTranslatorV3(version='2018-05-01',
                                                        authenticator=authenticator)
        self.language_translator.set_service_url('https://gateway.watsonplatform.net/language-translator/api')

    def translate(self, text, language='chinese'):
        codedic = {'chinese': 'zh'}
        language_code = codedic[language]
        translation = self.language_translator.translate(text=text, model_id=language_code+'-en').get_result()
        return translation['translations'][0]['translation']

    def list_model(self):
        models = self.language_translator.list_models().get_result()
        print(json.dumps(models, indent=2))


# translator = Translator()
# # translator.list_model()
# print(translator.translate('动作电影'))