import requests
import json

#
#   test_post_answer
#
def test_post_answer1():
    data={"answerText": "action","page": "1"}
    r = requests.get("http://127.0.0.1:8000/api/post_answer/", data)
    # 
    print(f"User answer1: {r.json()['robotResponse']}")

def test_post_answer2():
    data={"answerText": "sci-fi","page": "1"}
    r = requests.get("http://127.0.0.1:8000/api/post_answer/", data)
    # 
    print(f"User answer2: {r.json()['robotResponse']}")

def test_post_answer3():
    data={"answerText": "romantic","page": "2"}
    r = requests.get("http://127.0.0.1:8000/api/post_answer/", data)
    # 
    print(f"User answer3: {r.json()['robotResponse']}")

#
#   test_create_guest_session
#
def test_create_guest_session1():
    data={"username": "abcd1234", "age": "no", "language": "en"}
    r = requests.get("http://127.0.0.1:8000/api/create_guest_session/", data)
    #
    print(f"User answer: {r.json()['userinfo']}")

#
#   test_get_popular_movies
#
def test_get_popular_movies1():
    data={"top_n": 10, "page": 3} 
    r = requests.get("http://127.0.0.1:8000/api/get_popular_movies/", data)
    #
    if "movieList" in r.content.decode("utf-8") :
        print(f"User answer: passed this test case")
    else:
        print(f"User answer: failed this test case")

def test_get_popular_movies2():
    data={"top_n": 0, "page": 3} 
    r = requests.get("http://127.0.0.1:8000/api/get_popular_movies/", data)
    #
    if "movieList" in r.content.decode("utf-8") :
        print(f"User answer: passed this test case")
    else:
        print(f"User answer: failed this test case")

def test_get_popular_movies3():
    data={"top_n": 10000000, "page": 3} 
    r = requests.get("http://127.0.0.1:8000/api/get_popular_movies/", data)
    #
    if "movieList" in r.content.decode("utf-8") :
        print(f"User answer: passed this test case")
    else:
        print(f"User answer: failed this test case")

#
#   test_get_user_info
#
def test_get_user_info1():
    data={} 
    r = requests.get("http://127.0.0.1:8000/api/get_user_info/", data)
    print(f"User answer username: {r.json()['username']}")

#
#   test_get_latest_movie
#
def test_get_latest_movie1():
    r = requests.get("http://127.0.0.1:8000/api/get_latest_movie/")
    #
    if "movieList" in r.content.decode("utf-8") :
        print(f"User answer: passed this test case")
    else:
        print(f"User answer: failed this test case")

#
#   test_get_upcoming_movie
#
def test_get_upcoming_movie1():
    r = requests.get("http://127.0.0.1:8000/api/get_upcoming_movie/")
    #
    if "movieList" in r.content.decode("utf-8") :
        print(f"User answer: passed this test case")
    else:
        print(f"User answer: failed this test case")

#
#   test_get_similar_movie
#
def test_get_similar_movies1():
    data={"movie_id": 0, "page": 2} 
    r = requests.get("http://127.0.0.1:8000/api/get_similar_movies/", data)
    #
    if "movieList" in r.content.decode("utf-8") :
        print(f"User answer: passed this test case")
    else:
        print(f"User answer: failed this test case")

def test_get_similar_movies2():
    data={"movie_id": 100, "page": 3} 
    r = requests.get("http://127.0.0.1:8000/api/get_similar_movies/", data)
    #
    if "movieList" in r.content.decode("utf-8") :
        print(f"User answer: passed this test case")
    else:
        print(f"User answer: failed this test case")

def test_get_similar_movies3():
    data={"movie_id": 100000000000, "page": 2} 
    r = requests.get("http://127.0.0.1:8000/api/get_similar_movies/", data)
    #
    if "movieList" in r.content.decode("utf-8") :
        print(f"User answer: passed this test case")
    else:
        print(f"User answer: failed this test case")

#
#   test_get_recommendation_for_movie DOES NOT WORK
#
def test_get_recommendation_for_movies1():
    data={"movie_id": 550, "page": 1} 
    r = requests.get("http://127.0.0.1:8000/api/get_recommendation_for_movies/", data)
    #
    if "movieList" in r.content.decode("utf-8") :
        print(f"User answer: passed this test case")
    else:
        print(f"User answer: failed this test case")

#
#   test_get_movie_by_id
#
def test_get_movie_by_id1():
    data={"movie_id": 1} 
    r = requests.get("http://127.0.0.1:8000/api/get_movie_by_id/", data)
    #
    if "movieList" in r.content.decode("utf-8") :
        print(f"User answer: passed this test case")
    else:
        print(f"User answer: failed this test case")

def test_get_movie_by_id2():
    data={"movie_id": 996} 
    r = requests.get("http://127.0.0.1:8000/api/get_movie_by_id/", data)
    #
    if "movieList" in r.content.decode("utf-8") :
        print(f"User answer: passed this test case")
    else:
        print(f"User answer: failed this test case")

def test_get_movie_by_id3():
    data={"movie_id": 123123123123} 
    r = requests.get("http://127.0.0.1:8000/api/get_movie_by_id/", data)
    #
    if "movieList" in r.content.decode("utf-8") :
        print(f"User answer: passed this test case")
    else:
        print(f"User answer: failed this test case")

#
#   test_get_movie_trailer_link
#
def test_get_movie_trailer_link1():
    data={"movie_id": 550} 
    r = requests.get("http://127.0.0.1:8000/api/get_movie_trailer_link/", data)
    #
    if "youtube" in r.content.decode("utf-8") :
        print(f"User answer: {r.content}")
    else:
        print(f"User answer: failed this test case")

def test_get_movie_trailer_link2():
    data={"movie_id": 230} 
    r = requests.get("http://127.0.0.1:8000/api/get_movie_trailer_link/", data)
    #
    if "youtube" in r.content.decode("utf-8"):
        print(f"User answer: {r.content}")
    else:
        print(f"User answer: failed this test case")

#
#   __main__
#
if __name__ == '__main__':

    print(f"======test_post_answer is shown below======")
    test_post_answer1()
    test_post_answer2()
    test_post_answer3()

    print(f"======test_create_guest_session is shown below======")
    test_create_guest_session1()

    print(f"======test_get_popular_movies is shown below======")
    test_get_popular_movies1()
    test_get_popular_movies2()
    test_get_popular_movies3()

    print(f"======test_get_user_info is shown below======")
    test_get_user_info1()

    print(f"======test_get_latest_movie is shown below======")
    test_get_latest_movie1()

    print(f"======test_get_upcoming_movie is shown below======")
    test_get_upcoming_movie1()

    print(f"======test_get_similar_movie is shown below======")
    test_get_similar_movies1()
    test_get_similar_movies2()
    test_get_similar_movies3()

    print(f"======test_get_recommendation_for_movie is shown below======") # DOES NOT WORK
    test_get_recommendation_for_movies1()

    print(f"======test_get_movie_by_id is shown below======")
    test_get_movie_by_id1()
    test_get_movie_by_id2()
    test_get_movie_by_id3()

    print(f"======test_get_movie_trailer_link is shown below======")
    test_get_movie_trailer_link1()
    test_get_movie_trailer_link2()
    


