import getpass
from pymongo.errors import OperationFailure
from mongoengine import *


class Utilities:
    """I have several variations on a theme in this project, and each one will need to start up
    with the same MongoDB database.  So I'm putting any sort of random little utilities in here
    as I need them.

    startup - creates the connection and returns the database client."""

    @staticmethod
    def startup():
        print("Prompting for the password.")
        while True:
            password = getpass.getpass(prompt='MongoDB password --> ')
            cluster = f"mongodb+srv://CECS-323-Spring-2024-User:{password}@cluster0.uhlmij5.mongodb.net/?retryWrites=true&w=majority"
            database_name = input('Database name to use --> ')
            client = connect(db=database_name, host=cluster)
            try:
                junk = client.server_info()  # Test the connection
                return client
            except OperationFailure as OE:
                print(OE)
                print("Error, invalid password.  Try again.")
