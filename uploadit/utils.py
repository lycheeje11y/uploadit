
import random
import string
import json


def random_string():
    return "".join(random.choice(string.ascii_letters) for i in range(50))

def get_config():
    with open("files.json") as file_json:
        return json.load(file_json)
