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
from chatbot import models
from chatbot import  assistant
import requests
import json



@api_view(['POST'])
def create_user(request):
    """
    List all code snippets, or create a new snippet.
    """
    # if request.method == 'GET':
    #   response_data = list(range(10))
    #   # geodata = response.json()
    #   return Response(
    #     data=response_data
    #   )
    #     # snippets = Snippet.objects.all()
    #     # serializer = SnippetSerializer(snippets, many=True)
    #     # return Response(serializer.data)

    if request.method == 'POST':
        data = request.data
        try:
            if data['name'] and data['email'] and data['password']:
                print(data)
                user = models.Person.objects.create(name=data['name'], email=data['email'], password=data['password'])


            

        except (Exception, KeyError) as e:
            print(e)
            return HttpResponseBadRequest()
        # get response and movie list
        # assistant(user_question)
        # assistant.end_session()
        responseData = {"login": "Success"}
        return Response(
          data=responseData
          )

"""
 def create(self, **kwargs):
        
        Creates a new object with the given kwargs, saving it to the database
        and returning the created object.
        
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db)
        return obj
"""