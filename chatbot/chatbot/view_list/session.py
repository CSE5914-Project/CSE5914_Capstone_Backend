from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from chatbot.models import  Movie, Like
from django.contrib.auth.models import User
from chatbot import assistant
import requests
import json



@api_view(['GET'])
def get_session(request):
    print(request.session.items())
    response_data = get_session_ours(request.session.get("user_id",""))
    return response(data=response_data)

@api_view(['POST'])
def save_session(request):
    print(request.session.items())
    try:
        user_id = request.session['user_id']
        liked_movies = request.session['liked_movies']

        for movie in liked_movies:
            tgt = Movie.objects.filter(pk=movie)
            if tgt:
                Like.objects.create(user_ptr=user_id,movie_ptr=movie)

            else: 
                Movie.objects.create(movie_id=movie,movie_homepage="",name="")
                Like.objects.create(user_ptr=user_id,movie_ptr=movie)
    except KeyError:
        # clear session
        request.session.flush()
        return HttpResponseBadRequest()
    response_data = {"session":request.session}
    # clear session

    request.session.flush()
    return response(data=response_data)

def save_session_ours(session):
    print(session.items())
    try:
        user_id = session['user_id']
        liked_movies = session['liked_movies']

        for movie in liked_movies:
            tgt = Movie.objects.filter(pk=movie)
            if tgt:
                Like.objects.create(user_ptr=user_id,movie_ptr=movie)

            else: 
                Movie.objects.create(movie_id=movie,movie_homepage="",name="")
                Like.objects.create(user_ptr=user_id,movie_ptr=movie)
    except KeyError:
        # clear session
        
        return 0
    
    return 1

def get_session_ours(user_id):
    session = {}
    try:
        # user_id = session['user_id']
        liked_movies = Like.filter(user_id=user_id)
        movie_list = [liked_movies[i].movie_id for i in range(liked_movies.count())]

        for movie in liked_movies:
            tgt = Movie.objects.filter(pk=movie)
            if tgt:
                Like.objects.create(user_ptr=user_id,movie_ptr=movie)

            else: 
                Movie.objects.create(movie_id=movie,movie_homepage="",name="")
                Like.objects.create(user_ptr=user_id,movie_ptr=movie)
    except KeyError:
        # clear session
        
        return {}

    return {'user_id':user_id,"liked_movies":}
    
    # response_data = {"session":request.session}
    # # clear session
    
    # return response(data=response_data)

def _save_session(session):
    print(session.items())
    try:
        user_id = session['user_id']
        liked_movies = session['liked_movies']

        for movie in liked_movies:
            tgt = Movie.objects.filter(pk=movie)
            if tgt:
                Like.objects.create(user_ptr=user_id,movie_ptr=movie)

            else: 
                Movie.objects.create(movie_id=movie,movie_homepage="",name="")
                Like.objects.create(user_ptr=user_id,movie_ptr=movie)
    except KeyError:
        raise Exception("bad session")
        # clear session
        # session.flush()
        # return HttpResponseBadRequest()
    # response_data = {"session":session}
    # clear session
    # session.flush()
    # return response(data=response_data)