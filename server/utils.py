import string 
import random

def generate_random_string(length=9):
    # Generate a random string of the specified length
    characters = string.ascii_letters + string.digits  # Choose the characters you want
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string