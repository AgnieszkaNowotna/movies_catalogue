from main import app
from unittest.mock import Mock
import pytest

@pytest.mark.parametrize('list_type',(('now_playing'),('popular'), ('top_rated'), ('upcoming')))
def test_homepage(monkeypatch, list_type):
    api_mock = Mock(return_value = {'results':[{'id':1},{'id':2},{'id':3},{'id':4},{'id':5},{'id':6},{'id':7},{'id':8}]})
    monkeypatch.setattr('tmdb_client.call_tmdb_api', api_mock)

    mock_list_type = Mock(return_value = list_type)
    monkeypatch.setattr('tmdb_client.get_list_type', mock_list_type)

    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        api_mock.assert_called_once_with(f'movie/{list_type}')