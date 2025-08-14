"""
Random Company Name Generator
Generates unique company names for testing to avoid conflicts
"""

import random
import string
from datetime import datetime

def generate_company_name():
    """
    Generate a unique company name with timestamp to avoid conflicts
    
    Returns:
        str: Unique company name
    """
    # Company name prefixes
    prefixes = [
        "Innovatech", "Techno", "Global", "Smart", "Digital", "Future", 
        "Advanced", "Modern", "Dynamic", "Strategic", "Premier", "Elite",
        "Progressive", "Innovative", "Creative", "Professional", "Expert",
        "Superior", "Excellence", "Quality", "Reliable", "Trusted"
    ]
    
    # Company name suffixes  
    suffixes = [
        "Solutions", "Systems", "Technologies", "Enterprises", "Corporation",
        "Group", "Associates", "Partners", "Consulting", "Services",
        "Industries", "Holdings", "Ventures", "Dynamics", "Networks",
        "Labs", "Studios", "Works", "Hub", "Center"
    ]
    
    # Generate timestamp for uniqueness
    timestamp = datetime.now().strftime("%m%d%H%M")
    
    # Random selection
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    
    # Generate company name
    company_name = f"{prefix} {suffix} {timestamp}"
    
    return company_name

def generate_simple_company_name():
    """
    Generate a simpler company name without timestamp
    
    Returns:
        str: Simple company name
    """
    prefixes = ["Acme", "Beta", "Gamma", "Delta", "Sigma", "Alpha", "Omega"]
    suffixes = ["Corp", "Inc", "Ltd", "LLC", "Co"]
    
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    random_num = random.randint(100, 999)
    
    return f"{prefix} {suffix} {random_num}"

def generate_test_company_name():
    """
    Generate a company name specifically for testing with 'Test' prefix
    
    Returns:
        str: Test company name
    """
    adjectives = ["Smart", "Quick", "Fast", "Bright", "Sharp", "Swift", "Bold"]
    nouns = ["Tech", "Labs", "Works", "Systems", "Solutions", "Group", "Corp"]
    
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    timestamp = datetime.now().strftime("%H%M")
    
    return f"Test {adjective} {noun} {timestamp}"

def generate_company_name_with_industry(industry: str):
    """
    Generate a company name relevant to the industry
    
    Args:
        industry: Industry name (Finance, Healthcare, Technology, Education)
        
    Returns:
        str: Industry-relevant company name
    """
    timestamp = datetime.now().strftime("%m%d%H%M")
    
    industry_specific = {
        "Finance": {
            "prefixes": ["Capital", "Investment", "Financial", "Banking", "Credit", "Asset"],
            "suffixes": ["Solutions", "Partners", "Group", "Associates", "Holdings", "Capital"]
        },
        "Healthcare": {
            "prefixes": ["Health", "Medical", "Care", "Wellness", "Life", "Bio"],
            "suffixes": ["Systems", "Solutions", "Group", "Partners", "Care", "Medical"]
        },
        "Technology": {
            "prefixes": ["Tech", "Digital", "Cyber", "Data", "Cloud", "AI"],
            "suffixes": ["Solutions", "Systems", "Labs", "Works", "Hub", "Technologies"]
        },
        "Education": {
            "prefixes": ["Learning", "Education", "Academic", "Scholar", "Knowledge", "Study"],
            "suffixes": ["Solutions", "Systems", "Group", "Partners", "Institute", "Academy"]
        }
    }
    
    if industry in industry_specific:
        config = industry_specific[industry]
        prefix = random.choice(config["prefixes"])
        suffix = random.choice(config["suffixes"])
        return f"{prefix} {suffix} {timestamp}"
    else:
        # Fallback to general name
        return generate_company_name()

# Test data for specific test scenarios
TEST_COMPANY_NAMES = {
    "basic": "Innovatech Solutions",
    "duplicate_test": "Duplicate Test Company",
    "min_length": "AB",  # For minimum length validation
    "max_length": "A" * 85,  # For maximum length validation  
    "special_chars_start": "#Invalid Company",  # For special character validation
    "special_chars_end": "Invalid Company#",  # For special character validation
    "valid_with_numbers": "Company 123 Solutions",
    "valid_with_spaces": "Multi Word Company Name"
}
