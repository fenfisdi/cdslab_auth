from bson.objectid import ObjectId

from source.db import get_db_connection


def user_db():
    return get_db_connection().get_collection('user')


class UserInterface:

    @staticmethod
    def retrieve_user(*args, **kwargs) -> dict:
        """
            Search for a specific user inside the database

            Parameters
            ----------
            query: dict
                Key pair associated to the user

            Return
            ----------
            user: pymongo object
                Object containing the results of the search
        """
        return user_db().find_one(kwargs)

    @staticmethod
    def insert_user(data: dict):
        """
            Add user to the database

            Parameters
            ----------
            data: dict
                Information to add to the database

            Return
            ----------
            new_user: dict
                Codified information to add to the database
        """
        return user_db().insert_one(data)

    @staticmethod
    def update_user_state(data: dict, user_id: str):
        """
            Update user's status to active after verification

            Parameters
            ----------
            data: dict
                Key pair associated to a user

            user_id: str
                Unique id associated to a user

            Return
            ----------
            False:
                If user has no information
            False:
                If is not possible to update the user's status
            False:
                If the id doesn't match the one associated to the data parameter
            True:
                If the user has valid data and its status can be updated
        """
        if not bool(data):
            return False
        user = user_db().find_one({"_id": ObjectId(user_id)})
        if user:
            updated_user = user_db().update_one(
                {"_id": ObjectId(user_id)}, {"$set": data}
            )
            if updated_user:
                return True
        return False
