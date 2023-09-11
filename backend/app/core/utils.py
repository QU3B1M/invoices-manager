import random
import string


def get_random_string(length: int = 16) -> str:
    """
    Function to generate a random string using the ascii letters and digits
    """
    letters_and_digits = string.ascii_letters + string.digits
    return "".join(random.choice(letters_and_digits) for i in range(length))
