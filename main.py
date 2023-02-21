from flask import Flask, render_template, request
import tmdb_client
app = Flask(__name__)

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

@app.context_processor
def utility_processor():
    def tmdb_image_url(path,size):
        return tmdb_client.get_poster_url(path, size)
    return{"tmdb_image_url":tmdb_image_url}

if __name__ == "__main__":
    app.run(debug=True)