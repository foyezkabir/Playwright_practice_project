"""
Random Role Name Generator
Generates unique role names for testing user management functionality
"""

import random
import time


def generate_role_name():
    """
    Generate a unique role name for testing
    
    Returns:
        str: Unique role name
    """
    role_prefixes = [
        "Manager",
        "Administrator", 
        "Editor",
        "Viewer",
        "Supervisor",
        "Coordinator",
        "Assistant",
        "Lead",
        "Senior",
        "Junior"
    ]
    
    role_suffixes = [
        "Role",
        "Access",
        "Position",
        "Level",
        "Tier"
    ]
    
    departments = [
        "HR",
        "IT", 
        "Sales",
        "Marketing",
        "Finance",
        "Operations",
        "Development",
        "Support",
        "QA",
        "Design"
    ]
    
    # Generate timestamp for uniqueness (but we'll use it differently)
    timestamp = str(int(time.time()))[-4:]
    
    # Create role name with various patterns (without timestamp numbers)
    pattern = random.choice([1, 2, 3, 4])
    
    if pattern == 1:
        # Pattern: Department + Prefix + Suffix  
        role_name = f"{random.choice(departments)} {random.choice(role_prefixes)} {random.choice(role_suffixes)}"
    elif pattern == 2:
        # Pattern: Prefix + Department + Suffix
        role_name = f"{random.choice(role_prefixes)} {random.choice(departments)} {random.choice(role_suffixes)}"
    elif pattern == 3:
        # Pattern: Test + Prefix
        role_name = f"Test {random.choice(role_prefixes)}"
    else:
        # Pattern: Auto + Department + Prefix
        role_name = f"Auto {random.choice(departments)} {random.choice(role_prefixes)}"
    
    return role_name


def generate_permission_set():
    """
    Generate a random set of permissions for testing
    
    Returns:
        list: List of permission names
    """
    all_permissions = [
        "Dashboard",
        "Talent Read",
        "Talent Create", 
        "Talent Update",
        "Talent Delete",
        "Company Read",
        "Company Create",
        "Company Update", 
        "Company Delete",
        "Agency Read",
        "Agency Create",
        "Agency Update",
        "Agency Delete",
        "User Management",
        "Reports Read",
        "Reports Create",
        "Settings Read",
        "Settings Update"
    ]
    
    # Always include Dashboard as it's usually required
    selected_permissions = ["Dashboard"]
    
    # Randomly select 2-6 additional permissions
    additional_count = random.randint(2, 6)
    remaining_permissions = [p for p in all_permissions if p != "Dashboard"]
    
    additional_permissions = random.sample(remaining_permissions, 
                                         min(additional_count, len(remaining_permissions)))
    
    selected_permissions.extend(additional_permissions)
    
    return selected_permissions


def generate_test_role_data_set():
    """
    Generate a complete role data set with name and permissions
    
    Returns:
        dict: Dictionary containing role_name and permissions
    """
    return {
        'role_name': generate_role_name(),
        'permissions': generate_permission_set()
    }


def generate_multiple_role_names(count: int = 5):
    """
    Generate multiple unique role names
    
    Args:
        count: Number of role names to generate
        
    Returns:
        list: List of unique role names
    """
    role_names = []
    for i in range(count):
        role_names.append(generate_role_name())
        # Small delay to ensure unique timestamps
        time.sleep(0.1)
    
    return role_names


def generate_role_hierarchy():
    """
    Generate a set of roles with hierarchical permissions (Admin > Manager > User)
    
    Returns:
        dict: Dictionary with role hierarchy
    """
    
    return {
        'admin_role': {
            'role_name': "Test Admin Role",
            'permissions': [
                "Dashboard",
                "Talent Read", "Talent Create", "Talent Update", "Talent Delete",
                "Company Read", "Company Create", "Company Update", "Company Delete", 
                "Agency Read", "Agency Create", "Agency Update", "Agency Delete",
                "User Management",
                "Reports Read", "Reports Create",
                "Settings Read", "Settings Update"
            ]
        },
        'manager_role': {
            'role_name': "Test Manager Role",
            'permissions': [
                "Dashboard",
                "Talent Read", "Talent Create", "Talent Update",
                "Company Read", "Company Update",
                "Agency Read",
                "Reports Read"
            ]
        },
        'user_role': {
            'role_name': "Test User Role", 
            'permissions': [
                "Dashboard",
                "Talent Read",
                "Company Read",
                "Agency Read"
            ]
        }
    }
