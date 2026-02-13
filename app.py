#question processing code
import random

def answer(question: str) -> str:
    words = question.split(' ')
    word = random.choice(words)
    return "something something " + word