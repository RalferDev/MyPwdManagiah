# password_generator.py
import string
import secrets


def generate_password(length: int = 16) -> str:
    """Generates a secure, random password."""
    if length < 8:
        raise ValueError("Password length should be at least 8 characters.")

    # Define the character sets
    alphabet = string.ascii_letters
    digits = string.digits
    special_chars = "!@#$%^&*()-_=+"

    # Ensure the password contains at least one of each character type
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(digits),
        secrets.choice(special_chars)
    ]

    # Fill the rest of the password length with a mix of all characters
    all_chars = alphabet + digits + special_chars
    remaining_length = length - len(password)
    password.extend(secrets.choice(all_chars) for _ in range(remaining_length))

    # Shuffle the list to ensure randomness and convert back to a string
    secrets.SystemRandom().shuffle(password)

    return "".join(password)