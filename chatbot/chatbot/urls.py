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
from django.urls import include

from . import views
from .view_list import user,session
from .view_list.session import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',views.home,name='home'),
    path('api/reset_server/',views.reset_server,name='reset_server'),
# =================================== Nightly Testing
    path('api/hello/',views.hello,name='hello'),
    path('api/get_permissions_link/',views.get_permissions_link,name='get_permissions_link'),
    path('api/create_user_session/',views.create_user_session,name='create_user_ses1sion'),
# =================================== page Status management 
    path('api/get_browser_status/',views.get_browser_status,name='get_browser_status'),
    path('api/update_last_movie_id/',views.update_last_movie_id,name='update_last_movie_id'),
    path('api/update_last_genere_text/',views.update_last_genere_text,name='update_last_genere_text'),

# =================================== User Session management 
    path('api/create_guest_session/',views.create_guest_session,name='create_guest_session'),
    path('api/get_user_info/',views.get_user_info,name='get_user_info'),
    path('api/update_user_info/',views.update_user_info,name='update_user_info'),
# =================================== MovieList management     
    path('api/get_current_movie_list/',views.get_current_movie_list,name='get_current_movie_list'),
    path('api/remove_a_favorite_movie/',views.remove_a_favorite_movie,name='remove_a_favorite_movie'),
    path('api/add_a_favorite_movie/',views.add_a_favorite_movie,name='add_a_favorite_movie'),
    path('api/get_current_favorite_list/',views.get_current_favorite_list,name='get_current_favorite_list'),
# --------------------------------IBM relevant request    -----------
    path('api/get_all_question/',views.get_all_question,name='get_all_question'),
    path('api/get_next_question/',views.get_next_question,name='get_next_question'),
    path('api/set_up_languages/',views.set_up_languages,name='set_up_languages'),
    path('api/post_answer/',views.post_answer,name='post_answer'),
    path('api/get_IBM_response/',views.get_IBM_response,name='get_IBM_response'),
# --------------------------------Movie relevant request    -----------
    path('api/get_movie_by_id/',views.get_movie_by_id,name='get_movies'),
    path('api/get_movie_trailer_link/',views.get_movie_trailer_link,name='get_movie_trailer_link'),
    path('api/get_movie_overview/',views.get_movie_overview,name='get_movie_overview'),
    
    path('api/get_popular_movies/',views.get_popular_movies,name='get_popular_movies'),
    path('api/get_latest_movie/',views.get_latest_movie,name='get_latest_movie'),
    path('api/get_upcoming_movie/',views.get_upcoming_movie,name='get_upcoming_movie'),
    path('api/get_similar_movies/',views.get_similar_movies,name='get_similar_movies'),
    path('api/get_recommendation_for_movie/',views.get_recommendation_for_movie,name='get_recommendation_for_movie'),

# --------------------------------Movie relevant request    -----------
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/user/create_user/',user.create_user,name='create_user'),
    path('accounts/signup/', user.SignUpView.as_view() , name='signup'),
    path('accounts/get_session/', session.get_session , name='get_session'),
    path('accounts/save_session/', session.save_session , name='save_session'),
# --------------------------------Session test --------------------
]