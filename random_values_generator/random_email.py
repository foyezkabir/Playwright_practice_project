# random_values_generator.py
import random
import string

class RandomEmail:
    def __init__(self):
        self.domains = ["@tempml.com", "@maiinator.com", "@guerrillaml.com", "@10minuteml.com"]
        self.letters = string.ascii_lowercase
        self.digits = string.digits

    def generate_email(self):
        username = ''.join(random.choice(self.letters + self.digits) for _ in range(10))
        domain = random.choice(self.domains)
        return username + domain

random_email = RandomEmail()