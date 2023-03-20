from unittest.mock import Mock
from tmdb_client import *

def test_call_tmdb_api_endpoint(monkeypatch):
    movie_id = 1
    endpoint = f'movie/{movie_id}'
    mock_url = f'https://api.themoviedb.org/3/{endpoint}'
    required_url = f'https://api.themoviedb.org/3/movie/1'
    
    mock_request = Mock()
    response = mock_request.return_value
    response.json.return_value = mock_url
    monkeypatch.setattr('tmdb_client.requests.get', mock_request)
    
    result = call_tmdb_api(endpoint)
    assert required_url == result

def test_get_single_movie(monkeypatch):
    mock_movie_details = {'a':'1'}
    
    mock = Mock()
    mock.return_value = mock_movie_details
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock)

    movie_details = get_single_movie(movie_id = 1)
    assert movie_details == mock_movie_details

def test_get_single_movie_images(monkeypatch):
    mock_images_data = {'id':15,
                        "backdrops":[{'a':'1'}],
                        "posters":[{'a':'1'}]}
    mock = Mock()
    mock.return_value = mock_images_data
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock)

    result = get_single_movie_images(movie_id = 1)
    assert type(result) is list
    
def test_get_single_movie_cast(monkeypatch):
    mock_cast = {'cast':['Actor_1','Actor_2','Actor_3']}
    mock = Mock()
    mock.return_value = mock_cast
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock)

    result = get_single_movie_cast(movie_id = 1)
    assert mock_cast['cast'] == result

