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
import requests
import json



def hello(request):
  return JsonResponse({'response_text':'hello world!'})
  

@api_view(('GET',))
def get_movies(request):
    # response = requests.get('http://freegeoip.net/json/')
    response_data = ['movie {}'.format(i) for i in range(10)]
    # geodata = response.json()
    return Response(
      data=response_data
    )

@api_view(('GET',))
def get_question(request):
    # response = requests.get('http://freegeoip.net/json/')
    response_data = list(range(10))
    # geodata = response.json()
    return Response(
      data=response_data
    )

@api_view(['GET', 'POST'])
def post_answer(request):
    """
    List all code snippets, or create a new snippet.
    """
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
        data = json.dumps(request.data)
        print(data)
        response_data = {"nextQuestionString": "xxxx","nextQuestionCode": "2","updatedMovieList" : [{}, {}, {}]}
        return Response(
          data=response_data
          )