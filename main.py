from flask import Flask, render_template, request, redirect,url_for, flash
from datetime import datetime
import tmdb_client

app = Flask(__name__)
app.secret_key = b'secret'

FAVOURITES = []

@app.route('/')
def homepage():
    movie_types = ['now_playing','popular','top_rated','upcoming']
    selected_list = tmdb_client.get_list_type(movie_types)
    movies = tmdb_client.get_random_movies(how_many = 8, list_name = selected_list)
    return render_template("homepage.html", movies = movies, movie_types = movie_types, selected_list = selected_list)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    image = tmdb_client.get_random_movie_image(movie_id)
    return render_template("movie_details.html", movie = details, cast=cast, image=image)

@app.route('/search')
def search():
    search_query = request.args['q']
    search_list = tmdb_client.get_wanted_movies(search_query)[:12]
    sorted_list = sorted(search_list, key=lambda movie : movie['popularity'])[::-1]
    return render_template('search.html', search_list = sorted_list, search_query=search_query)

@app.route('/movie/today')
def movie_today():
    today = datetime.now().strftime('%d.%m.%Y')
    today_list = tmdb_client.get_today_tv()
    return render_template('today_show.html', today_list = today_list, today=today)

@app.route('/favourites')
def show_favourites():
    favourites_movies = []
    for movie_id in FAVOURITES:
        movie = tmdb_client.get_single_movie(movie_id)
        favourites_movies.append(movie)
    return render_template('favourites.html', movie_list = favourites_movies, lenght = len(favourites_movies))

@app.route('/favourites/add', methods = ['POST'])
def add_to_favourites():
    data = request.form
    movie_id = data.get('movie_id')
    if movie_id:
        for movie in FAVOURITES:
            if movie == movie_id:
                return redirect(url_for('homepage'))
        FAVOURITES.append(movie_id)
        title = tmdb_client.get_single_movie(movie_id)['title']
        flash (f'{title} has been added to your favourite list')
    return redirect(url_for('homepage'))

@app.context_processor
def utility_processor():
    def tmdb_image_url(path,size):
        return tmdb_client.get_poster_url(path, size)
    return{"tmdb_image_url":tmdb_image_url}

if __name__ == "__main__":
    app.run(debug=True)