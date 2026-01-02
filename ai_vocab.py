import random

WORDS = [
    ("Articulate", "Able to express ideas clearly", "She articulated her thoughts confidently."),
    ("Resilient", "Able to recover quickly", "He remained resilient after failure."),
    ("Meticulous", "Very careful and precise", "She is meticulous about her work."),
    ("Empathy", "Understanding others' feelings", "Empathy strengthens relationships."),
]

def get_vocab():
    return random.choice(WORDS)
