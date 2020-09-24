import urllib3, requests, json

class TMDB_assistant():
    
    bearer_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwMjgzNDgzM2E5ZGZlMjlkYzJjNTVlYjcwN2M1YTczYyIsInN1YiI6IjVmNTE4YjEyNWFhZGM0MDAzMzY3MDZhNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vExhd12qTYMuJPzRMRCQE9_W63_ReWbv98ANIdXb5jc"
    
    def __init__(self, api_key="02834833a9dfe29dc2c55eb707c5a73c", language="en-US"):
        self.api_key = api_key
        self.language = language

    def get_popular_movie(self, top_n=10):
        """
            Argument: 
                top_n: int, the number of movie you want to retrive
            Return:
                a list of top_n movie, each movie is constructed with a dictionary, e.g., 
                {'popularity': 2699.389, 'vote_count': 0, 'video': False, 'poster_path': '/6CoRTJTmijhBLJTUNoVSUNxZMEI.jpg', 'id': 694919, 'adult': False, 'backdrop_path': '/9Y12EdkIVvYir3uTcZGjqfXWBUv.jpg', 'original_language': 'en', 'original_title': 'Money Plane', 'genre_ids': [28], 'title': 'Money Plane', 'vote_average': 0, 'overview': "A professional thief with $40 million in debt and his family's life on the line must commit one final heist - rob a futuristic airborne casino filled with the world's most dangerous criminals.", 'release_date': '2020-09-29'}
        """
        # Get a list of recommended movies for a movie.
        query_url = "https://api.themoviedb.org/3/movie/popular?api_key="+self.api_key +"&language="+self.language+"&page=1"
        r = requests.get(query_url)
        json_data = r.json()
        parse_data = json.dumps(json_data, indent=4, sort_keys=True)    # conver json to str for pretty format

        # Extract 10 movie from response:
        movie_list = json_data["results"]
        top_n_list = movie_list[:top_n]
        return top_n_list


if __name__ == '__main__':
    TMDB_assistant = TMDB_assistant()
    top_n = 10
    top_n_list = TMDB_assistant.get_popular_movie(top_n)

    print(type(top_n_list))
    print(len(top_n_list))
    print(top_n_list[0])