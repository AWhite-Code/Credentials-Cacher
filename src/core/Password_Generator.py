import random
import string

class PasswordGenerator:
    """
    A utility class for generating random passwords with specific criteria.
    """
    
    @staticmethod
    def generate_password(length=12, include_uppercase=True, num_digits=2, num_specials=2):
        """
        Generates a random password based on specified criteria.

        Args:
            length (int): The total length of the password. Defaults to 12 characters.
            include_uppercase (bool): Whether to include uppercase letters. Defaults to True.
            num_digits (int): The number of numeric digits to include in the password. Defaults to 2.
            num_specials (int): The number of special characters to include in the password. Defaults to 2.

        Returns:
            str: A string representing the randomly generated password.
        """
        characters = string.ascii_lowercase
        password_parts = []

        # Ensure at least one uppercase letter is added if required
        if include_uppercase:
            password_parts.append(random.choice(string.ascii_uppercase))

        # Ensure at least one lowercase letter is added
        password_parts.append(random.choice(string.ascii_lowercase))

        # Select unique digits if required
        if num_digits > 0:
            digits = random.sample(string.digits, k=num_digits)
            password_parts.extend(digits)

        # Select unique special characters if required
        specials = "!@#$%^&*()?:|"  # Removed characters that might break SQL
        if num_specials > 0:
            specials_selected = random.sample(specials, k=num_specials)
            password_parts.extend(specials_selected)

        # Ensure the remainder of the password length with a mix of character types
        remaining_length = length - len(password_parts)
        remaining_characters = [char for char in characters if char not in string.digits and char not in specials]
        password_parts.extend(random.choices(remaining_characters, k=remaining_length))

        # Shuffle the selected characters to eliminate any predictable patterns
        random.shuffle(password_parts)
        
        return ''.join(password_parts)