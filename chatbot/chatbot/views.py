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

serverState = 0
userResponse = []
robotResponse = []
userQuestions = {1:"Hello", 0:"I am tired", 2: "Give me some movies"}
assistant = assistant.Assistant()

api_key = "02834833a9dfe29dc2c55eb707c5a73c"
language = "en-US"
tmdb_assistant = tmdb_assistant.TMDB_assistant(api_key, language)

def hello(request):
  return JsonResponse({'response_text':'hello world!'})

@api_view(('GET',))
def get_movie_by_id(request):
    movie_id = 550
    json_data = tmdb_assistant.get_movie_by_id(movie_id)
    # geodata = response.json()
    return Response(
      data={"movieList":json_data}
    )

@api_view(('GET', ))
def get_popular_movies(self, top_n=10):
  """
  Argument: 
    top_n: int, the number of movie you want to retrive
  Return:
    a list of top_n movie, each movie is constructed with a dictionary, e.g., 
    {'popularity': 2699.389, 'vote_count': 0, 'video': False, 'poster_path': '/6CoRTJTmijhBLJTUNoVSUNxZMEI.jpg', 'id': 694919, 'adult': False, 'backdrop_path': '/9Y12EdkIVvYir3uTcZGjqfXWBUv.jpg', 'original_language': 'en', 'original_title': 'Money Plane', 'genre_ids': [28], 'title': 'Money Plane', 'vote_average': 0, 'overview': "A professional thief with $40 million in debt and his family's life on the line must commit one final heist - rob a futuristic airborne casino filled with the world's most dangerous criminals.", 'release_date': '2020-09-29'}
  """
  json_data = tmdb_assistant.get_popular_movies(top_n)
  return Response(
    data={"movieList":json_data}
  )

@api_view(('GET',))
def get_question(request):
    assistant.create_session()
    user_question = userQuestions[1] # assume greeting first
    robot_response = assistant.ask_assistant(user_question)
    assistant.end_session()
    # geodata = response.json()
    return Response(
      data={"questionString":robot_response,"questionCode":1}
    )
  
@api_view(['GET', 'POST'])
def post_answer(request):
    """
    List all code snippets, or create a new snippet.
    """
    movie_id = 550

    if request.method == 'GET':
      response_data = list(range(10))
      # geodata = response.json()
      return Response(
        data=response_data
      )
        # snippets = Snippet.objects.all()
        # serializer = SnippetSerializer(snippets, many=True)
        # return Response(serializer.data)

    elif request.method == 'POST':
        assistant.create_session()
        data = request.data
        print(type(data))
        userResponse.append(data)
        if int(data['questionCode']) in userQuestions:
          user_question = userQuestions[int(data['questionCode'])]
        print(user_question)

        # get response and movie list
        updatedMovieList = tmdb_assistant.get_movie_by_id(movie_id)
        robotMessage = assistant.ask_assistant(user_question)
        responseData = {"nextQuestionString": robotMessage,"nextQuestionCode": int(data['questionCode'])+1,"updatedMovieList" : updatedMovieList}
        assistant.end_session()
        return Response(
          data=responseData
        )
          
