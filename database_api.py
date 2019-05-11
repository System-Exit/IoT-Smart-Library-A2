import MySQLdb
import json


class GoogleDatabaseAPI:
    def __init__(self):
        """
        Constructor for google database API
        Reads config file for database details

        """
        # Load config file to get database details
        with open("gdb_config.json", "r") as jsonFile:
            config = json.load(jsonFile)
            host = config["host"]
            user = config["user"]
            password = config["password"]
            database = config["database"]

        # Create connection to database
        self.__connection = MySQLdb.connect(host, user, password, database)

    def execute_parameterized_query(self, query):
        """
        Execute the specified query in the database and return the results

        Args:
            query (str): The query that will be executed on the database
            parameters (:obj:`tuple` of :obj:`str`): The parameters of the
                parameterized query

        Returns:
            The results of the query as a list of tuples

        """
        with self.__connection.cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchall()
