import random

adjectives = [
    "Creative", "Dynamic", "Bold", "Innovative", "Bright", "Smart", "Elite", "Prime", "Urban", "Global"
]

nouns = [
    "Solutions", "Studio", "Agency", "Group", "Works", "Lab", "Media", "Partners", "Collective", "Network"
]

extras = [
    "Edge", "Vision", "Pulse", "Hive", "Bridge", "Point", "Sphere", "Core", "Link", "Zone"
]

def generate_agency_name():
    word_count = random.choice([2, 3])
    if word_count == 2:
        name = f"{random.choice(adjectives)} {random.choice(nouns)}"
    else:
        name = f"{random.choice(adjectives)} {random.choice(extras)} {random.choice(nouns)}"
    return name

if __name__ == "__main__":
    for _ in range(10):
        print(generate_agency_name())