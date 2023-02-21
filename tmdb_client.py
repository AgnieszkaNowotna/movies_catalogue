from random import randrange
import requests


def get_popular_movies():
    endpoint = 'https://api.themoviedb.org/3/movie/popular'
    api_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMjY5NzQzNDdmOTFlNzQ2NWQ5YjViM2M3ZDVkM2ExMSIsInN1YiI6IjYzZjM0ZjA0YTI0YzUwMDA4MDBjYzYzNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.QSwOJ5NE30GFESKOCx00kGxEHl5DFJ5EruMWHiAb65k'
    headers = {'Authorization': f'Bearer {api_token}'}
    response = requests.get (endpoint, headers = headers)
    return response.json()

def get_poster_url(poster_api_path, size = 'w342'):
    base_url = 'https://image.tmdb.org/t/p/' 
    url = f'{base_url}{size}/{poster_api_path}'
    return url

def get_movies(how_many):
    data = get_popular_movies()
    return data["results"][:how_many]

def get_random_movies(how_many):
    data = []
    movies = get_popular_movies()['results']
    for i in range (how_many):
        position = randrange(len(movies))
        data.append(movies[position])
        movies.remove(movies[position])
    return data