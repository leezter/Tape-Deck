from flask import Flask, render_template, request, redirect, url_for
from datamanager.data_manager import SQLiteDataManager, User, Movie, db
import requests
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'moviwebapp.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

data_manager = SQLiteDataManager('moviwebapp.db')  

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/users')
def list_users():
    users = data_manager.list_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    user = next((u for u in data_manager.list_all_users() if u.id == user_id), None)
    if not user:
        return render_template('404.html'), 404

    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            data_manager.add_user(User(name=name))
            return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    user = next((u for u in data_manager.list_all_users() if u.id == user_id), None)
    if not user:
        return render_template('404.html'), 404

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            director = request.form.get('director')
            year = request.form.get('year')
            rating = request.form.get('rating')

            if name:
                # Fetch movie details from OMDb API
                api_key = "45ce7064"  # Replace with your actual OMDb API key
                response = requests.get(f"http://www.omdbapi.com/?t={name}&apikey={api_key}")
                response.raise_for_status()
                movie_data = response.json()
                cover_image = movie_data.get('Poster', '')

                # Use fetched data if available
                director = director or movie_data.get('Director', 'Unknown')
                year = year or movie_data.get('Year', 'Unknown')
                rating = rating or movie_data.get('imdbRating', '0')

                movie = Movie(
                    name=name,
                    director=director,
                    year=int(year) if year.isdigit() else 0,
                    rating=float(rating) if rating.replace('.', '', 1).isdigit() else 0.0,
                    cover_image=cover_image,
                    user_id=user_id
                )
                data_manager.add_movie(movie)
                return redirect(url_for('user_movies', user_id=user_id))
            else:
                return "Movie name is required.", 400
        except requests.exceptions.RequestException as e:
            return f"Failed to fetch movie details from OMDb API: {str(e)}", 500
        except Exception as e:
            return f"An error occurred: {str(e)}", 500

    return render_template('add_movie.html', user=user)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user = next((u for u in data_manager.list_all_users() if u.id == user_id), None)
    if not user:
        return "User not found", 404

    movie = next((m for m in data_manager.get_user_movies(user_id) if m.id == movie_id), None)
    if not movie:
        return "Movie not found", 404

    if request.method == 'POST':
        movie.name = request.form.get('name')
        movie.director = request.form.get('director')
        movie.year = int(request.form.get('year'))
        movie.rating = float(request.form.get('rating'))

        data_manager.update_movie(movie)
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('update_movie.html', user=user, movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    user = next((u for u in data_manager.list_all_users() if u.id == user_id), None)
    if not user:
        return "User not found", 404

    movie = next((m for m in data_manager.get_user_movies(user_id) if m.id == movie_id), None)
    if not movie:
        return "Movie not found", 404

    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
