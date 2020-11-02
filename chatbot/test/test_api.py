import requests
import json

def test_get_movies1():
    # data={"questionCode": 1,"answerText": "yes"}
    r = requests.get("http://127.0.0.1:8000/api/get_movie_by_id/")
    # 
    print(r.json()['movieList'])

def test_get_question1():
    # data={"questionCode": "1","answerText": "yes"}
    r = requests.get("http://127.0.0.1:8000/api/get_question/")
    # 
    print(f"Robot Question: {r.json()['questionString']}")

def test_post_answer1():
    data={"questionCode": 1, "answerText": "yes"}
    r = requests.post("http://127.0.0.1:8000/api/post_answer/", data=data)
    # 
    print(f"User answer: {r.json()}")


def test_post_create_user1():
    data={'name':'hs', 'email': "123@gmail.com", 'password': "sdfdsfsdfs"}
    r = requests.post("http://127.0.0.1:8000/api/user/create_user", data=data)
    # 
    print(f"User answer: {r.json()}")

def test_post_save_session1():
    data={'name':'hs', 'email': "123@gmail.com", 'password': "sdfdsfsdfs"}
    r = requests.post("http://127.0.0.1:8000/api/user/create_user", data=data)
    # 
    data={'user_id':'hs', 'liked_movies': ["123","1234"]}
    r = requests.get("http://127.0.0.1:8000/account/get_session",data=data)



    print(f"User response: {r.json()}")

def get_top_n_popular_movie():
    pass

if __name__ == '__main__':
    # test_get_movies1()
    # test_get_question1()
    # test_post_answer1()

    test_post_create_user1()