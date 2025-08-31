"""
Random User Data Generator
Generates unique user data for testing user management functionality
"""

import random
import time


def generate_user_name():
    """
    Generate a realistic user name for testing
    
    Returns:
        str: Full user name (first + last)
    """
    first_names = [
        "John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert", "Emma",
        "William", "Jennifer", "James", "Jessica", "Christopher", "Ashley", "Daniel", "Amanda",
        "Matthew", "Stephanie", "Anthony", "Melissa", "Mark", "Nicole", "Steven", "Elizabeth",
        "Paul", "Helen", "Andrew", "Sharon", "Kenneth", "Donna", "Brian", "Carol"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", 
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
        "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
        "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young"
    ]
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    return f"{first_name} {last_name}"


def generate_user_email(user_name: str = None):
    """
    Generate a unique email address for testing
    
    Args:
        user_name: Optional user name to base email on
        
    Returns:
        str: Unique email address
    """
    domains = [
        "test.com", 
        "example.org", 
        "demo.net",
        "testmail.com",
        "sample.org",
        "mockmail.net",
        "autotest.com",
        "qatest.org"
    ]
    
    # Generate timestamp for uniqueness
    timestamp = str(int(time.time()))[-6:]
    
    if user_name:
        # Base email on user name
        name_parts = user_name.lower().replace(" ", ".").replace("-", ".")
        email_prefix = f"{name_parts}.{timestamp}"
    else:
        # Generate random email prefix
        prefixes = [
            "testuser", "qauser", "autouser", "demouser", "sampleuser",
            "john.doe", "jane.smith", "test.account", "demo.person", "qa.tester"
        ]
        email_prefix = f"{random.choice(prefixes)}.{timestamp}"
    
    domain = random.choice(domains)
    
    return f"{email_prefix}@{domain}"


def generate_test_user_data():
    """
    Generate complete user data set with name and email
    
    Returns:
        dict: Dictionary containing user_name and user_email
    """
    user_name = generate_user_name()
    user_email = generate_user_email(user_name)
    
    return {
        'user_name': user_name,
        'user_email': user_email
    }


def generate_multiple_test_users(count: int = 5):
    """
    Generate multiple unique test users
    
    Args:
        count: Number of users to generate
        
    Returns:
        list: List of user data dictionaries
    """
    users = []
    for i in range(count):
        users.append(generate_test_user_data())
        # Small delay to ensure unique timestamps
        time.sleep(0.1)
    
    return users


def generate_user_with_role_data(role_name: str):
    """
    Generate user data with specific role assignment
    
    Args:
        role_name: Name of the role to assign
        
    Returns:
        dict: Complete user invitation data
    """
    user_data = generate_test_user_data()
    user_data['role_name'] = role_name
    
    return user_data


def generate_invalid_email_test_cases():
    """
    Generate invalid email addresses for validation testing
    
    Returns:
        list: List of invalid email addresses with descriptions
    """
    invalid_emails = [
        {
            'email': 'invalid-email',
            'description': 'Missing @ symbol and domain'
        },
        {
            'email': '@example.com',
            'description': 'Missing username part'
        },
        {
            'email': 'user@',
            'description': 'Missing domain part'
        },
        {
            'email': 'user@.com',
            'description': 'Invalid domain format'
        },
        {
            'email': 'user..name@example.com',
            'description': 'Double dots in username'
        },
        {
            'email': 'user@domain',
            'description': 'Missing top-level domain'
        },
        {
            'email': 'user name@example.com',
            'description': 'Space in username'
        },
        {
            'email': 'user@domain .com',
            'description': 'Space in domain'
        },
        {
            'email': '',
            'description': 'Empty email'
        },
        {
            'email': '   ',
            'description': 'Only whitespace'
        }
    ]
    
    return invalid_emails


def generate_edge_case_user_names():
    """
    Generate edge case user names for validation testing
    
    Returns:
        list: List of edge case user names with descriptions
    """
    edge_case_names = [
        {
            'name': '',
            'description': 'Empty name'
        },
        {
            'name': '   ',
            'description': 'Only whitespace'
        },
        {
            'name': 'A',
            'description': 'Single character'
        },
        {
            'name': 'A' * 100,
            'description': 'Very long name (100 characters)'
        },
        {
            'name': 'User Name With Many Words In Between',
            'description': 'Name with many spaces'
        },
        {
            'name': 'User123',
            'description': 'Name with numbers'
        },
        {
            'name': 'User-Name',
            'description': 'Name with hyphen'
        },
        {
            'name': 'User.Name',
            'description': 'Name with period'
        },
        {
            'name': "User'Name",
            'description': 'Name with apostrophe'
        },
        {
            'name': 'User@Name',
            'description': 'Name with special character'
        }
    ]
    
    return edge_case_names


def generate_host_email_variants():
    """
    Generate variants of host email for protection testing
    
    Returns:
        list: List of host email variants
    """
    base_host_email = "mi003b@onemail.host"
    
    variants = [
        base_host_email,  # Exact match
        base_host_email.upper(),  # Uppercase
        base_host_email.lower(),  # Lowercase  
        "MI003B@ONEMAIL.HOST",  # All uppercase
        "Mi003b@Onemail.Host",  # Mixed case
        " mi003b@onemail.host ",  # With spaces
        "mi003b@onemail.host\n",  # With newline
        "mi003b@onemail.host\t"   # With tab
    ]
    
    return variants


def generate_bulk_user_test_data(count: int = 20):
    """
    Generate bulk user data for performance testing
    
    Args:
        count: Number of users to generate
        
    Returns:
        list: List of user data for bulk operations
    """
    bulk_users = []
    
    for i in range(count):
        user_data = generate_test_user_data()
        user_data['batch_id'] = f"BULK_{int(time.time())}_{i:03d}"
        bulk_users.append(user_data)
        
        # Very small delay to ensure uniqueness
        time.sleep(0.01)
    
    return bulk_users


def generate_user_hierarchy_data():
    """
    Generate user data for role hierarchy testing
    
    Returns:
        dict: Dictionary with admin, manager, and regular user data
    """
    timestamp = str(int(time.time()))[-4:]
    
    return {
        'admin_user': {
            'user_name': f"Test Admin User {timestamp}",
            'user_email': f"admin.test.{timestamp}@example.com",
            'role_name': "Admin Role"
        },
        'manager_user': {
            'user_name': f"Test Manager User {timestamp}",
            'user_email': f"manager.test.{timestamp}@example.com", 
            'role_name': "Manager Role"
        },
        'regular_user': {
            'user_name': f"Test Regular User {timestamp}",
            'user_email': f"user.test.{timestamp}@example.com",
            'role_name': "User Role"
        }
    }
