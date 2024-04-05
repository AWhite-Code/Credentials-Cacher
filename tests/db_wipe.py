from Database import Database

def wipe_database():
    print("I have been called!")
    db = Database()  # Initializes and connects to the database
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM vault")  # Clears the 'vault' table
    db.connection.commit()
    print("Database wiped clean.")
    db.close_connection()  # Close the database connection cleanly

if __name__ == "__main__":
    wipe_database()