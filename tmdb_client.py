from flask import request
from random import randrange, choice
import requests, os
API_TOKEN = os.environ.get("TMDB_API_TOKEN", "")

def call_tmdb_api(endpoint):
    full_url = f'https://api.themoviedb.org/3/{endpoint}'
    headers = {
        "Authorization": f'Bearer {API_TOKEN}'
    }
    response = requests.get(full_url, headers = headers)
    response.raise_for_status()
    return response.json()

def get_single_movie(movie_id):
    return call_tmdb_api(f'movie/{movie_id}')

def get_single_movie_cast(movie_id):
    response = call_tmdb_api(f'movie/{movie_id}/credits')
    return response["cast"]   

def get_single_movie_images(movie_id):
    response = call_tmdb_api(f'/movie/{movie_id}/images?language=en,null')
    return response["backdrops"]

def get_movies_list(list_name = 'popular'):
    return call_tmdb_api(f'movie/{list_name}')

def get_wanted_movies(search_query):
    response = call_tmdb_api(f'search/movie?query={search_query}')
    return response['results']

def get_today_tv():
    response = call_tmdb_api(f'tv/airing_today?include_adult=false')
    return response['results']

def get_poster_url(poster_api_path, size = 'w342'):
    base_url = 'https://image.tmdb.org/t/p/' 
    url = f'{base_url}{size}/{poster_api_path}'
    return url

def get_movies(how_many, list_name = 'popular'):
    data = get_movies_list(list_name)
    return data["results"][:how_many]

def get_random_movies(how_many, list_name = 'popular'):
    data = []
    movies = get_movies_list(list_name)['results']
    for i in range (how_many):
        position = randrange(len(movies))
        data.append(movies[position])
        movies.remove(movies[position])
    return data

def get_random_movie_image(movie_id):
    image = choice(get_single_movie_images(movie_id))
    return image

def get_list_type(movie_types):
    for movie_type in movie_types:
        if request.args.get('list_type') == movie_type:
            return request.args.get('list_type', 'popular')
    return 'popular'
