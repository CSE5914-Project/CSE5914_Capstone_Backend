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

def get_top_n_popular_movie():
    top_n=10
    pass


if __name__ == '__main__':
    test_get_movies1()
    test_get_question1()
    test_post_answer1()