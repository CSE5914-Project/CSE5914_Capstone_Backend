"""chatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hello/',views.hello,name='hello'),
    # path('',views.home,name='home'),
    path('api/reset_server/',views.reset_server,name='reset_server'),
    path('api/get_all_question/',views.get_all_question,name='get_all_question'),
    path('api/get_next_question/',views.get_next_question,name='get_next_question'),
    path('api/set_up_languages/',views.set_up_languages,name='set_up_languages'),
    path('api/post_answer/',views.post_answer,name='post_answer'),
    path('api/get_IBM_response/',views.get_IBM_response,name='get_IBM_response'),
# --------------------------------Movie relevant request    -----------
    path('api/get_current_movie_list/',views.get_current_movie_list,name='get_current_movie_list'),
    path('api/get_movie_by_id/',views.get_movie_by_id,name='get_movies'),
    path('api/get_movie_trailer_link/',views.get_movie_trailer_link,name='get_movie_trailer_link'),
    path('api/get_movie_overview/',views.get_movie_overview,name='get_movie_overview'),
    
    path('api/get_popular_movies/',views.get_popular_movies,name='get_popular_movies'),
    path('api/get_latest_movie/',views.get_latest_movie,name='get_latest_movie'),
    path('api/get_upcoming_movie/',views.get_upcoming_movie,name='get_upcoming_movie'),
    path('api/get_similar_movies/',views.get_similar_movies,name='get_similar_movies'),
    path('api/get_recommendation_for_movie/',views.get_recommendation_for_movie,name='get_recommendation_for_movie'),
]