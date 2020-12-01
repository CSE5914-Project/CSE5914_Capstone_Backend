import requests
import json
import unittest

class Test_TMDB_Movies(unittest.TestCase):
    def test_get_get_movie_by_id1(self):
        movie_id = 550
        r = requests.get("http://127.0.0.1:8000/api/get_movie_by_id/?movie_id="+str(movie_id))
        self.assertEqual(r.json()['movieList']['id'], movie_id, "Should be Equal")

    # def test_get_question1():
    #     # data={"questionCode": "1","answerText": "yes"}
    #     r = requests.get("http://127.0.0.1:8000/api/get_question/")
    #     print(f"Robot Question: {r.json()['questionString']}")

    # def test_post_answer1():
    #     data={"questionCode": 1, "answerText": "yes"}
    #     r = requests.post("http://127.0.0.1:8000/api/post_answer/", data=data)
    #     print(f"User answer: {r.json()}")

    # def get_top_n_popular_movie():
    #     pass

class Test_API(unittest.TestCase):

    def test_post_answer_multiturn_1(self):
        data={"questionCode": 1, "answerText": "I would like something for my family",'page':1}
        r = requests.get("http://127.0.0.1:8000/api/post_answer_multiturn/", params=data)

        self.assertEqual(r.json()['movieList']['id'], movie_id, "Should be Equal")

    def test_post_answer_multiturn_1(self):
        data={"questionCode": 1, "answerText": "I would like something for my family",'page':1}
        r = requests.get("http://127.0.0.1:8000/api/post_answer_multiturn/", params=data)
        print(r)
        print(f"User answer: {r.json()}")


if __name__ == '__main__':
    unittest.main()
    # test_get_movies1()
    # test_get_question1()
    # test_post_answer1()