from ..src.core.Password_Generator import PasswordGenerator  # Adjust the import according to your project structure
import pytest

class TestPasswordGenerator:
    def test_length(self):
        """Test that the generated password has at least 12 characters."""
        password = PasswordGenerator.generate_password(12)
        assert len(password) >= 12, "Password does not meet the minimum length requirement"

    def test_contains_digit(self):
        """Test that the generated password contains at least one digit."""
        password = PasswordGenerator.generate_password()
        assert any(char.isdigit() for char in password), "Password does not contain a digit"

    def test_contains_uppercase(self):
        """Test that the generated password contains at least one uppercase letter."""
        password = PasswordGenerator.generate_password()
        assert any(char.isupper() for char in password), "Password does not contain an uppercase letter"

    def test_contains_lowercase(self):
        """Test that the generated password contains at least one lowercase letter."""
        password = PasswordGenerator.generate_password()
        assert any(char.islower() for char in password), "Password does not contain a lowercase letter"

    def test_contains_special_character(self):
        """Test that the generated password contains at least one special character."""
        password = PasswordGenerator.generate_password()
        special_chars = "!@#$%^&*(),.?\":{}|<>"
        assert any(char in special_chars for char in password), "Password does not contain a special character"

    def test_randomness(self):
        """Test that multiple invocations produce different passwords."""
        passwords = {PasswordGenerator.generate_password() for _ in range(100)}
        assert len(passwords) > 1, "Generated passwords are not unique"
