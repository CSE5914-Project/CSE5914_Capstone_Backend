import urllib3, requests, json

class TMDB_assistant():
    
    def __init__(self, api_key="02834833a9dfe29dc2c55eb707c5a73c", language="en-US"):
        print("TMDB_assistant created!")
        self.api_key = api_key
        self.language = language
        # genres_list: A dict, with two item: id and name, e.g. {"id": 35 "name": "Comedy"}
        self.genres_list = self.__get_all_genres()   

    # Get the list of official genres for movies
    def __get_all_genres(self):
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
        # Example: https://image.tmdb.org/t/p/w220_and_h330_face/6CoRTJTmijhBLJTUNoVSUNxZMEI.jpg
        return (path)

    def get_movie_trailer_link(self, json_object):
        movie_id = self.get_movie_id(json_object)
        url = "https://api.themoviedb.org/3/movie/" + str(movie_id) +"/videos?api_key="+self.api_key+"&language=en-US"
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

    # ------------------------------------API call ---------------------
    def get_movie_by_id(self, movie_id:int):
        query_url = "https://api.themoviedb.org/3/movie/"+str(movie_id)+"?api_key="+self.api_key
        response = requests.get(query_url)    # Get response message
        json_data = response.json()
        return json_data

    def get_popular_movies(self, top_n=10):
        """
            Argument: 
                top_n: int, the number of movie you want to retrive
            Return:
                a list of top_n movie, each movie is constructed with a dictionary, e.g., 
                {'popularity': 2699.389, 'vote_count': 0, 'video': False, 'poster_path': '/6CoRTJTmijhBLJTUNoVSUNxZMEI.jpg', 'id': 694919, 'adult': False, 'backdrop_path': '/9Y12EdkIVvYir3uTcZGjqfXWBUv.jpg', 'original_language': 'en', 'original_title': 'Money Plane', 'genre_ids': [28], 'title': 'Money Plane', 'vote_average': 0, 'overview': "A professional thief with $40 million in debt and his family's life on the line must commit one final heist - rob a futuristic airborne casino filled with the world's most dangerous criminals.", 'release_date': '2020-09-29'}
        """
        query_url = "https://api.themoviedb.org/3/movie/popular?api_key="+self.api_key +"&language="+self.language+"&page=1"
        response = requests.get(query_url)
        json_data = response.json()
        # Extract 10 movie from response:
        top_n_list = json_data["results"][:top_n]
        return top_n_list

    def get_n_recommendation_for_movie(self, movie_id:int):
        query_url = "https://api.themoviedb.org/3/movie/"+str(movie_id)+"/recommendations?api_key="+self.api_key+"&language=en-US&page=1"
        r = requests.get(query_url)
        json_data = r.json()
        return json_data

    def get_similar_movies(self, movie_id:int):
        query_url = "https://api.themoviedb.org/3/movie/"+str(movie_id)+"/recommendations?api_key="+self.api_key+"&language=en-US&page=1"
        r = requests.get(query_url)
        json_data = r.json()
        return json_data
    
    def discover_movies(self, sort_by="popularity.desc", genre="action"):
        """Discover
            Argument:
                language: str, default "en-US"
                sort_by: str, choose one, [popularity.asc, popularity.desc, release_date.desc, release_date.desc, vote_average.asc, vote_average.asc, vote_count.asc, vote_count.desc]
                include_adult: boolean, default False
                with_genres: str, what genre want to search for?
                with_keyword: str, what keyword want to search for?
                with_people: str, what character you want to watch?
        """
        query_url = "https://api.themoviedb.org/3/discover/movie?api_key=02834833a9dfe29dc2c55eb707c5a73c&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_people=Niki%20Caro&with_genres=action"
        r = requests.get(query_url)
        json_data = r.json()
        return json_data
        
        

    # Get the most newly created movie. This is a live response and will continuously change.
    def get_latest_movie(self):
        
        query_url = "https://api.themoviedb.org/3/movie/latest?api_key="+self.api_key + "&language=en-US"
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
    print(type(TMDB_assistant))
# Test get_popular_movie
    print("Testing: get_popular_movies")
    top_n = 10
    top_n_list = TMDB_assistant.get_popular_movies(top_n)
    print(type(top_n_list))
    print(len(top_n_list))
    # top1 = json.dumps(top_n_list[0], indent=4, sort_keys=True)
    top1 = top_n_list[2]
    print(top_n_list)
# Test genres_list:
    # print("Testing: get_popular_movies")
    # print(TMDB_assistant.genres_list)

# Test get_latest_movies
    # print("Testing: get_latest_movies")
    # latest_movie = TMDB_assistant.get_latest_movie()
    # print(latest_movie)


# Test get_movie_by_id 
    print("Testing: get_movie_by_id")
    movie_id = 550
    movie_550 = TMDB_assistant.get_movie_by_id(movie_id)
    # print(json.dumps(movie_550, indent=4, sort_keys=True))
    print(type(movie_550))
    print(len(movie_550))

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

