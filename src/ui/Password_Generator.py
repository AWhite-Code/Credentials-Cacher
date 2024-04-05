import random
import string

class PasswordGenerator:
    @staticmethod
    def generate_password(length=12, include_uppercase=True, num_digits=2, num_specials=2):
        # Initialize character pools
        characters = string.ascii_lowercase
        if include_uppercase:
            characters += string.ascii_uppercase
        
        # Initialize parts of the password
        password_parts = []
        
        # Add the required number of digits
        if num_digits > 0:
            password_parts += random.choices(string.digits, k=num_digits)
            characters += string.digits
        
        # Add the required number of special characters
        if num_specials > 0:
            specials = "!@#$%^&*(),.?\":{}|<>"
            password_parts += random.choices(specials, k=num_specials)
            characters += specials
        
        # Calculate the remaining length to be filled with characters from the pool
        remaining_length = length - len(password_parts)
        
        # Generate the rest of the password
        password_parts += random.choices(characters, k=remaining_length)
        
        # Shuffle to avoid predictable patterns
        random.shuffle(password_parts)
        
        # Return the final password
        return ''.join(password_parts)