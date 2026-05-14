import json
import os

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_DIR = os.path.join(BASE_DIR, "memory")
MEMORY_FILE = os.path.join(MEMORY_DIR, "user_memory.json")


def save_memory(username, preferences):
    # Ensure directory exists
    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)

    try:

        with open(MEMORY_FILE, "r") as file:
            data = json.load(file)

    except:
        data = {}

    data[username] = preferences

    with open(MEMORY_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_memory(username):

    try:

        with open(MEMORY_FILE, "r") as file:
            data = json.load(file)

        return data.get(username, {})

    except:
        return {}