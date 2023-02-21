from flask import request
from random import randrange, choice
import requests
API_TOKEN = 'api token'

def get_popular_movies():
    endpoint = 'https://api.themoviedb.org/3/movie/popular'
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    response = requests.get (endpoint, headers = headers)
    return response.json()

def get_single_movie(movie_id):
    endpoint = f'https://api.themoviedb.org/3/movie/{movie_id}'
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    response = requests.get (endpoint, headers = headers)
    return response.json()

def get_single_movie_cast(movie_id):
    endpoint = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    response = requests.get (endpoint, headers = headers)
    return response.json()["cast"]

def get_single_movie_images(movie_id):
    endpoint = f'https://api.themoviedb.org/3//movie/{movie_id}/images'
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    response = requests.get (endpoint, headers = headers )
    return response.json()["backdrops"]

def get_movies_list(list_name = 'popular'):
    endpoint = f'https://api.themoviedb.org/3/movie/{list_name}'
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    response = requests.get (endpoint, headers = headers)
    response.raise_for_status()
    return response.json()

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