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
import chatbot.assistant as assistant
import chatbot.tmdb_assistant as tmdb_assistant
import chatbot.translator as translator
import chatbot.nlu  as nlu
import chatbot.ibm_nl_understanding as ibm_nl_understanding
import requests
import json
import os

from enum import Enum
# For language detection in post_answer, https://pypi.org/project/langdetect/
from langdetect import detect
from textblob import TextBlob

print("yes")
# Set up IBM Chatbot API
assistant = assistant.Assistant()
# API For IBM translation
API = {
  "apikey": "pU-g-4CPjauoZBpVDEC58QMPfXxXl8R06EnmurtIb9QX",
  "iam_apikey_description": "Auto-generated for key e159326d-147d-477f-8c72-fc2735135cb7",
  "iam_apikey_name": "Auto-generated service credentials",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/1e0763c1010f4e268cfe0a32c0c9988f::serviceid:ServiceId-66e6b35d-3825-4d42-91c6-2f9139ca90eb",
  "url": "https://api.us-south.language-translator.watson.cloud.ibm.com/instances/af931a5f-645c-43ee-a82d-2051dce96ed4"
}
   
# Set up TMDB_assistant
api_key = "02834833a9dfe29dc2c55eb707c5a73c"
language = "en-US"
TMDB_assistant = tmdb_assistant.TMDB_assistant(api_key, language)

# Set up IBM NLP module
nlu = ibm_nl_understanding.NLUnderstand()

class movieSource(Enum):
  default = "popular"
  byId =  "byId"
  byGenere = "byGenere"

class Server():
  def __init__(self):
    self.curr_dir = "data"
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
    self.question_list = ["What language do you speak?",  "What genre would you like to watch?", "are you over 18?"]
    self.robot_question = [{
        "questionCode" : 1,
        "questionString" : "What language do you speak?" 
      },{
        "questionCode" : 2,
        "questionString" : "What genre would you like to watch?"
      },{
        "questionCode" : 3,
      "questionString" :  "are you over 18?"
      }]

# If you changed language here is what gonna happen: 1) All the question will be covnerted to target language, 2)movie list will be overwirte by popular movies.. ==> SO this funciton is not design for updating server language!!!
  def set_server_language_to(self, target_lang, src_lang="en"):
    # Call the API to do the translation
    msg = translator.translate(self.question_list, API, src_lang, target_lang)
    # Get a list of translated questions
    translations = [i['translation'] for i in json.loads(msg.text)['translations']]
    # Reset the robot_question
    self.robot_question = [{"questionCode": i, "questionString": q} for i,q in enumerate(translations)]
    self.data["movieList"] = TMDB_assistant.get_popular_movies()

  def update_question_language_to(self, target_lang, src_lang="en"):
    # Call the API to do the translation
    msg = translator.translate(self.question_list, API, src_lang, target_lang)
    # Get a list of translated questions
    translations = [i['translation'] for i in json.loads(msg.text)['translations']]
    # Reset the robot_question
    self.robot_question = [{"questionCode": i, "questionString": q} for i,q in enumerate(translations)]

  def translate(self, msg, target_lang, src_lang="en"):
    '''
      msg: string
      target_lang: language code, two char
    '''
    msg = translator.translate(msg, API, src_lang, target_lang)
    translation = [i['translation'] for i in json.loads(msg.text)['translations']]
    return translation

  def save_data(self, username):
    data_path = os.path.join(self.curr_dir, username+".json")
    print(data_path)
    with open(data_path, 'w') as outfile:
      json.dump(self.data, outfile)

  def read_data(self, username):
    data_path = os.path.join(self.curr_dir, username+".json")
    with open(data_path, 'r') as outfile:
      self.data = json.load(outfile)

  def set_genre_list(self, genre_list):
    self.genre_list = genre_list

  def get_genre_list(self):
    return self.genre_list

  def reset_server(self):
    self.__init__()
    TMDB_assistant.language = language
    # self.save_data()

  # Update the serverState if there is question left, other wise return error!
  # def get_next_question(self):
  #   question = {}
  #   if self.end_question == True:
  #     question = {
  #     "questionCode" : 9999,
  #     "questionString" : "You've reached last question?"
  #     }
  #   else:
  #     # Get question 
  #     question = self.robot_question[self.serverState]
  #     # Update server state
  #     self.serverState+=1
  #     if self.serverState == self.total_quesitons:
  #       self.end_question = True
  #   return question
  
  def process_user_input(self, user_answer):
    # Get response from IBM assistant:
    assistant.create_session()
    robot_response = assistant.ask_assistant(user_answer)
    print(f"Result from process_user_input:{robot_response}")
    assistant.end_session()
    return robot_response

# =================================== Set up Server
server = Server()
genre_list = TMDB_assistant.get_all_genres()
server.set_genre_list(genre_list)

# Note: Due to some frontend issue, the POST call is not able to use, so we change all the API calls to GET requests. But we added note in front of function to indicate the function that involves server status update

# To-Do: Removed ==> It's internal function for server
@api_view(['GET'])
def reset_server(request):
    server.reset_server()
    return Response(
      data="Session reset completed!" + "  Current server code: "+str(server.serverState)
    )

# Return all robot questions to user interface
@api_view(['GET'])
def get_all_question(request):
    # print(server.robot_question)
    return Response(
      data = server.robot_question
    )
  
# Return the first robot question and server.movieList to user interface
# @api_view(['GET'])
# def get_next_question(request):
#     return Response(
#       data=[server.get_next_question(),{"movieList": server.data["movieList"]}]
#     )

# Need username as param
@api_view(['GET'])
def user_login(request):
  # What is the user name?
  username = request.query_params["username"]
  server.read_data(username)
  # If the username doesn't exist, server will return None (as default)
  if username == server.data["userinfo"]["username"]:
    response = username + " Log in successfully!"
    language = server.data["userinfo"]["language"]
    if language != "en":
      TMDB_assistant.language = language
      server.update_question_language_to(language)
  else:
    response = "Error, user doesn't exist!'"
  return Response(
    data= response
  )

@api_view(['GET'])
def user_logout(request):
  # What is the user name?
  username = server.data["userinfo"]["username"]
  server.save_data(username)
  server.reset_server()
  return Response(
    data= username + " Logoff!"
  )

# Note: Those functions are used for the purpose of restoring browser status after user last visit
# =================================== browser Status management 
@api_view(['GET'])
def get_browser_status(request):
  return Response(
    data={"browser_status":server.data["browser_status"] }
  )

# Need username as param
# POST: update the last movie that user visited, involves server update
@api_view(['GET'])
def update_last_movie_id(request):
  server.data["browser_status"]["movieSource"] = movieSource.byId.value
  server.data["browser_status"]["lastMovieId"]= request.query_params["lastMovieId"]
  username = server.data["userinfo"]["username"]

  server.save_data(username)
  return Response(
    data={"browser_status":server.data["browser_status"] }
  )

# Need username as param
# POST: update the last genre that user requested, involves server update
@api_view(['GET'])
def update_last_genere_text(request):
  server.data["browser_status"]["movieSource"] = movieSource.byGenere.value
  server.data["browser_status"]["lastGenreText"]= request.query_params["lastGenreText"]
  username = server.data["userinfo"]["username"]

  server.save_data(username)
  return Response(
    data={"browser_status":server.data["browser_status"] }
  )

# Here are a list of methods for managing the movielist, e.g. favoriated_movie list, watched_movie list
# =================================== MovieList management 
@api_view(['GET'])
def get_current_favorite_list(request):
  # Whose favorite_list you want to get?
  return Response(
    data={"favorite_list":server.data["favorite_list"]}
  )

# POST: remove a favorite movie from particular user's list, involves server update
@api_view(['GET'])
def remove_a_favorite_movie(request):
  # what is the movie we want to remove
  movie_id= request.query_params["movie_id"]
  server.data["favorite_list"].pop(movie_id)
  # print(server.data["favorite_list"])

  username = server.data["userinfo"]["username"]
  server.save_data(username)
  return Response(
    data={
      "message": str(movie_id)+" removed!",
      "Current favorite_list": server.data["favorite_list"]
      }
  )

@api_view(['GET'])
def add_a_favorite_movie(request):
  # Who is your target user?
  username = server.data["userinfo"]["username"]
  # what is the movie you want to add to the list?
  movie_id= request.query_params["movie_id"]
  movie_json_obj = TMDB_assistant.get_movie_by_id(movie_id)
  server.data["favorite_list"][movie_id] = movie_json_obj
  # server.data["favorite_list"].append(movie_json_obj)

  server.save_data(username)
  return Response(
    data={
      "message": str(movie_id)+" added!",
      "Current favorite_list": server.data["favorite_list"]
      }
  )

# =================================== User Session management 
# [To-Do] 10/29: For implementing multiuser function, we need to:
  # - Save all user related data(e.g. info, movie, browser status) for the call that related user data update, e.g. 1) update_user_info, 2) add_a_favorite_movie， etc
  # - 需要做一个交restore_user_session的接口，然后你切换用户时，要给我他的名字，如果他名字不在database里的话，我就return error； Otherwise， 就直接把server里的数据都跟新了

# [To-Do] 10/29: Adult movie filtering, whenever the frontend made a movie request, we need to do some filtering process, and only allow valid movie to pass through ==> But the filtering result is same as we implemented this at frontend where we might have less than 20 movie objects to display.

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
  # Get the data from user
  username = server.data["userinfo"]["username"] = request.query_params["username"]
  server.data["userinfo"]["age"]  = request.query_params["age"]
  language  = request.query_params["language"]
  
  # Reset the language for server, and other APIs (if user speak other language than English)
  if language != "en":
    server.data["userinfo"]["language"] = language
    TMDB_assistant.language = language
    server.set_server_language_to(language) # quetion will be update, movie_list ==> popular movies
  
  # Create a session for new user
  success, guest_session_id, expires_at = TMDB_assistant.create_guest_session()
  if success:
    server.data["userinfo"]["guest_session_id"] = guest_session_id
    server.data["userinfo"]["expires_at"] = expires_at
    data = {
      "message": "Guest session created successfully!", "userinfo":server.data["userinfo"], "favorite_list":server.data["favorite_list"], "movieList":server.data["movieList"]
      }
  else:
    data = {"message": "Error, Invalid API key: You must be granted a valid key."}
  server.save_data(username)
  return Response( 
      data=data
    )

@api_view(['GET'])
def get_user_info(request):
  # Who is your target user?
  # username = request.query_params["username"]
  # username = server.data["userinfo"]["username"]
  # server.read_data(username)
  return Response(
    data=server.data["userinfo"]
  )

# Need username as param
# Update user info: name, age, and language
@api_view(['GET'])
def update_user_info(request):
  username = server.data["userinfo"]["username"] = request.query_params.get("username")
  # server.read_data(username)
  # server.data["userinfo"]["username"] = request.query_params.get("username")
  # server.data["userinfo"]["age"]  = request.query_params.get("age")
  # server.data["userinfo"]["language"]  = request.query_params.get("language")
  # if request.query_params.__contains__("username"):
  #   server.data["userinfo"]["username"] = request.query_params.get("username")
  # if request.query_params.__contains__("age"):
  server.data["userinfo"]["age"] = request.query_params.get("age")
  # if request.query_params.__contains__("language"):
  src_lang = server.data["userinfo"]["language"] 
  target_lan = request.query_params.get("language")
  print("in update_user_info", language)
  if src_lang != target_lan:
    TMDB_assistant.language = target_lan
    server.update_question_language_to(target_lan, src_lang) # ==> Only update the questions, not movie list 
    server.data["userinfo"]["language"] = target_lan
  server.save_data(username)
  return Response(
    data=server.data["userinfo"]
  )

# -------------------------TMDB API Call ------------------------
# search_movie_by_keyword return the movie id, not json object
# @api_view(['GET'])
# def search_movie_by_keyword(request):
#     keyword = request.query_params["keyword"]
#     page = request.query_params["page"]
#     # Keyword Translation: If the user don't enter english, we need to convert that:
#     src_lang = server.data["userinfo"]["language"]
#     target_lang = "en"
#     if src_lang!=target_lang:
#       msg = translator.translate([keyword], API, src_lang, target_lang)
#       print(f"msg: {msg}")
#       keyword = [i['translation'] for i in json.loads(msg.text)['translations']][0]
#       print(f"translated keyword: {keyword}")
#     json_data = TMDB_assistant.search_movie_by_keyword(keyword, page)
    
#     # Find the corresponding movie info
#     movieList = []
#     for movie_item in json_data["results"]:
#       print(movie_item)
#       movie_json_object = TMDB_assistant.get_movie_details_by_id(movie_item["id"])
#       if "success" not in movie_json_object:
#         movieList.append(movie_json_object)      

#     return Response(
#       data={"movieList": server.data["movieList"]}
#     )

# TMDB_assistant.search_movie return all the movie json object(Differ from search_movie_by_keyword), supported by https://developers.themoviedb.org/3/search/search-movies
@api_view(['GET'])
def search_movie_by_keyword(request):
    keyword = request.query_params["keyword"]
    page = request.query_params["page"]
    json_data = TMDB_assistant.search_movie(keyword, page, include_adult=request.query_params["include_adult"])  

    return Response(
      data={"movieList": json_data}
    )

# # Drago: What the hell is this?
# @api_view(['GET'])
# def search_movie_by_sentence_keyword(request,top_n = 15):
#     user_response = request.query_params["answerText"]
#     page = request.query_params["page"]
#     keywords = nlu.get_keywords(user_response)
    
#     if len(keywords) > 0:
#       json_data = TMDB_assistant.search_movie_by_keyword(keywords[0], page)
#     else:
#       json_data = TMDB_assistant.get_popular_movies(top_n)

#     return Response(
#       data={"movieList": json_data}
#     )

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
    username = server.data["userinfo"]["username"]
    server.read_data(username)
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

@api_view(['GET'])
def get_IBM_response(request):
  # Obtain user answer：
  user_answer = request.query_params["answerText"]
  # Get response from IBM assistant:
  assistant.create_session()
  robot_response = assistant.ask_assistant(user_answer)
  print(f"Result from get_IBM_response:{robot_response}")
  assistant.end_session()
  return Response(
    data= {"robotResponse": robot_response}
  )

# @api_view(['GET'])
# def get_good_movies_based_on_genre(request):

# @api_view(['GET'])
# def get_bad_movies_based_on_genre(request):

def _reorder_movieList(good_movie_list, bad_movie_list):
  import random
  total_list = []
  # Genre movie doesn't exist, user only provides keywords
  if len(bad_movie_list)==0:
    total_list = good_movie_list
  # Genre exist ==> So we should have two list
  elif len(bad_movie_list)>0:
    n_movies = 0 
    # limit = len(good_movie_list['results']) + len(bad_movie_list['results'])
    good_movie_list = good_movie_list['results']
    bad_movie_list = bad_movie_list['results']
    # Very unlikely we would get the order that [19 bad movie, 10 good movie, 1 bad movie]
    while(len(good_movie_list)>0 and n_movies<30):
      n_movies+=1
      if random.random() > 0.3:
        total_list.append(good_movie_list.pop(0))
      else:
        total_list.append(bad_movie_list.pop(0))
  print(f"Total movies in the list: {len(total_list)}")
  return {'results':total_list}


# Assume the post_answer method only take care one question: "What genre do you like to watch?"
@api_view(['GET'])
def post_answer(request):
    """
    List all code snippets, or create a new snippet.
    """
    # # If the request 'Get' method, the next reuqestion and current movieList will be returned
    # if request.method == 'POST':
    #   question = server.get_next_question()
    #   # if the user don't speak english, convert to corresponding one
    #   if server.data["userinfo"]["language"] != "en":
    #     response = translator.translate([question], API, "en", server.data["userinfo"]["language"])
    #     # print(response.json())
    #     question = response.json()['translations'][0]['translation']
    #   return Response(
    #     # return the next question along with the current movie list
    #     data=[
    #         translated_question,
    #         {"movieList": server.data["movieList"]}
    #       ]
    #   )

    # If the request 'POST' method, the robot_response and the updated movieList will be returned
    # e.g. user say: { "questionCode": 1, "answerText": "War"} ==> {"robotResponse": "Found you requested genre War with id 10752", 
    # "movieList": { ... }}
    if request.method == 'GET':
        # Step1: Get user's response, and the page info to searching corresponding genre movies
        user_answer = request.query_params["answerText"]
        page = int(request.query_params['page'])

        # Step2: Get response from IBM assistant:
        assistant.create_session()
        # If user don't speak english, we need to convert it to en, in order to processing the 'genre' keyword filtering
        # src_lang = detect(user_answer)[:2]
        src_lang = TextBlob(user_answer).detect_language()[:2]
        print(f"User typed language: {src_lang}")
        if src_lang != "en":
          # print(f"user_answer: {user_answer}")
          response = translator.translate([user_answer], API, src_lang, "en")
          print(f"Response: {response}")
          user_answer = response.json()['translations'][0]['translation']
          # response = translator.translate([user_answer], API, src_lang, "en")
          # user_answer = [i['translation'] for i in json.loads(response.text)['translations']]
        print(f"User_answer: {user_answer}")
          
        # Use IBM NLU to extract the keyword, sentiment, cast/crews, and movie title: ==> Not robust enough, required len(user_answer)>45 characters
        with_keyword = None
        keyword_exist = False
        if len(user_answer) > 15:
          with_keyword = nlu.get_keywords(user_answer)[0] # Return the first keyword
          print(f"with_keyword: {with_keyword}")
          if with_keyword:
            keyword_exist = True

        # Use IBM assistant to search movie based on the genre keywords 
        user_answer = assistant.ask_assistant(user_answer)
        print(f"Result from post_answer:{user_answer}")
        # user_answer = user_answer.capitalize()  # some query preprocessing, so "action" ==> "Action"
        # print(user_answer)

        # Step3: Checking whether the requested genere supported by TMDB. if requested genre doesn't exist, return a error response message
        gener_list = server.get_genre_list()  # Update the genre list in server object
        genre_exist = False # whether there is requested genre in TMDB database
        # print(f"gener_list: {gener_list}")
        gener_id = 0
        for item in gener_list:
          genre_type = item['name']
          if genre_type == user_answer:
            gener_id = item["id"]
            genre_exist = True
            server.user_genre = gener_id

        # Update the robot_response 
        good_movie_list = bad_movie_list = {}
        exist = False
        if genre_exist:
          exist = True
          robot_response = f'Found your requested movies with genre "{user_answer}"!'
          # Update the movieList
          # server.data["movieList"] = TMDB_assistant.discover_movies(page, gener_id=gener_id, include_adult=request.query_params['include_adult'])
          # Get the GOOD movie list ==> The result might not necessary to be popular, but at least 50 people say it's GOOD
          good_movie_list = server.data["movieList"] = TMDB_assistant.discover_movies(page, gener_id=gener_id, include_adult=request.query_params['include_adult'], sort_by="vote_average.desc&vote_count.gte=50")
          # Get the BAD movie list ==> The result might not necessary to be popular, but at least 50 people say it's BAD
          bad_movie_list = TMDB_assistant.discover_movies(page, gener_id=gener_id, include_adult=request.query_params['include_adult'], sort_by="vote_average.asc&vote_count.gte=50")
          # combine two list into one with certain amount of randomness
          server.data["movieList"] = _reorder_movieList(good_movie_list, bad_movie_list)
        elif keyword_exist:
          exist = True
          robot_response = f'Found your requested movies with keyword "{with_keyword}"! '
          good_movie_list =  TMDB_assistant.search_movie(with_keyword, page, include_adult=request.query_params["include_adult"])  
          # bad_movie_list = TMDB_assistant.discover_movies(page, include_adult=request.query_params['include_adult'], sort_by="vote_average.asc&vote_count.gte=50", with_keyword=with_keyword)
          server.data["movieList"] = good_movie_list
        else:
          robot_response = "Error, we don't have the result you are asking!"
        assistant.end_session()

        # ==> THe robot response doesn't matter, we never gonna show this to user!!
        # print(f"source_lan: en, target_lang: robot_response: {robot_response}")
        # Step4: Convert and return the robot_response according to the language user speaks
        src_lang = "en"
        target_lang = server.data["userinfo"]["language"]
        if src_lang!=target_lang:
          msg = translator.translate([robot_response], API, src_lang, target_lang)
          robot_response = [i['translation'] for i in json.loads(msg.text)['translations']]
          print(f"msg: {msg}")
        print(f"robot_response: {robot_response}")

        return Response(
            data= {
              "robotResponse": robot_response, 
              "movieList": server.data["movieList"],
              "exist": exist
            }
        )