from sqlalchemy import Column, Integer, String, Float, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from datamanager.data_manager_interface import DataManagerInterface

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    director = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    cover_image = Column(String, nullable=True)


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.db = db
        self.db_file_name = db_file_name


    def get_all_users(self):
        """
        Retrieve all users from the database.
        """
        try:
            users = self.db.session.query(User).all()
            print(f"Retrieved users: {users}")
            return users
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return []


    def list_all_users(self):
        """
        Alias for get_all_users to match route naming.
        """
        return self.get_all_users()


    def get_user_movies(self, user_id):
        """
        Retrieve all movies for a specific user by their ID.
        """
        return self.db.session.query(Movie).filter_by(user_id=user_id).all()


    def add_user(self, user):
        """
        Add a new user to the database.
        """
        try:
            print(f"Adding user: {user}")
            self.db.session.add(user)
            self.db.session.commit()
            print("User added successfully.")
        except Exception as e:
            self.db.session.rollback()
            print(f"Error adding user: {e}")


    def add_movie(self, movie):
        """
        Add a new movie to the database.
        """
        self.db.session.add(movie)
        self.db.session.commit()


    def update_movie(self, movie):
        """
        Update the details of a specific movie in the database.
        """
        self.db.session.merge(movie)
        self.db.session.commit()


    def delete_movie(self, movie_id):
        """
        Delete a specific movie from the database.
        """
        session = self.db.session
        try:
            movie = session.query(Movie).filter_by(id=movie_id).first()
            if movie:
                session.delete(movie)
                session.commit()
            else:
                print(f"Movie with id {movie_id} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error deleting movie: {e}")
        finally:
            session.close()
