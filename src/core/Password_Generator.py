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
        
        if num_digits > 0:
            password_parts += random.choices(string.digits, k=num_digits)
            characters += string.digits
        
        if num_specials > 0:
            specials = "!@#$%^&*(),.?\":{}|<>"
            password_parts += random.choices(specials, k=num_specials)
            characters += specials
        
        remaining_length = length - len(password_parts)
        password_parts += random.choices(characters, k=remaining_length)
        random.shuffle(password_parts)
        
        return ''.join(password_parts)