from src.core.Password_Generator import PasswordGenerator  # Adjust the import according to your project structure
import random
import pytest

class TestPasswordGenerator:
    def test_varying_length(self):
        """Test that the generated password matches the randomly chosen length."""
        for _ in range(10000):
            random_length = random.randint(12, 100)  # Generate a random length between 12 and 100
            password = PasswordGenerator.generate_password(random_length)
            assert len(password) == random_length, f"Password of length {random_length} does not meet the length requirement"

    def test_contains_digit(self):
        """Test that the generated password contains at least one digit."""
        for _ in range(10000):
            password = PasswordGenerator.generate_password()
            assert any(char.isdigit() for char in password), "Password does not contain a digit"

    def test_contains_uppercase(self):
        """Test that the generated password contains at least one uppercase letter."""
        for _ in range(10000):
            password = PasswordGenerator.generate_password()
            if not any(char.isupper() for char in password):
                print(f"Failed uppercase test with password: {password}")
            assert any(char.isupper() for char in password), "Password does not contain an uppercase letter"

    def test_contains_lowercase(self):
        """Test that the generated password contains at least one lowercase letter."""
        for _ in range(10000):
            password = PasswordGenerator.generate_password()
            assert any(char.islower() for char in password), "Password does not contain a lowercase letter"

    def test_contains_special_character(self):
        """Test that the generated password contains at least one special character."""
        for _ in range(10000):
            password = PasswordGenerator.generate_password()
            assert any(char in "!@#$%^&*()?:|" for char in password), "Password does not contain a special character"

    def test_randomness(self):
        """Test that multiple invocations produce different passwords."""
        passwords = {PasswordGenerator.generate_password() for _ in range(10000)}
        assert len(passwords) == 10000, "Generated passwords are not unique"

