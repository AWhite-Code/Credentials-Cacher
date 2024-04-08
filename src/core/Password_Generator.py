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

        The function constructs a password that meets the specified requirements by
        assembling a pool of characters, digits, and special characters from which it
        randomly selects. It ensures that the generated password contains the required
        number of digits and special characters, and then fills the remainder of the
        password length with a mix of the specified character types. Finally, it shuffles
        the selected characters to eliminate any predictable patterns.
        """
        characters = string.ascii_lowercase
        if include_uppercase:
            characters += string.ascii_uppercase
        
        password_parts = []

        # Select unique digits if required
        if num_digits > 0:
            digits = random.sample(string.digits, k=min(num_digits, len(string.digits)))
            password_parts.extend(digits)

        # Select unique special characters if required
        if num_specials > 0:
            specials = "!@#$%^&*()?\:|<>"
            specials_selected = random.sample(specials, k=min(num_specials, len(specials)))
            password_parts.extend(specials_selected)

        # Ensure the remainder of the password doesn't inadvertently increase the count of digits/specials
        remaining_characters = []
        for char in characters:
            if char not in string.digits and char not in specials:      # Create a list of only upper and lower case characters
                remaining_characters.append(char)
                

        remaining_length = length - len(password_parts)
        remaining_parts = random.choices(remaining_characters, k=remaining_length)

        password_parts.extend(remaining_parts)
        random.shuffle(password_parts)
        
        return ''.join(password_parts)