import random
import string

def random_string():
    return "".join(random.choice(string.ascii_letters) for i in range(50))
