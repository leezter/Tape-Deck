from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    @abstractmethod
    def get_all_users(self):
        """ 
        Retrieve all users from the data source. 
        """
        pass


    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Retrieve all movies for a specific user by their ID.
        """
        pass


    @abstractmethod
    def add_user(self, user):
        """
        Add a new user to the data source.
        """
        pass


    @abstractmethod
    def add_movie(self, movie):
        """
        Add a new movie to the data source.
        """
        pass


    @abstractmethod
    def update_movie(self, movie):
        """
        Update the details of a specific movie in the data source.
        """
        pass


    @abstractmethod
    def delete_movie(self, movie_id):
        """
        Delete a specific movie from the data source.
        """
        pass
