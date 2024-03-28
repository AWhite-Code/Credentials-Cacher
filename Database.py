import sqlite3
import os

class Database:
    def __init__(self):
        self.db_path = self.get_db_path()
        self.connection = self.connect_to_db()
        self.create_table()

    def get_db_path(self):
        app_data_path = os.getenv('APPDATA')  # Gets the AppData path
        db_directory = os.path.join(app_data_path, 'Credentials Cacher')  # Specify your app's name
        if not os.path.exists(db_directory):
            os.makedirs(db_directory)  # Creates the directory if it doesn't exist
        return os.path.join(db_directory, 'passwords.db')  # Path for the database file

    def connect_to_db(self):
        return sqlite3.connect(self.db_path)  # Establishes a connection to the SQLite database

    def create_table(self):
        cursor = self.connection.cursor()
        table_creation_query = """
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY,
            website_name TEXT NOT NULL,
            website_url TEXT,
            username TEXT NOT NULL,
            password BLOB NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(table_creation_query)
        self.connection.commit()  # Commits the CREATE TABLE operation
        
    def add_password_entry(self, website_name, website_url, username, password, notes):
        cursor = self.connection.cursor()
        query = """INSERT INTO vault (website_name, website_url, username, password, notes)
                VALUES (?, ?, ?, ?, ?);"""
        cursor.execute(query, (website_name, website_url, username, password, notes))
        self.connection.commit()
        
    def fetch_all_entries(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM vault;"
        cursor.execute(query)
        entries = cursor.fetchall()  # Fetches all rows of a query result, returning a list.
        return entries    
            
    def close_connection(self):
        if self.connection:
            self.connection.close()