import urllib3, requests, json

class TMDB_assistant():
    
    def __init__(self, api_key="02834833a9dfe29dc2c55eb707c5a73c", language="en-US"):
        print("TMDB_assistant created!")
        self.api_key = api_key
        self.language = language
        # genres_list: A dict, with two item: id and name, e.g. {"id": 35 "name": "Comedy"}
        genres_list = self.get_all_genres()   

    def get_permissions_link(self):
        query_str = "https://api.themoviedb.org/3/authentication/token/new?api_key=" +self.api_key
        r = requests.get(query_str)
        tmp_token = r.json()["request_token"]
        url = "https://www.themoviedb.org/authenticate/"+tmp_token
        return url, tmp_token
    
    # def create_user_session(self):
    #     new_session_url =  "https://api.themoviedb.org/3/authentication/session/new?api_key="+self.api_key
    #     payload = {
    #         "request_token": tmp_token
    #     }
    #     response = requests.post(new_session_url, json=payload)
    #     session_id = response.json()["session_id"]
    #     return session_id

    def create_guest_session(self):
        url =  "https://api.themoviedb.org/3/authentication/guest_session/new?api_key="+self.api_key
        r = requests.get(url)
        json_data = r.json()
        success = json_data["success"]
        guest_session_id = json_data["guest_session_id"]
        expires_at = json_data["expires_at"]
        return success, guest_session_id, expires_at

    def create_a_list(self, session_id):
        url =  "https://api.themoviedb.org/3/list?api_key="+self.api_key+"&session_id="+session_id
        payload = {
            "name": "This is my awesome test list.",
            "description": "Just an awesome list dawg.",
            "language": "en"
        }
        # header = {'Content-Type': 'application/json;charset=utf-8'}
        response = requests.post(url, json=payload)
        text = response.json()
        print("Json data for post: ", text)

    def rate_a_movie(self, movie_id, session_id, rating_value):
        url = "https://api.themoviedb.org/3/movie/"+str(movie_id)+"/rating?api_key="+self.api_key+"&guest_session_id="+session_id
        payload = {
            "value": rating_value
            }
        # header = {'Content-Type': 'application/json;charset=utf-8'}
        response = requests.post(url, json=payload)
        json_data = response.json()
        return json_data

    def add_to_watchlist(self):
        raise NotImplementedError


    # Referebce: 1) Selenium tutorial: https://www.youtube.com/watch?v=oM-yAjUGO-E 2) Session Object feature in Requests, https://requests.readthedocs.io/en/master/user/advanced/
    def create_user_session_in_onestep(self):
        # Step1: Create a request token
        query_str = "https://api.themoviedb.org/3/authentication/token/new?api_key=" +self.api_key
        r = requests.get(query_str)
        # This is a temporary token that is required to ask the user for permission to access their account. This token will auto expire after 60 minutes if it's not used.
        tmp_token = r.json()["request_token"]     # get json object
        print(r.json())
        print(tmp_token)
        # Step2: Ask the user for permission
        # 1) With a request token in hand, forward your user to the following URL: https://www.themoviedb.org/authenticate/{REQUEST_TOKEN}
        # 2) You can also pass this URL a redirect_to parameter, ie: https://www.themoviedb.org/authenticate/{REQUEST_TOKEN}?redirect_to=http://www.yourapp.com/approved
        # Get a list of genres for movies
        import webbrowser
        import time
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        url = "https://www.themoviedb.org/authenticate/"+tmp_token
        # driver = webdriver.Chrome()
        # driver.get(url)
        # driver.implicitly_wait(10) # seconds
        # driver.quit()

        time.sleep(5)
        webbrowser.open_new_tab(url)
        # query_url = "https://www.themoviedb.org/authenticate/"+tmp_token+"allow"
        # r = requests.get(query_url)
        # # json_data = r.json()
        # print("json_data = response.json(): ", r.headers)

        # Step 3: Create a new sesion_id with the authorized request token
        new_session_url =  "https://api.themoviedb.org/3/authentication/session/new?api_key="+self.api_key
        payload = {
            "request_token": tmp_token
        }
        # header = {'Content-Type': 'application/json;charset=utf-8', 'Authorization': 'Bearer ' + tmp_token}
        response = requests.post(new_session_url, json=payload)
        # Get the json data
        text = response.json()
        print("Json data for post: ", text)
        # Display the session ID
        session_id = response.json()["session_id"]
        print("The session ID: ", session_id)

        return tmp_token, session_id


    # Get the list of official genres for movies
    def get_all_genres(self):
        url = "https://api.themoviedb.org/3/genre/movie/list?api_key="+self.api_key+ "&language="+ self.language
        r = requests.get(url)
        json_data = r.json()
        return json_data.get('genres')
    
    def set_language(self, language):
        self.language = language

    # Given a movie json_object, return it's original_title link as str
    def get_movie_title(self, json_object):
        result = json_object.get("original_title")
        if result==None:
            print("Error in get_movie_title: original_title doesn't exist!")
        return result
        
    # Given a movie json_object, return it's homepage link as str
    def get_movie_homepage(self, json_object):
        result = json_object.get("homepage")
        if result==None:
            print("Error in get_movie_homepage: homepage doesn't exist!")
        return result
    
    # Given a movie json_object, return it's decription link as str
    def get_movie_overview(self, json_object):
        result = json_object.get("overview")
        if result==None:
            print("Error in get_movie_overview: overview doesn't exist!")
        return result

    def get_movie_avatar_link(self, json_object):
        result = json_object.get("poster_path")
        if result==None:
            print("Error in get_movie_avatar_link: poster_path doesn't exist!")
        path = "https://image.tmdb.org/t/p/w220_and_h330_face/" + result
        # path = "https://image.tmdb.org/t/p/w600_and_h900_bestv2/" + result
        # Example: https://image.tmdb.org/t/p/w220_and_h330_face/6CoRTJTmijhBLJTUNoVSUNxZMEI.jpg
        return (path)

    def get_movie_trailer_link(self, movie_id):
        url = "https://api.themoviedb.org/3/movie/" + str(movie_id) +"/videos?api_key="+self.api_key+"&language=en"
        r = requests.get(url)
        json_data = r.json()
        key = json_data.get("results")[0].get("key")
        if key==None:
            print("Error in get_movie_trailer_link: key trailer_link doesn't exist!")
        # root_path = "https://www.themoviedb.org/movie/"
        # movie_title = self.get_movie_title(json_object)
        # movie_title = movie_title.lower().strip().replace(" ", "-")
        # path = root_path + str(movie_id) + "-" + movie_title + "#play=" + key
        path = "https://www.youtube.com/watch?v="+key+"&feature=emb_title"
        # https://www.youtube.com/watch?v=aETz_dRDEys&feature=emb_title
        # https://www.themoviedb.org/movie/694919-money-plane#play=aETz_dRDEys
        # https://www.themoviedb.org/movie/734309-santana#play=CdkxJ8BD0EI
        # https://www.youtube.com/watch?v=aETz_dRDEys&feature=emb_title
        return (path)
    
    def get_movie_id(self, json_object):
        result = json_object.get("id")
        if result==None:
            print("Error in get_id_by_movie: id doesn't exist!")
        return result

    def is_adult_movie(self, json_object):
        result = json_object.get("adult")
        if result==None:
            print("Error in is_adult_movie: adult doesn't exist!")
        return result

    # ------------------------------------TMDB API call ---------------------
    # Reference: https://developers.themoviedb.org/3/search/search-keywords
    def search_movie_by_keyword(self, keyword, page=1):
        query_url = "https://api.themoviedb.org/3/search/keyword?api_key="+self.api_key+"&query="+keyword+"&page="+str(page)
        response = requests.get(query_url)    # Get response message
        json_data = response.json()
        return json_data

    def get_movie_by_id(self, movie_id:int):
        query_url = "https://api.themoviedb.org/3/movie/"+str(movie_id)+"?api_key="+self.api_key
        response = requests.get(query_url)    # Get response message
        json_data = response.json()
        return json_data

    def get_popular_movies(self, top_n=10, page=1):
        """
            Argument: 
                top_n: int, the number of movie you want to retrive
            Return:
                a list of top_n movie, each movie is constructed with a dictionary, e.g., 
                {'popularity': 2699.389, 'vote_count': 0, 'video': False, 'poster_path': '/6CoRTJTmijhBLJTUNoVSUNxZMEI.jpg', 'id': 694919, 'adult': False, 'backdrop_path': '/9Y12EdkIVvYir3uTcZGjqfXWBUv.jpg', 'original_language': 'en', 'original_title': 'Money Plane', 'genre_ids': [28], 'title': 'Money Plane', 'vote_average': 0, 'overview': "A professional thief with $40 million in debt and his family's life on the line must commit one final heist - rob a futuristic airborne casino filled with the world's most dangerous criminals.", 'release_date': '2020-09-29'}
        """
        query_url = "https://api.themoviedb.org/3/movie/popular?api_key="+self.api_key +"&language="+self.language+"&page="+str(page)
        response = requests.get(query_url)
        json_data = response.json()
        # Extract 10 movie from response:
        top_n_list = json_data["results"][:top_n]
        return top_n_list

    def get_recommendation_for_movie(self, movie_id:int, page=1):
        query_url = "https://api.themoviedb.org/3/movie/"+str(movie_id)+"/recommendations?api_key="+self.api_key+"&language="+self.language+"&page="+str(page)
        r = requests.get(query_url)
        json_data = r.json()
        return json_data

    def get_similar_movies(self, movie_id:int, page=1):
        query_url = "https://api.themoviedb.org/3/movie/"+str(movie_id)+"/recommendations?api_key="+self.api_key+"&language="+self.language+"&page="+str(page)
        r = requests.get(query_url)
        json_data = r.json()
        return json_data
    
    def discover_movies(self, page, sort_by="popularity.desc", gener_id="28"):
        """Discover
            Argument:
                language: str, default "en-US"
                sort_by: str, choose one, [popularity.asc, popularity.desc, release_date.desc, release_date.desc, vote_average.asc, vote_average.asc, vote_count.asc, vote_count.desc]
                include_adult: boolean, default False
                with_genres: str, what genre want to search for?
                with_keyword: str, what keyword want to search for?
                with_people: str, what character you want to watch?
        """
        query_url = "https://api.themoviedb.org/3/discover/movie?api_key="+self.api_key+"&language="+self.language+"&sort_by=popularity.desc&include_adult=false&include_video=false&page="+str(page)+"&with_genres="+str(gener_id)
        r = requests.get(query_url)
        json_data = r.json()
        return json_data
        

    # Get the most newly created movie. This is a live response and will continuously change.
    def get_latest_movie(self):
        query_url = "https://api.themoviedb.org/3/movie/latest?api_key="+self.api_key + "&language="+self.language
        r = requests.get(query_url)
        json_data = r.json()
        return json_data

    def get_upcoming_movie(self, page=1):
        query_url = "https://api.themoviedb.org/3/movie/upcoming?api_key="+self.api_key +"&language="+self.language+"US&page="+str(page)
        r = requests.get(query_url)
        json_data = r.json()
        return json_data


class TMDB_guest_session(TMDB_assistant):
    def __init__(self):
        TMDB_assistant.__init__(self)
        print("TMDB_guess_session Created!")

    def create_guest_session(self):
        pass

    def get_rated_movies(self):
        pass

    def set_movie_list(self):
        pass

    def delete_movie_list(self):
        pass

    def add_movie_to_list(self, movie):
        pass

    def delete_movie_from_list(self):
        pass
    


if __name__ == '__main__':
    api_key="02834833a9dfe29dc2c55eb707c5a73c"
    TMDB_assistant = TMDB_assistant(api_key, "en-US")
    # tmp_token = TMDB_assistant.create_user_session()

    # print(type(TMDB_assistant))
# Test get_popular_movie
    # print("Testing: get_popular_movies")
    top_n = 10
    top_n_list = TMDB_assistant.get_popular_movies(top_n)
    print(type(top_n_list))
    print(len(top_n_list))
    # top1 = json.dumps(top_n_list[0], indent=4, sort_keys=True)
    top1 = top_n_list[2]
    # print(top_n_list)
# Test genres_list:
    # print("Testing: get_popular_movies")
    # print(TMDB_assistant.genres_list)

# Test get_latest_movies
    # print("Testing: get_latest_movies")
    # latest_movie = TMDB_assistant.get_latest_movie()
    # print(latest_movie)

# Test discover_movies:
    print("Testing: discover_movies based on given genre")
    movie_list = TMDB_assistant.discover_movies(page=100, gener_id=28)
    print(movie_list)

# Test get_movie_by_id 
    print("Testing: get_movie_by_id")
    movie_id = 550
    movie_550 = TMDB_assistant.get_movie_by_id(movie_id)
    # print(json.dumps(movie_550, indent=4, sort_keys=True))
    # print(type(movie_550))
    # print(len(movie_550))

    # get movie description
    overview = TMDB_assistant.get_movie_overview(top1)
    # print(f"overview: {overview}")

    # get movie avatar_link
    avatar_link = TMDB_assistant.get_movie_avatar_link(top1)
    # print(f"avatar_link: {avatar_link}")

    # get movie trailer_link
    trailer_link = TMDB_assistant.get_movie_trailer_link(top1)
    # print(f"trailer_link: {trailer_link}")

# Test get_n_recommendation_for_movie 
    # movid_id = 550
    # top_n = 2
    # recommendation = TMDB_assistant.get_n_recommendation_for_movie(movid_id)
    # top_n_list = recommendation["results"][:top_n]
    # print("Show Result: ")
    # print(type(top_n_list))
    # print(f"number of recommendations: {len(top_n_list)}")
    # print(json.dumps(top_n_list, indent=4))

