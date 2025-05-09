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
