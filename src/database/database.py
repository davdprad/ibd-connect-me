import mysql.connector as connector
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection, MySQLCursor

class Database:
    """
    Database class responsible for connecting to, querying, and manipulating the MySQL database.
    """

    # Database configuration settings
    config = {
        'user': 'ibd',
        'password': 'ibd',
        'host': 'localhost',
        'database': 'connect_me',
        'port': 3306
    }
    
    # Instance variables for the database connection and cursor
    conn: MySQLConnection
    cursor: MySQLCursor

    def open_connection(self):
        """
        Opens a connection to the MySQL database using the provided configuration.
        """
        try:
            self.conn = connector.connect(**self.config)
            self.cursor = self.conn.cursor()
        except Error as e:
            print(f'Error connecting to the database: {e}')
        else:
            print('Database connection successfully!')

    def close_connection(self):
        """
        Close a connection to the MySQL database.
        """
        try:
            self.conn.close()
            self.cursor.close()
        except Error as e:
            print(f'Error to close connection: {e}')
        else:
            print('Connection closed successfully!')

    def execute_query(self, query: str, params: list = None):
        """
        Execute a query against the MySQL database
        
        Params:
            query (str): An SQL query to be executed.
            params (tuple, optional): Parameters for executing the query. The default is None.
        """
        try:
            if params:
                for param in params:
                    self.cursor.execute(query, param)
            else:
                self.cursor.execute(query)

            if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE", "DROP")):
                self.conn.commit()
                print("Query executed and changes committed successfully!")
            elif query.strip().upper().startswith(("SELECT", "SHOW")):
                results = self.cursor.fetchall()
                print("Query executed successfully!")
                return results
            
        except Error as e:
            print(f"Error executing the query: {e}")
