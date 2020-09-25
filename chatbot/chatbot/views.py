"""
Django views for chatbot project.

Created manually

"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from django.http import JsonResponse
from . import assistant
from . import tmdb_assistant
import requests
import json

robotResponse = []
userResponse = []
userQuestions = []
assistant = assistant.Assistant()

class Server():
  
  def __init__(self):
     self.serverState = 0
     self.total_quesitons = 3
     self.end_question = False
     self.movieList = []
     self.robot_question = [
    {
      "questionCode" : 1,
      "questionString" : "are you over 18?"
    },{
      "questionCode" : 2,
      "questionString" : "What language do you speak?"
    },{
      "questionCode" : 3,
    "questionString" : "What genre would you like to watch?"
    }
  ]

  # Update the serverState if there is question left, other wise return error!
  def get_next_question(self):
    question = {}
    if self.end_question == True:
      question = {
      "questionCode" : 9999,
      "questionString" : "You've reached last question?"
      }
    else:
      # Get question 
      question = self.robot_question[self.serverState]
      # Update server state
      self.serverState+=1
      if self.serverState == self.total_quesitons:
        self.end_question = True
    return question

api_key = "02834833a9dfe29dc2c55eb707c5a73c"
language = "en-US"
tmdb_assistant = tmdb_assistant.TMDB_assistant(api_key, language)
server = Server()

# -------------------------TMDB API Call ------------------------
@api_view(('GET',))
def get_movie_by_id(request):
    movie_id = 550
    json_data = tmdb_assistant.get_movie_by_id(movie_id)
    # geodata = response.json()
    return Response(
      data={"movieList":json_data}
    )

@api_view(('GET', ))
def get_popular_movies(top_n=10):
  """
  Argument: 
    top_n: int, the number of movie you want to retrive
  Return:
    a list of top_n movie, each movie is constructed with a dictionary, e.g., 
    {'popularity': 2699.389, 'vote_count': 0, 'video': False, 'poster_path': '/6CoRTJTmijhBLJTUNoVSUNxZMEI.jpg', 'id': 694919, 'adult': False, 'backdrop_path': '/9Y12EdkIVvYir3uTcZGjqfXWBUv.jpg', 'original_language': 'en', 'original_title': 'Money Plane', 'genre_ids': [28], 'title': 'Money Plane', 'vote_average': 0, 'overview': "A professional thief with $40 million in debt and his family's life on the line must commit one final heist - rob a futuristic airborne casino filled with the world's most dangerous criminals.", 'release_date': '2020-09-29'}
  """
  # Get the data from TMDB databases
  json_data = tmdb_assistant.get_popular_movies(top_n)
  # update the movie list
  server.movieList = json_data
  return Response(
    data={"movieList":json_data}
  )

# -------------------IBM API Call --------------------
def hello(request):
  return JsonResponse({'response_text':'hello world!'})

# Return the first robot questions to user interface
@api_view(('GET',))
def get_question(request):
    # assume greeting first
    # robot_question =  
    return Response(
      data=server.get_next_question()
    )
  
# Return the first robot questions to user interface
# @api_view(('GET',))
# def get_question(request):
#     assistant.create_session()
#     user_question = userQuestions[1] # assume greeting first
#     robot_response = assistant.ask_assistant(user_question)
#     assistant.end_session()
#     # geodata = response.json()
#     return Response(
#       data={"questionString":robot_response,"questionCode":1}
#     )

@api_view(['GET', 'POST'])
def post_answer(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
      return Response(
        data=server.get_next_question()
      )
      # snippets = Snippet.objects.all()
      # serializer = SnippetSerializer(snippets, many=True)
      # return Response(serializer.data)

    elif request.method == 'POST':
        # ?? what this doing here?? 
        # userResponse.append(user_response)
        # if user_response['questionCode'] in userQuestions:
        #   user_question = user_response['questionString']
        # print(user_question)

        # Obtain user answer
        user_response = request.data
        print(user_response)
        user_answer = user_response["answerText"]

        # Get response from IBM assistant:
        assistant.create_session()
        robot_response = assistant.ask_assistant(user_answer)
        # responseData = {"nextQuestionString": robotMessage,"nextQuestionCode": int(data['questionCode'])+1,"updatedMovieList" : updatedMovieList}
        assistant.end_session()

        # get response and movie list
        # updatedMovieList = tmdb_assistant.get_movie_by_id(movie_id)
        # assistant.create_session()
        # robotMessage = assistant.ask_assistant(user_answer)
        # # responseData = {"nextQuestionString": robotMessage,"nextQuestionCode": int(data['questionCode'])+1,"updatedMovieList" : updatedMovieList}
        # assistant.end_session()
        return Response(
          data=robot_response
        )
          
