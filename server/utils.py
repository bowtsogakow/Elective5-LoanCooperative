import datetime
import string 
import random

def generate_random_string(length=8):
    # Generate a random string of the specified length
    characters = string.ascii_letters + string.digits  # Choose the characters you want
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def format_number_with_commas(num):
    # Format the number with commas and ensure two decimal places
    formatted_number = "{:,.2f}".format(num)
    return formatted_number

def parse_date(date_string):
    # List of possible date formats
    date_formats = [
        "%Y-%m-%d",  # YYYY-MM-DD
        "%m-%d-%Y",  # MM-DD-YYYY
        "%d-%m-%Y",  # DD-MM-YYYY
    ]
    
    # Try parsing the string with each format
    for date_format in date_formats:
        try:
            return datetime.datetime.strptime(date_string, date_format).date()
        except ValueError:
            continue
    
    # If no format works, raise an error
    raise ValueError(f"Invalid date format for string: {date_string}")