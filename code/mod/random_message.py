import random
import uuid

def random_message() -> str:
    word = ["Apple", "Banana", "Coconut", "Durian", "Eggplant", "Fig", "Grape"]
    return " ".join(random.sample(word, 3))

def structured_random_message() -> str:
    return str(uuid.uuid4())