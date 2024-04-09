import sqlite3
import os
from .Encryption import Encryption

class Database:
    def __init__(self):
        # Initialize database paths and connection
        self.db_path = self.get_db_path()
        self.salt_path = self.get_salt_path()
        self.connection = self.connect_to_db()
        self.create_table()
        self.initialize_salt()

    def get_db_path(self):
        """Determine the database file path in the application's AppData directory."""
        app_data_path = os.getenv('APPDATA')
        db_directory = os.path.join(app_data_path, 'Credentials Cacher')
        if not os.path.exists(db_directory):
            os.makedirs(db_directory)
        return os.path.join(db_directory, 'passwords.db')

    def get_salt_path(self):
        """Get the file path for the global salt used in encryption."""
        return os.path.join(os.path.dirname(self.db_path), 'global_salt.bin')

    def initialize_salt(self):
        """Create a new global salt file if it doesn't already exist."""
        if not os.path.exists(self.salt_path):
            salt = os.urandom(16)
            with open(self.salt_path, 'wb') as f:
                f.write(salt)

    def get_global_salt(self):
        """Retrieve the global salt from the file system."""
        with open(self.salt_path, 'rb') as f:
            return f.read()

    def connect_to_db(self):
        """Establish a SQLite database connection."""
        return sqlite3.connect(self.db_path)

    def create_table(self):
        """Create the main table for storing encrypted vault entries if it doesn't exist."""
        cursor = self.connection.cursor()
        table_creation_query = """
            CREATE TABLE IF NOT EXISTS vault (
                id INTEGER PRIMARY KEY,
                website_name TEXT NOT NULL,
                website_url TEXT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                notes TEXT,
                favourite INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );"""
        cursor.execute(table_creation_query)
        self.connection.commit()

    def delete_password_entry(self, entry_id):
        print(f"Attempting to delete entry with ID: {entry_id}, type: {type(entry_id)}")
        cursor = self.connection.cursor()
        if isinstance(entry_id, tuple):
            # If entry_id is a tuple, extract the first element assuming it's the correct ID.
            entry_id = entry_id[0]
        cursor.execute("DELETE FROM vault WHERE id = ?", (entry_id,))
        self.connection.commit()

    def add_password_entry(self, website_name, website_url, username, password, notes, encryption_key):
        """Add a new vault entry, encrypting the data with the provided encryption key."""
        encrypted_website_name = Encryption.encrypt_data(website_name, encryption_key)
        encrypted_website_url = Encryption.encrypt_data(website_url, encryption_key) if website_url else None
        encrypted_username = Encryption.encrypt_data(username, encryption_key)
        encrypted_password = Encryption.encrypt_data(password, encryption_key)
        encrypted_notes = Encryption.encrypt_data(notes, encryption_key) if notes else None
        
        cursor = self.connection.cursor()
        query = """INSERT INTO vault (website_name, website_url, username, password, notes)
                   VALUES (?, ?, ?, ?, ?);"""
        cursor.execute(query, (
            encrypted_website_name or '',
            encrypted_website_url or '',
            encrypted_username or '',
            encrypted_password or '',
            encrypted_notes or ''))
        self.connection.commit()
            
    def fetch_all_entries(self, encryption_key):
        """Fetch all vault entries, decrypting them with the given encryption key."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, website_name, website_url, username, password, notes, favourite, created_at, updated_at FROM vault;")
        encrypted_entries = cursor.fetchall()
        
        return self.decrypt_entries(encrypted_entries, encryption_key)

    def close_connection(self):
        """Safely close the database connection."""
        if self.connection:
            self.connection.close()
            
    def update_password_entry(self, id, website_name, website_url, username, password, notes, encryption_key):
        """Update an existing vault entry with new data, re-encrypting with the provided key."""
        encrypted_website_name = Encryption.encrypt_data(website_name, encryption_key)
        encrypted_website_url = Encryption.encrypt_data(website_url, encryption_key)
        encrypted_username = Encryption.encrypt_data(username, encryption_key)
        encrypted_password = Encryption.encrypt_data(password, encryption_key)
        encrypted_notes = Encryption.encrypt_data(notes, encryption_key)
        
        cursor = self.connection.cursor()
        query = """UPDATE vault SET website_name = ?, website_url = ?, username = ?, password = ?, notes = ?
                   WHERE id = ?;"""
        cursor.execute(query, (encrypted_website_name, encrypted_website_url, encrypted_username, encrypted_password, encrypted_notes, id))
        self.connection.commit()
        
        
    def toggle_favourite_status(self, entry_id, new_status):
        """Sets the current favourite value to the opposite"""
        new_status_int = 1 if new_status else 0
        
        cursor = self.connection.cursor()
        cursor.execute("UPDATE vault SET favourite = ? WHERE id = ?", (new_status_int, entry_id))
        self.connection.commit()
                    
    def fetch_favourite_status(self, entry_id):
        """Fetches the favourite status of an entry by ID."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT favourite FROM vault WHERE id = ?", (entry_id,))
        result = cursor.fetchone()
        if result:
            return bool(result[0])
        return False
        
    def fetch_favourites(self, encryption_key):
        """
        Fetches all entries marked as favourites from the vault.

        This method retrieves all entries from the database where the 'favourite' column is set to 1 (true),
        indicating they are marked as favourites. The retrieved entries are then decrypted using the provided
        encryption key before being returned.

        Args:
            encryption_key (bytes): The encryption key used for decrypting the entries.

        Returns:
            list of tuple: A list of decrypted entries that are marked as favourites.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM vault WHERE favourite = 1;")
        encrypted_entries = cursor.fetchall()
        return self.decrypt_entries(encrypted_entries, encryption_key)
    
    def wipe_database(self):
        """Delete all entries from the vault."""
        cursor = self.connection.cursor()
        # This deletes all entries in the vault
        cursor.execute("DELETE FROM vault;")
        self.connection.commit()
        
    def decrypt_entries(self, encrypted_entries, encryption_key):
        """Decrypt a list of encrypted vault entries."""
        decrypted_entries = []
        for entry in encrypted_entries:
            id, encrypted_website_name, encrypted_website_url, encrypted_username, encrypted_password, encrypted_notes, favourite, created_at, updated_at = entry
            
            website_name = Encryption.decrypt_data(encrypted_website_name, encryption_key) if encrypted_website_name else None
            website_url = Encryption.decrypt_data(encrypted_website_url, encryption_key) if encrypted_website_url else None
            username = Encryption.decrypt_data(encrypted_username, encryption_key)
            password = Encryption.decrypt_data(encrypted_password, encryption_key)
            notes = Encryption.decrypt_data(encrypted_notes, encryption_key) if encrypted_notes else None
            
            decrypted_entries.append((id, website_name, website_url, username, password, notes, bool(favourite), created_at, updated_at))
        
        return decrypted_entries