import random
import string

class PasswordGenerator:
    @staticmethod
    def generate_password(length=12):
        if length < 12:
            length = 12  # Ensuring the minimum length is 12

        # Define the characters to be used in the password
        characters = string.ascii_letters + string.digits + "!@#$%^&*(),.?\":{}|<>"
        
        # Ensure the password meets all criteria by including at least one of each required character type
        password = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice("!@#$%^&*(),.?\":{}|<>")
        ]
        
        # Fill the rest of the password length with random choices from the characters pool
        password += random.choices(characters, k=length - 4)
        
        # Shuffle the generated password list to avoid any predictable patterns
        random.shuffle(password)
        
        # Join the list into a string to form the final password
        return ''.join(password)

# Example usage
password_generator = PasswordGenerator()
generated_password = password_generator.generate_password(12)
print("Generated Password:", generated_password)