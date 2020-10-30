from django.db import models
from django.contrib.auth.models import User

# class Person(models.Model):
#     name = models.CharField(max_length=30)
#     email = models.EmailField(max_length=100,primary_key=True)
#     password = models.CharField(max_length=512)


class Movie(models.Model):
    name = models.CharField(max_length=100)
    movie_homepage = models.CharField(max_length=120)
    movie_id = models.CharField(max_length=128,primary_key=True)


class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    
    user_ptr = models.OneToOneField(
        User, on_delete=models.CASCADE,
        parent_link=True,
    )

    movie_ptr = models.OneToOneField(
        Movie, on_delete=models.CASCADE,
        parent_link=True,
    )