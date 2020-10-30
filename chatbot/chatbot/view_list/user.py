from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseBadRequest
from chatbot import models
from chatbot import  assistant
from chatbot import forms
import requests
import json

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.views import APIView



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

class SignUpView(generic.CreateView):
    form_class = forms.CustomUserCreationForm
    success_url = reverse_lazy('accounts/login')
    template_name = 'registration/signup.html'


class ProfileFormView(APIView):
    # Assume you have a model named UserProfile
    # And a serializer for that model named UserSerializer
    # This is the view to let users update their profile info.
    # Like E-Mail, Birth Date etc.

    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except:
            return None

    # this method will be called when your request is GET
    # we will use this to fetch field names and values while creating our form on React side
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        if not user:
            return JsonResponse({'status': 0, 'message': 'User with this id not found'})

        # You have a serializer that you specified which fields should be available in fo
        serializer = UserSerializer(user)
        # And here we send it those fields to our react component as json
        # Check this json data on React side, parse it, render it as form.
        return JsonResponse(serializer.data, safe=False)

    # this method will be used when user try to update or save their profile
    # for POST requests.
    def post(self, request, pk, format=None):
        try:
            user = self.get_object(pk)
        except:
            return JsonResponse({'status': 0, 'message': 'User with this id not found'})

        e_mail = request.data.get("email", None)
        birth_date = request.data.get('birth_date', None)
        job = request.data.get('job', None)

        user.email = e_mail
        user.birth_date = birth_date
        user.job = job

        try:
            user.save()
            return JsonResponse({'status': 1, 'message': 'Your profile updated successfully!'})
        except:
            return JsonResponse({'status': 0, 'message': 'There was something wrong while updating your profile.'})