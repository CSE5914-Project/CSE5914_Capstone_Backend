import requests
import json
import unittest

class Test_TMDB_Movies(unittest.TestCase):
    def test_get_get_movie_by_id1(self):
        movie_id = 550
        r = requests.get("http://127.0.0.1:8000/api/get_movie_by_id/?movie_id="+str(movie_id))
        self.assertEqual(r.json()['movieList']['id'], movie_id, "Should be Equal")


if __name__ == '__main__':
    unittest.main()
    # test_get_movies1()
    # test_get_question1()
    # test_post_answer1()