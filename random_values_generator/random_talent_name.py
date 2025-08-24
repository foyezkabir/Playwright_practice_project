"""
Random Talent Name Generator
Generates unique talent names for test isolation
"""

import random
from datetime import datetime

class RandomTalentName:
    def __init__(self):
        self.first_names = [
            "John", "Jane", "Michael", "Sarah", "David", "Emily", "James", "Lisa", 
            "Robert", "Mary", "William", "Patricia", "Richard", "Jennifer", "Joseph", 
            "Linda", "Thomas", "Elizabeth", "Christopher", "Barbara", "Charles", "Susan",
            "Daniel", "Jessica", "Matthew", "Karen", "Anthony", "Nancy", "Mark", "Betty"
        ]
        
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
            "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
            "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"
        ]
        
        self.job_titles = [
            "Software Engineer", "Data Analyst", "Project Manager", "Marketing Specialist",
            "Sales Representative", "Human Resources Manager", "Financial Analyst", 
            "Business Analyst", "Product Manager", "Operations Manager", "Customer Service Representative",
            "Administrative Assistant", "Accountant", "Research Assistant", "Quality Assurance Analyst",
            "Content Writer", "Graphic Designer", "Web Developer", "Database Administrator",
            "Network Engineer", "System Administrator", "Consultant", "Training Specialist",
            "Account Manager", "Business Development Manager", "Technical Writer", "Associate",
            "Analyst", "Coordinator", "Specialist"
        ]
    
    def generate_talent_name(self):
        """Generate a unique talent name with timestamp."""
        timestamp = datetime.now().strftime("%H%M%S")
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        return f"{first_name} {last_name} {timestamp}"
    
    def generate_first_name(self):
        """Generate random first name with timestamp."""
        timestamp = datetime.now().strftime("%H%M%S")
        first_name = random.choice(self.first_names)
        return f"{first_name}{timestamp}"
    
    def generate_last_name(self):
        """Generate random last name with timestamp."""
        timestamp = datetime.now().strftime("%H%M%S") 
        last_name = random.choice(self.last_names)
        return f"{last_name}{timestamp}"
    
    def generate_job_title(self):
        """Generate random job title."""
        return random.choice(self.job_titles)
    
    def generate_cv_name(self, talent_name: str = None):
        """Generate CV name based on talent name or random."""
        if talent_name:
            return f"{talent_name} CV"
        else:
            timestamp = datetime.now().strftime("%H%M%S")
            return f"CV_{timestamp}"
    
    def generate_email(self, first_name: str = None, last_name: str = None):
        """Generate email address for talent."""
        if not first_name:
            first_name = random.choice(self.first_names).lower()
        if not last_name:
            last_name = random.choice(self.last_names).lower()
        
        timestamp = datetime.now().strftime("%H%M%S")
        domains = ["gmail.com", "outlook.com", "yahoo.com", "company.com", "test.com"]
        domain = random.choice(domains)
        
        return f"{first_name}.{last_name}{timestamp}@{domain}"
    
    def generate_phone_number(self):
        """Generate random phone number."""
        # Generate 10-digit phone number
        area_code = random.randint(200, 999)
        exchange = random.randint(200, 999)
        number = random.randint(1000, 9999)
        return f"{area_code}{exchange:03d}{number}"
    
    def generate_location(self):
        """Generate random location."""
        locations = [
            "United States", "Canada", "United Kingdom", "Australia", "Germany", 
            "France", "Japan", "South Korea", "Singapore", "Netherlands",
            "Sweden", "Norway", "Denmark", "Switzerland", "New Zealand",
            "Ireland", "Belgium", "Austria", "Finland", "Italy"
        ]
        return random.choice(locations)
    
    def generate_date_of_birth(self, min_age: int = 18, max_age: int = 65):
        """Generate random date of birth within age range."""
        current_year = datetime.now().year
        birth_year = random.randint(current_year - max_age, current_year - min_age)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # Safe day range for all months
        
        return f"{birth_month:02d}/{birth_day:02d}/{birth_year}"
    
    def generate_language_level(self):
        """Generate random language proficiency level."""
        levels = ["Basic", "Conversational", "Fluent", "Native"]
        return random.choice(levels)
    
    def generate_gender(self):
        """Generate random gender."""
        genders = ["Male", "Female", "Prefer not to say"]
        return random.choice(genders)
    
    def generate_talent_status(self):
        """Generate random talent status."""
        statuses = ["Active", "Inactive", "Proactive"]
        return random.choice(statuses)

# Convenience function for quick access
def generate_talent_name():
    """Quick function to generate talent name."""
    generator = RandomTalentName()
    return generator.generate_talent_name()

def generate_random_talent_data():
    """Generate complete random talent data for testing."""
    generator = RandomTalentName()
    first_name = generator.generate_first_name()
    last_name = generator.generate_last_name()
    
    return {
        'first_name': first_name,
        'last_name': last_name,
        'full_name': f"{first_name} {last_name}",
        'gender': generator.generate_gender(),
        'job_title': generator.generate_job_title(),
        'date_of_birth': generator.generate_date_of_birth(),
        'japanese_level': generator.generate_language_level(),
        'english_level': generator.generate_language_level(),
        'location': generator.generate_location(),
        'cv_name': generator.generate_cv_name(f"{first_name} {last_name}"),
        'cv_language': 'English',
        'email': generator.generate_email(first_name, last_name),
        'phone': generator.generate_phone_number(),
        'talent_status': generator.generate_talent_status()
    }
