from datamanager.data_manager import db, SQLiteDataManager, User, Movie
import os
from flask import Flask

def setup_test_db():
    """Set up a temporary SQLite database for testing."""
    db_file_name = "test_tape_deck.db"
    if os.path.exists(db_file_name):
        os.remove(db_file_name)

    # Create a minimal Flask app
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Create the database tables within the app context
    with app.app_context():
        db.drop_all()  # Drop all tables to ensure a clean slate
        db.create_all()

    return SQLiteDataManager(db_file_name), app

import unittest

class TestDataManager(unittest.TestCase):
    def setUp(self):
        """Set up the test database and app context before each test."""
        self.data_manager, self.app = setup_test_db()

    def test_add_and_get_all_users(self):
        """Test adding a user and retrieving all users."""
        with self.app.app_context():
            user = User(name="Test User")
            self.data_manager.add_user(user)
            users = self.data_manager.get_all_users()
            self.assertEqual(len(users), 1)
            self.assertEqual(users[0].name, "Test User")

    def test_add_and_get_user_movies(self):
        """Test adding movies and retrieving them for a specific user."""
        with self.app.app_context():
            user = User(name="Movie Lover")
            self.data_manager.add_user(user)
            user_id = self.data_manager.get_all_users()[0].id

            movie1 = Movie(name="Inception", director="Christopher Nolan", year=2010, rating=4.8, user_id=user_id)
            movie2 = Movie(name="The Matrix", director="The Wachowskis", year=1999, rating=4.7, user_id=user_id)
            self.data_manager.add_movie(movie1)
            self.data_manager.add_movie(movie2)

            movies = self.data_manager.get_user_movies(user_id)
            self.assertEqual(len(movies), 2)
            self.assertEqual(movies[0].name, "Inception")
            self.assertEqual(movies[1].name, "The Matrix")

    def test_update_movie(self):
        """Test updating a movie's details."""
        with self.app.app_context():
            user = User(name="Editor")
            self.data_manager.add_user(user)
            user_id = self.data_manager.get_all_users()[0].id

            movie = Movie(name="Old Title", director="Unknown", year=2000, rating=3.0, user_id=user_id)
            self.data_manager.add_movie(movie)
            movie_to_update = self.data_manager.get_user_movies(user_id)[0]

            movie_to_update.name = "New Title"
            movie_to_update.director = "Famous Director"
            movie_to_update.year = 2022
            movie_to_update.rating = 4.5
            self.data_manager.update_movie(movie_to_update)

            updated_movie = self.data_manager.get_user_movies(user_id)[0]
            self.assertEqual(updated_movie.name, "New Title")
            self.assertEqual(updated_movie.director, "Famous Director")
            self.assertEqual(updated_movie.year, 2022)
            self.assertEqual(updated_movie.rating, 4.5)

    def test_delete_movie(self):
        """Test deleting a movie from the database."""
        with self.app.app_context():
            user = User(name="Deleter")
            self.data_manager.add_user(user)
            user_id = self.data_manager.get_all_users()[0].id

            movie = Movie(name="To Be Deleted", director="Director", year=2020, rating=3.5, user_id=user_id)
            self.data_manager.add_movie(movie)
            movie_id = self.data_manager.get_user_movies(user_id)[0].id

            self.data_manager.delete_movie(movie_id)
            movies = self.data_manager.get_user_movies(user_id)
            self.assertEqual(len(movies), 0)

if __name__ == "__main__":
    unittest.main()
