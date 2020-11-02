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
from enum import Enum
class movieSource(Enum):
  default = "popular"
  byId =  "byId"
  byGenere = "byGenere"

# from . import utils

robotResponse = []
userResponse = []
userQuestions = []
assistant = assistant.Assistant()


# Set up TMDB_assistant
api_key = "02834833a9dfe29dc2c55eb707c5a73c"
language = "en-US"
TMDB_assistant = tmdb_assistant.TMDB_assistant(api_key, language)

class Server():
  def __init__(self):
    self.user_genre = None
    self.data = {
        "userinfo":{
          "username": None,
          'age': 21,
          'language': 'en',
          'session_id': None,
          "guest_session_id": None,
          "expires_at": None
        },
        "browser_status": {
          "movieSource":movieSource.default.value,
          "lastMovieId": None,
          "lastGenreText": None,
        },
        "favorite_list":{},
        "movieList":TMDB_assistant.get_popular_movies(),
      }
    self.serverState = 0
    self.total_quesitons = 3
    self.end_question = False
    # self.movieList = []
    self.robot_question = [
    {
      "questionCode" : 1,
      "questionString" : "What language do you speak?" 
    },{
      "questionCode" : 2,
      "questionString" : "What genre would you like to watch?"
    },{
      "questionCode" : 3,
    "questionString" :  "are you over 18?"
    }
  ]
  def save_data(self):
    with open('data.txt', 'w') as outfile:
      json.dump(self.data, outfile)

  def read_data(self):
    with open('data.txt', 'r') as outfile:
      self.data = json.load(outfile)

  def set_genre_list(self, genre_list):
    self.genre_list = genre_list

  def get_genre_list(self):
    return self.genre_list

  def reset_server(self):
    self.__init__()
    self.save_data()

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
  
  def process_user_input(self, user_answer):
    # Get response from IBM assistant:
    assistant.create_session()
    robot_response = assistant.ask_assistant(user_answer)
    assistant.end_session()
    return robot_response


# =================================== Set up Server
server = Server()
genre_list = TMDB_assistant.get_all_genres()
server.set_genre_list(genre_list)

# Return the first robot questions to user interface
@api_view(['GET'])
def reset_server(request):
    server.reset_server()
    return Response(
      data="Session reset completed!" + "  Current server code: "+str(server.serverState)
    )

# =================================== browser Status management 
@api_view(['GET'])
def get_browser_status(request):
  return Response(
    data={"browser_status":server.data["browser_status"] }
  )

@api_view(['GET'])
def update_last_movie_id(request):
  server.data["browser_status"]["movieSource"] = movieSource.byId.value
  server.data["browser_status"]["lastMovieId"]= request.query_params["lastMovieId"]
  server.save_data()
  return Response(
    data={"browser_status":server.data["browser_status"] }
  )

@api_view(['GET'])
def update_last_genere_text(request):
  server.data["browser_status"]["movieSource"] = movieSource.byGenere.value
  server.data["browser_status"]["lastGenreText"]= request.query_params["lastGenreText"]
  server.save_data()
  return Response(
    data={"browser_status":server.data["browser_status"] }
  )

# =================================== MovieList management 
@api_view(['GET'])
def get_current_favorite_list(request):
  server.read_data()
  return Response(
    data={"favorite_list":server.data["favorite_list"]}
  )

@api_view(['GET'])
def remove_a_favorite_movie(request):
  server.read_data()
  movie_id= request.query_params["movie_id"]
  server.data["favorite_list"].pop(movie_id)
  print(server.data["favorite_list"])
  server.save_data()
  return Response(
    data={"favorite_list":server.data["favorite_list"]}
  )

@api_view(['GET'])
def add_a_favorite_movie(request):
  server.read_data()
  movie_id= request.query_params["movie_id"]
  movie_json_obj = TMDB_assistant.get_movie_by_id(movie_id)
  server.data["favorite_list"][movie_id] = movie_json_obj
  server.save_data()
  # server.data["favorite_list"].append(movie_json_obj)
  return Response(
    data={"favorite_list":server.data["favorite_list"]}
  )

# =================================== User Session management 
@api_view(['GET'])
def get_permissions_link(request):
  # url, server.data["tmp_token"] = TMDB_assistant.get_permissions_link()
  # return Response(
  #   data={"url": url, "tmp_token": server.data["tmp_token"]}
  # )
  raise NotImplementedError

@api_view(['GET'])
def create_user_session(request):
    # server.data["userinfo"]["username"] = request.query_params["username"]
    # server.data["userinfo"]["age"]  = request.query_params["age"]
    # server.data["userinfo"]["language"]  = request.query_params["language"]
    # server.user_token, server.session_id = TMDB_assistant.create_user_session()
    # # You must open the browser, and grated the authentication within 5 sec in order to create the session.
    # server.save_data()
    # return Response(
    #   data={"mesage":"User session created successfully!", 
    #   "userinfo":server.data["userinfo"], 
    #   "movieList":server.data["movieList"]}
    # )
    raise NotImplementedError

@api_view(['GET'])
def create_guest_session(request):
  server.data["userinfo"]["username"] = request.query_params["username"]
  server.data["userinfo"]["age"]  = request.query_params["age"]
  server.data["userinfo"]["language"]  = request.query_params["language"]
  TMDB_assistant.language = request.query_params.get("language")
  success, guest_session_id, expires_at = TMDB_assistant.create_guest_session()
  if success:
    server.data["userinfo"]["guest_session_id"] = guest_session_id
    server.data["userinfo"]["expires_at"] = expires_at
    server.save_data()
    data = {"message": "Guest session created successfully!", "userinfo":server.data["userinfo"], "favorite_list":server.data["favorite_list"], "movieList":server.data["movieList"]}
  else:
    data = {"message": "Error, Invalid API key: You must be granted a valid key."}
  return Response( 
    data=data
  )

@api_view(['GET'])
def get_user_info(request):
  server.read_data()
  return Response(
    data=server.data["userinfo"]
  )

@api_view(['GET'])
def update_user_info(request):
  server.read_data()
  # server.data["userinfo"]["username"] = request.query_params.get("username")
  # server.data["userinfo"]["age"]  = request.query_params.get("age")
  # server.data["userinfo"]["language"]  = request.query_params.get("language")
  if request.query_params.__contains__("username"):
    server.data["userinfo"]["username"] = request.query_params.get("username")
  if request.query_params.__contains__("age"):
    server.data["userinfo"]["age"]  = request.query_params.get("age")
  if request.query_params.__contains__("language"):
    server.data["userinfo"]["language"]  = request.query_params.get("language")
    TMDB_assistant.language = request.query_params.get("language")
  server.save_data()
  return Response(
    data=server.data["userinfo"]
  )


# -------------------------TMDB API Call ------------------------
@api_view(['GET'])
def get_movie_by_id(request):
    movie_id = request.query_params["movie_id"]
    json_data = TMDB_assistant.get_movie_by_id(movie_id)
    # geodata = response.json()
    return Response(
      data={"movieList": json_data}
    )

# Return the first robot question and server.movieList to user interface
@api_view(['GET'])
def get_current_movie_list(request):
    server.read_data()
    return Response(
      data={"movieList": server.data["movieList"]}
    )

@api_view(['GET'])
def get_movie_trailer_link(request):
  movie_id = request.query_params["movie_id"]
  trailer_link = TMDB_assistant.get_movie_trailer_link(movie_id)
  # print(f"movie_id: {trailer_link}")
  return Response(
    data={"trailer": trailer_link}
  )

@api_view(['GET'])
def get_movie_overview(request):
  movie_id = request.query_params["movie_id"]
  print(f"movie_id: {movie_id}")
  movie_json_object = TMDB_assistant.get_movie_by_id(movie_id)
  overview = movie_json_object.get("overview")
  if overview==None:
    overview = "Error!! overview doesn't exist for the given movie!"
  return Response(
    data={"trailer": overview}
  )

# Return one movie object
@api_view(['GET'])
def get_latest_movie(query):
  # Get the data from TMDB databases
  json_data = TMDB_assistant.get_latest_movie()
  # update the movie list
  # print(f"json_data {json_data}")
  # server.data["movieList"] = json_data
  return Response(
    data={"movieList": json_data}
  )

@api_view(['GET'])
def get_upcoming_movie(request):
  page = int(request.query_params['page'])
  # Get the data from TMDB databases
  json_data = TMDB_assistant.get_upcoming_movie(page)
  # update the movie list
  # print(f"json_data {json_data}")
  # server.movieList = json_data
  return Response(
    data={"movieList": json_data}
  )

@api_view(['GET'])
def get_popular_movies(request):
  """
  Argument: 
    top_n: int, the number of movie you want to retrive
  Return:
    a list of top_n movie, each movie is constructed with a dictionary, e.g., 
    {'popularity': 2699.389, 'vote_count': 0,... 'release_date': '2020-09-29'}
  """
  top_n = int(request.query_params['top_n'])
  page = int(request.query_params['page'])
  # print(f"query.data: {query.data}, query.query_params: {query.query_params}")
  # ==> query.data: {}, query.query_params: <QueryDict: {'top_n': ['10']}>
  # Get the data from TMDB databases
  json_data = TMDB_assistant.get_popular_movies(top_n, page)
  # json_data = json.loads(json_data)
  # update the movie list
  # server.movieList = json_data
  return Response(
    data={"movieList":json_data}
  )

# Return the first robot question and server.movieList to user interface
@api_view(['GET'])
def get_recommendation_for_movie(request):
  movie_id = request.query_params["movie_id"]
  page = int(request.query_params['page'])
  print(f"movie_id: {movie_id}")
  movieList = TMDB_assistant.get_recommendation_for_movie(movie_id, page)
  # server.movieList = movieList
  return Response(
    data={"movieList": movieList}
  )

@api_view(['GET'])
def get_similar_movies(request):
  movie_id = request.query_params["movie_id"]
  page = int(request.query_params['page'])
  print(f"movie_id: {movie_id}")
  movieList = TMDB_assistant.get_similar_movies(movie_id, page)
  # server.movieList = movieList
  return Response(
    data={"movieList": movieList}
  )

# -------------------IBM API Call --------------------
def hello(request):
  return JsonResponse({'response_text':'hello world!'})

# Front end will post the language, e.g. en-US, and the TMDB server will update the language.
@api_view(["POST"])
def set_up_languages(request):
  language = request.data["language"]
  print(f"language: {language}")
  TMDB_assistant.set_language(language)
  return Response({"message": "Updated language to: "+language})

# Return all robot questions to user interface
@api_view(['GET'])
def get_all_question(request):
    return Response(
      data=server.robot_question
    )
  
# Return the first robot question and server.movieList to user interface
@api_view(['GET'])
def get_next_question(request):
    return Response(
      data=[server.get_next_question(),{"movieList": server.movieList}]
    )

@api_view(['GET'])
def get_IBM_response(request):
  # Obtain user answer：
  user_answer = request.query_params["answerText"]
  # Get response from IBM assistant:
  assistant.create_session()
  robot_response = assistant.ask_assistant(user_answer)
  assistant.end_session()
  return Response(
    data= {"robotResponse": robot_response}
  )

# Assume the post_answer method only take care one question: "What genre do you like to watch?"
@api_view(['GET'])
def post_answer(request):
    """
    List all code snippets, or create a new snippet.
    """
    # If the request 'Get' method, the next reuqestion and current movieList will be returned
    if request.method == 'POST':
      return Response(
        data=[server.get_next_question(),
            {"movieList": server.movieList}]
      )

    # If the request 'POST' method, the robot_response and the updated movieList will be returned
    # e.g. user say: { "questionCode": 1, "answerText": "War"} ==> {"robotResponse": "Found you requested genre War with id 10752", 
    # "movieList": { ... }}
    elif request.method == 'GET':
        user_answer = request.query_params["answerText"]
        page = int(request.query_params['page'])
        # print(f"user_answer: {user_answer}")

        # Get response from IBM assistant:
        assistant.create_session()
        user_answer = assistant.ask_assistant(user_answer)
        # print(f"user_answer: {user_answer}")
        # Search genre id based on user input:
        user_answer = user_answer.capitalize()  # some query preprocessing
        # user_answer = "Action"
        gener_list = server.get_genre_list()  # Update the genre list in server object
        exist = False # whether there is requested genre in TMDB database
        # print(f"gener_list: {gener_list}")
        gener_id = 0

        for item in gener_list:
          genre_type = item['name']
          # print(f"item: {item}")
          # print(f"genre_type: {genre_type}, type: {type(genre_type)}")
          if genre_type == user_answer:
            gener_id = item["id"]
            exist = True
            # Store genre
            server.user_genre = gener_id
            # print(f"Found genre_id: {gener_id}")

        # Update the robot_response 
        if exist:
          robot_response = f"Found you requested genre {user_answer} with id {gener_id}"
        else:
          robot_response = "Error, we don't have the result you are asking!"
        # Update the movieList
        server.movieList = TMDB_assistant.discover_movies(page, gener_id=gener_id)
        assistant.end_session()
        return Response(
            data= {"robotResponse": robot_response, "movieList": server.movieList}
        )
