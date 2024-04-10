import pytest
from src.core.Database import Database
from src.core.Encryption import Encryption
import random
import string
from Crypto.Random import get_random_bytes

# Helper function to generate a unique encryption key for testing
def generate_test_key():
    return Encryption.derive_key("testpassword".encode(), get_random_bytes(16))

def random_string(length=10):
    """Generates a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

@pytest.fixture(scope="module")
def db():
    # Setup a test database instance
    test_db = Database()
    yield test_db
    # Teardown test database
    test_db.wipe_database()
    test_db.close_connection()

@pytest.fixture(scope="module")
def encryption_key():
    return generate_test_key()

class TestDatabaseCRUD:
    def test_add_new_entry(self, db, encryption_key):
        website_name = random_string(12)
        website_url = f"https://{random_string(8)}.com"
        username = random_string(8)
        password = random_string(12)
        notes = random_string(20)
        
        db.add_password_entry(website_name, website_url, username, password, notes, encryption_key)
        entries = db.fetch_all_entries(encryption_key)
        
        assert entries, "No entries found after adding a new entry."
        assert any(entry[1] == website_name and entry[3] == username for entry in entries), "Added entry does not match the expected values."

    def test_update_entry(self, db, encryption_key):
        # Initial entry creation with dynamic data
        initial_website_name = random_string(12)
        initial_website_url = f"https://{random_string(8)}.com"
        initial_username = random_string(8)
        initial_password = random_string(12)
        initial_notes = random_string(20)

        db.add_password_entry(initial_website_name, initial_website_url, initial_username, initial_password, initial_notes, encryption_key)
        entries = db.fetch_all_entries(encryption_key)
        entry_id = entries[0][0]  # Assuming the first entry is the one we just added

        # Updating with new dynamic data
        new_website_name = random_string(12)
        new_website_url = f"https://{random_string(8)}.com"
        new_username = random_string(8)
        new_password = random_string(12)
        new_notes = random_string(20)

        db.update_password_entry(entry_id, new_website_name, new_website_url, new_username, new_password, new_notes, encryption_key)
        updated_entries = db.fetch_all_entries(encryption_key)
        updated_entry = next((entry for entry in updated_entries if entry[0] == entry_id), None)

        assert updated_entry, "The entry to update was not found."
        assert updated_entry[1] == new_website_name and updated_entry[3] == new_username, "Data integrity test failed; the entry was not updated correctly."

    def test_delete_entry(self, db, encryption_key):
        entry_id = 1  # Assuming an entry exists with ID 1
        db.delete_password_entry(entry_id)
        entries = db.fetch_all_entries(encryption_key)
        
        for entry in entries:
            assert entry[0] != entry_id, "Deleted entry still exists in the database."

    def test_list_all_entries(self, db, encryption_key):
        # Setup step: Add an entry to ensure there's at least one entry to list
        db.add_password_entry("List Test Site", "https://listtest.com", "listuser", "listpassword", "list note", encryption_key)
        entries = db.fetch_all_entries(encryption_key)
        assert entries, "Failed to list entries: No entries found."


    def test_search_functionality(self, db, encryption_key):
        search_term = random_string(5)
        db.add_password_entry(f"{search_term} Site", f"https://{search_term}.com", f"{search_term}user", "password", "Example note", encryption_key)

        entries = db.fetch_all_entries(encryption_key)
        assert any(search_term.lower() in entry[1].lower() for entry in entries), "Search functionality did not return correct entries."


    def test_fetch_favourites(self, db, encryption_key):
        db.add_password_entry("Favourite Test Site", "https://favtest.com", "favuser", "favpassword", "Fav note", encryption_key)
        entries = db.fetch_all_entries(encryption_key)
        entry_id = entries[-1][0]  # Get the last added entry's ID
        db.toggle_favourite_status(entry_id, True)  # Mark as favourite

        favourites = db.fetch_favourites(encryption_key)
        assert any(entry[0] == entry_id for entry in favourites), "Failed to fetch favourite entries."

    def test_toggle_favourite_status(self, db, encryption_key):
        # Setup step: Add an entry and then toggle its favourite status
        db.add_password_entry("Favourite Test Site", "https://favtest.com", "favuser", "favpassword", "fav note", encryption_key)
        entries = db.fetch_all_entries(encryption_key)
        entry_id = entries[-1][0]  # Get the last added entry's ID
        initial_status = db.fetch_favourite_status(entry_id)
        db.toggle_favourite_status(entry_id, not initial_status)
        updated_status = db.fetch_favourite_status(entry_id)
        assert updated_status != initial_status, "Failed to toggle favourite status."


    def test_data_integrity_on_update(self, db, encryption_key):
        # Test setup: Add an entry to update
        website_name = "Data Integrity Test"
        website_url = "https://dataintegritytest.com"
        username = "integrityuser"
        password = "integritypassword"
        notes = "Data integrity test note."
        db.add_password_entry(website_name, website_url, username, password, notes, encryption_key)
        
        # Fetch all entries to get the ID of the newly added entry
        entries = db.fetch_all_entries(encryption_key)
        entry_id = entries[-1][0]  # Assuming the newly added entry is the last one

        # Execute the update
        db.update_password_entry(entry_id, "Updated Example", "https://test.com", "user_updated", "pass_updated", "Notes updated", encryption_key)
        updated_entries = db.fetch_all_entries(encryption_key)
        
        # Test verification: Check that the updated entry has the expected values
        updated_entry = next((entry for entry in updated_entries if entry[0] == entry_id), None)
        assert updated_entry, "The entry to update was not found."
        assert updated_entry[1] == "Updated Example" and updated_entry[3] == "user_updated", "Data integrity test failed; the entry was not updated correctly."


    def test_database_wipe(self, db, encryption_key):
        db.wipe_database()
        entries = db.fetch_all_entries(encryption_key)
        assert not entries, "Database wipe test failed; entries still exist after wipe."

    def test_error_handling_and_validation(self, db, encryption_key):
        with pytest.raises(Exception):
            db.add_password_entry(None, None, None, None, None, encryption_key)
                
    def test_error_handling_for_invalid_entry_addition(self, db, encryption_key):
        """Test handling of adding entries with invalid data."""
        with pytest.raises(ValueError):
            db.add_password_entry(None, "https://example.com", "user", "password", "Notes", encryption_key)  # 'password' is now a valid non-None value
        with pytest.raises(ValueError):
            db.add_password_entry("Website", "https://example.com", None, "password", "Notes", encryption_key)  # 'username' is None, expecting ValueError
        with pytest.raises(ValueError):
            db.add_password_entry("Website", "https://example.com", "user", None, "Notes", encryption_key)  # 'password' is None, correctly triggering ValueError

            