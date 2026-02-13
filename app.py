#question processing code
import random

def answer(question: str) -> str:
    words = str.split(' ')
    word = random.choice(words)
    return "something something " + word