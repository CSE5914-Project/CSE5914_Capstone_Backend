import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class Assistant:
    authenticator = IAMAuthenticator('n0wn_OrjN7yR0PPbTP-C8x2tgczMZwGSruI-tfMvM6r-')
    assistant = AssistantV2(version='2020-04-01', authenticator=authenticator)
    assistant.set_service_url(
        'https://api.us-south.assistant.watson.cloud.ibm.com/instances/ddab0742-ca44-444e-b4b3-420a1868a372')

    ASSISTANT_ID = '0d6f7d80-c769-42d2-bccf-183d7700bc6b'

    def __init__(self):
        self.session_id = ''
        self.create_session()
        print(self.session_id)

    def create_session(self):
        session = self.assistant.create_session(self.ASSISTANT_ID).get_result()
        self.session_id = session.get('session_id')

    def ask_assistant(self, message):
        """Gets the response from Watson assistant.
            At this point the message should only be a yes/no type answer for asking age
                or querying for movie genre
            Random input may get a 'I didn't understand' response

        Parameters
        ----------
        message: str,
            user input message to get response for

        Returns
        -------
        str
            The string of what assistant response
            possible values for now: 'yes', 'no', '[Genres]' 'I didn't understand.'
        """
        if self.session_id == '':
            self.create_session()
        response = self.assistant.message(assistant_id=self.ASSISTANT_ID, session_id=self.session_id,
                                          input={'text': message}).get_result()
        return response.get('output').get('generic')[0].get('text')

    def end_session(self):
        self.assistant.delete_session(self.ASSISTANT_ID, self.session_id).get_result()
        self.session_id = ''

# Example usage of Assistant
# --------------------------
assistant = Assistant()
print(assistant.ask_assistant('yes i am'))
print(assistant.ask_assistant('I want to watch action movie today'))
print(assistant.ask_assistant('no i am not'))
print(assistant.ask_assistant("show me some sci fi movie"))
assistant.end_session
