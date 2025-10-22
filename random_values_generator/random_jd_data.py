"""
Random JD Data Generator
Generates unique job description data for testing JD functionality
"""

import random
import time
from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class JDTestData:
    """Data structure for JD test data"""
    position_title: str
    company: str
    work_style: str
    workplace: str
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    currency: Optional[str] = None
    job_age_min: Optional[int] = None
    job_age_max: Optional[int] = None
    target_age_min: Optional[int] = None
    target_age_max: Optional[int] = None
    japanese_level: Optional[str] = None
    english_level: Optional[str] = None
    priority_grade: Optional[str] = None
    hiring_status: Optional[str] = None
    employment_type: Optional[str] = None
    department: Optional[str] = None
    direct_report: Optional[str] = None
    job_function: Optional[str] = None
    client: Optional[str] = None


def generate_position_title():
    """
    Generate a realistic position title for testing
    
    Returns:
        str: Job position title
    """
    seniority_levels = [
        "Junior", "Senior", "Lead", "Principal", "Staff", "Associate", 
        "Mid-level", "Entry-level", "Executive", "Director"
    ]
    
    job_roles = [
        "Software Engineer", "Data Scientist", "Product Manager", "UX Designer",
        "DevOps Engineer", "Business Analyst", "Marketing Manager", "Sales Representative",
        "HR Specialist", "Financial Analyst", "Project Manager", "Quality Assurance Engineer",
        "Frontend Developer", "Backend Developer", "Full Stack Developer", "Mobile Developer",
        "System Administrator", "Database Administrator", "Security Engineer", "Cloud Architect",
        "Scrum Master", "Technical Writer", "Customer Success Manager", "Operations Manager"
    ]
    
    specializations = [
        "React", "Python", "Java", "JavaScript", "AWS", "Azure", "Machine Learning",
        "AI", "Blockchain", "Mobile", "Web", "Enterprise", "Startup", "E-commerce",
        "FinTech", "HealthTech", "EdTech", "Gaming", "SaaS", "B2B", "B2C"
    ]
    
    # Generate timestamp for uniqueness
    timestamp = str(int(time.time()))[-4:]
    
    # Random selection with different patterns
    pattern = random.choice([1, 2, 3, 4])
    
    if pattern == 1:
        # Seniority + Role
        title = f"{random.choice(seniority_levels)} {random.choice(job_roles)}"
    elif pattern == 2:
        # Role + Specialization
        title = f"{random.choice(job_roles)} - {random.choice(specializations)}"
    elif pattern == 3:
        # Seniority + Role + Specialization
        title = f"{random.choice(seniority_levels)} {random.choice(job_roles)} ({random.choice(specializations)})"
    else:
        # Simple role
        title = random.choice(job_roles)
    
    # Add timestamp for uniqueness in testing
    return f"{title} {timestamp}"


def generate_workplace_location():
    """
    Generate random workplace locations
    
    Returns:
        str: Workplace location
    """
    cities = [
        "Tokyo", "Osaka", "Kyoto", "Yokohama", "Nagoya", "Sapporo", "Fukuoka", "Kobe",
        "Sendai", "Hiroshima", "New York", "San Francisco", "London", "Singapore",
        "Sydney", "Toronto", "Berlin", "Amsterdam", "Stockholm", "Copenhagen"
    ]
    
    workplace_types = [
        "Office", "Remote", "Hybrid", "Co-working Space", "Headquarters", 
        "Branch Office", "Regional Office", "Innovation Center", "R&D Center"
    ]
    
    # Generate different workplace formats
    format_type = random.choice([1, 2, 3])
    
    if format_type == 1:
        # City + Office type
        return f"{random.choice(cities)} {random.choice(workplace_types)}"
    elif format_type == 2:
        # Just city
        return random.choice(cities)
    else:
        # Just workplace type
        return random.choice(workplace_types)


def generate_company_name():
    """
    Generate company name for JD testing
    
    Returns:
        str: Company name
    """
    prefixes = [
        "Tech", "Global", "Digital", "Smart", "Future", "Advanced", "Modern",
        "Dynamic", "Strategic", "Premier", "Elite", "Progressive", "Innovative"
    ]
    
    suffixes = [
        "Solutions", "Systems", "Technologies", "Corp", "Inc", "Ltd", "Group",
        "Associates", "Partners", "Consulting", "Services", "Industries", "Labs"
    ]
    
    timestamp = str(int(time.time()))[-4:]
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    
    return f"{prefix} {suffix} {timestamp}"


def generate_work_style():
    """
    Generate work style options - only use options available in the dropdown
    
    Returns:
        str: Work style
    """
    # Only use the exact options available in the system dropdown
    work_styles = [
        "Remote", "On-site", "Hybrid"
    ]
    
    return random.choice(work_styles)


def generate_salary_range():
    """
    Generate realistic salary range
    
    Returns:
        tuple: (min_salary, max_salary)
    """
    base_salaries = [
        (30000, 50000),   # Entry level
        (50000, 80000),   # Mid level
        (80000, 120000),  # Senior level
        (120000, 180000), # Lead level
        (180000, 250000)  # Executive level
    ]
    
    min_sal, max_sal = random.choice(base_salaries)
    
    # Add some variation
    variation = random.randint(-5000, 10000)
    min_salary = max(25000, min_sal + variation)
    max_salary = min_salary + random.randint(20000, 50000)
    
    return min_salary, max_salary


def generate_age_range():
    """
    Generate realistic age range
    
    Returns:
        tuple: (min_age, max_age)
    """
    age_ranges = [
        (22, 30),  # Fresh graduates
        (25, 35),  # Early career
        (30, 45),  # Mid career
        (35, 50),  # Senior career
        (40, 60)   # Executive level
    ]
    
    return random.choice(age_ranges)


def generate_language_level():
    """
    Generate language proficiency level (matching actual system options)
    
    Returns:
        str: Language level
    """
    levels = [
        "Basic", "Conversational", "Fluent", "Native"
    ]
    
    return random.choice(levels)


def generate_priority_grade():
    """
    Generate priority grade (matching actual system options)
    
    Returns:
        str: Priority grade
    """
    grades = ["AAA", "AA", "A", "BBB", "BB"]
    return random.choice(grades)


def generate_hiring_status():
    """
    Generate hiring status (matching actual system options)
    
    Returns:
        str: Hiring status
    """
    statuses = ["Open", "Urgent", "Closed"]
    return random.choice(statuses)


def generate_employment_type():
    """
    Generate employment type (matching actual system options)
    
    Returns:
        str: Employment type
    """
    types = [
        "Part-time", "Permanent", "Self-employed", "Freelance", 
        "Contract", "Internship", "Apprenticeship", "Indirect Contract"
    ]
    return random.choice(types)


def generate_department():
    """
    Generate department name
    
    Returns:
        str: Department name
    """
    departments = [
        "Engineering", "Product", "Design", "Marketing", "Sales", "HR",
        "Finance", "Operations", "Customer Success", "Business Development",
        "Quality Assurance", "DevOps", "Data Science", "Security", "Legal"
    ]
    return random.choice(departments)


def generate_job_function():
    """
    Generate job function
    
    Returns:
        str: Job function
    """
    functions = [
        "Development", "Management", "Analysis", "Design", "Testing",
        "Support", "Research", "Strategy", "Implementation", "Optimization",
        "Coordination", "Leadership", "Innovation", "Consultation"
    ]
    return random.choice(functions)


def generate_currency():
    """
    Generate currency code
    
    Returns:
        str: Currency code
    """
    currencies = ["USD", "JPY", "EUR", "GBP", "CAD", "AUD", "SGD", "HKD"]
    return random.choice(currencies)


def generate_complete_jd_data():
    """
    Generate complete JD data set with all fields
    
    Returns:
        JDTestData: Complete JD data object
    """
    min_salary, max_salary = generate_salary_range()
    job_age_min, job_age_max = generate_age_range()
    target_age_min, target_age_max = generate_age_range()
    
    return JDTestData(
        position_title=generate_position_title(),
        company=generate_company_name(),
        work_style=generate_work_style(),
        workplace=generate_workplace_location(),
        min_salary=min_salary,
        max_salary=max_salary,
        currency=generate_currency(),
        job_age_min=job_age_min,
        job_age_max=job_age_max,
        target_age_min=target_age_min,
        target_age_max=target_age_max,
        japanese_level=generate_language_level(),
        english_level=generate_language_level(),
        priority_grade=generate_priority_grade(),
        hiring_status=generate_hiring_status(),
        employment_type=generate_employment_type(),
        department=generate_department(),
        direct_report=generate_job_function(),
        job_function=generate_job_function()
    )


def generate_minimal_jd_data():
    """
    Generate minimal JD data with only required fields
    
    Returns:
        JDTestData: Minimal JD data object
    """
    return JDTestData(
        position_title=generate_position_title(),
        company=generate_company_name(),
        work_style=generate_work_style(),
        workplace=generate_workplace_location()
    )


def generate_invalid_jd_data_cases():
    """
    Generate invalid JD data for validation testing
    
    Returns:
        list: List of invalid JD data cases with descriptions
    """
    invalid_cases = [
        {
            'data': JDTestData(
                position_title="",
                company=generate_company_name(),
                work_style=generate_work_style(),
                workplace=generate_workplace_location()
            ),
            'description': 'Empty position title',
            'expected_error': 'Position Job Title is required'
        },
        {
            'data': JDTestData(
                position_title=generate_position_title(),
                company="",
                work_style=generate_work_style(),
                workplace=generate_workplace_location()
            ),
            'description': 'Empty company',
            'expected_error': 'Company is required'
        },
        {
            'data': JDTestData(
                position_title=generate_position_title(),
                company=generate_company_name(),
                work_style="",
                workplace=generate_workplace_location()
            ),
            'description': 'Empty work style',
            'expected_error': 'Work Style is required'
        },
        {
            'data': JDTestData(
                position_title=generate_position_title(),
                company=generate_company_name(),
                work_style=generate_work_style(),
                workplace=""
            ),
            'description': 'Empty workplace',
            'expected_error': 'JD Workplace is required'
        },
        {
            'data': JDTestData(
                position_title=generate_position_title(),
                company=generate_company_name(),
                work_style=generate_work_style(),
                workplace=generate_workplace_location(),
                min_salary=100000,
                max_salary=50000
            ),
            'description': 'Invalid salary range (max < min)',
            'expected_error': 'Maximum salary must be greater than minimum salary'
        },
        {
            'data': JDTestData(
                position_title=generate_position_title(),
                company=generate_company_name(),
                work_style=generate_work_style(),
                workplace=generate_workplace_location(),
                job_age_min=50,
                job_age_max=25
            ),
            'description': 'Invalid age range (max < min)',
            'expected_error': 'Maximum age must be greater than minimum age'
        }
    ]
    
    return invalid_cases


def generate_multiple_jd_data(count: int = 5):
    """
    Generate multiple unique JD data sets
    
    Args:
        count: Number of JD data sets to generate
        
    Returns:
        list: List of JDTestData objects
    """
    jd_list = []
    for i in range(count):
        jd_list.append(generate_complete_jd_data())
        # Small delay to ensure unique timestamps
        time.sleep(0.1)
    
    return jd_list


def generate_bulk_jd_data(count: int = 20):
    """
    Generate bulk JD data for performance testing
    
    Args:
        count: Number of JDs to generate
        
    Returns:
        list: List of JD data for bulk operations
    """
    bulk_jds = []
    
    for i in range(count):
        jd_data = generate_complete_jd_data()
        # Add batch identifier for tracking
        jd_data.batch_id = f"BULK_{int(time.time())}_{i:03d}"
        bulk_jds.append(jd_data)
        
        # Very small delay to ensure uniqueness
        time.sleep(0.01)
    
    return bulk_jds


def generate_search_test_data():
    """
    Generate JD data specifically for search testing
    
    Returns:
        dict: Dictionary with search-specific JD data
    """
    timestamp = str(int(time.time()))[-4:]
    
    return {
        'searchable_jd': JDTestData(
            position_title=f"Searchable Engineer Position {timestamp}",
            company=f"Searchable Tech Corp {timestamp}",
            work_style="Remote",
            workplace="Tokyo Office",
            department="Engineering"
        ),
        'unique_jd': JDTestData(
            position_title=f"Unique Developer Role {timestamp}",
            company=f"Unique Solutions Ltd {timestamp}",
            work_style="Hybrid",
            workplace="Osaka Branch",
            department="Development"
        ),
        'common_jd': JDTestData(
            position_title=f"Software Engineer {timestamp}",
            company=f"Tech Solutions {timestamp}",
            work_style="On-site",
            workplace="Remote",
            department="Technology"
        )
    }


def generate_filter_test_data():
    """
    Generate JD data specifically for filter testing
    
    Returns:
        dict: Dictionary with filter-specific JD data
    """
    timestamp = str(int(time.time()))[-4:]
    
    return {
        'remote_jd': JDTestData(
            position_title=f"Remote Developer {timestamp}",
            company=f"Remote Corp {timestamp}",
            work_style="Remote",
            workplace="Remote Office",
            hiring_status="Open",
            employment_type="Full-time"
        ),
        'onsite_jd': JDTestData(
            position_title=f"Onsite Manager {timestamp}",
            company=f"Onsite Inc {timestamp}",
            work_style="On-site",
            workplace="Tokyo Headquarters",
            hiring_status="In Progress",
            employment_type="Full-time"
        ),
        'hybrid_jd': JDTestData(
            position_title=f"Hybrid Analyst {timestamp}",
            company=f"Hybrid Solutions {timestamp}",
            work_style="Hybrid",
            workplace="Flexible Location",
            hiring_status="Open",
            employment_type="Part-time"
        )
    }


def generate_edge_case_jd_data():
    """
    Generate edge case JD data for validation testing
    
    Returns:
        list: List of edge case JD data with descriptions
    """
    edge_cases = [
        {
            'data': JDTestData(
                position_title="A",  # Minimum length
                company="B",
                work_style="Remote",
                workplace="C"
            ),
            'description': 'Minimum length fields'
        },
        {
            'data': JDTestData(
                position_title="A" * 100,  # Maximum length
                company="B" * 100,
                work_style="Remote",
                workplace="C" * 100
            ),
            'description': 'Maximum length fields'
        },
        {
            'data': JDTestData(
                position_title="Position with Special Characters !@#$%",
                company="Company & Associates Ltd.",
                work_style="Remote",
                workplace="Location (Building A)"
            ),
            'description': 'Special characters in fields'
        },
        {
            'data': JDTestData(
                position_title="   Position with Spaces   ",
                company="   Company with Spaces   ",
                work_style="Remote",
                workplace="   Workplace with Spaces   "
            ),
            'description': 'Fields with leading/trailing spaces'
        }
    ]
    
    return edge_cases


def validate_jd_data(jd_data: JDTestData) -> Dict[str, bool]:
    """
    Validate JD data against field requirements
    
    Args:
        jd_data: JD data to validate
        
    Returns:
        dict: Validation results for each field
    """
    validation_results = {
        'position_title_valid': bool(jd_data.position_title and jd_data.position_title.strip()),
        'company_valid': bool(jd_data.company and jd_data.company.strip()),
        'work_style_valid': bool(jd_data.work_style and jd_data.work_style.strip()),
        'workplace_valid': bool(jd_data.workplace and jd_data.workplace.strip()),
        'salary_range_valid': True,
        'age_range_valid': True
    }
    
    # Validate salary range if both values are provided
    if jd_data.min_salary is not None and jd_data.max_salary is not None:
        validation_results['salary_range_valid'] = jd_data.max_salary > jd_data.min_salary
    
    # Validate age range if both values are provided
    if jd_data.job_age_min is not None and jd_data.job_age_max is not None:
        validation_results['age_range_valid'] = jd_data.job_age_max > jd_data.job_age_min
    
    return validation_results


# Test data constants for specific scenarios
TEST_JD_DATA = {
    "valid_minimal": {
        "position_title": "Test Software Engineer",
        "company": "Test Tech Corp",
        "work_style": "Remote",
        "workplace": "Test Office"
    },
    "valid_complete": {
        "position_title": "Senior Full Stack Developer",
        "company": "Innovation Tech Solutions",
        "work_style": "Hybrid",
        "workplace": "Tokyo Innovation Center",
        "min_salary": 80000,
        "max_salary": 120000,
        "currency": "USD",
        "department": "Engineering",
        "employment_type": "Full-time"
    },
    "invalid_empty_title": {
        "position_title": "",
        "company": "Test Company",
        "work_style": "Remote",
        "workplace": "Test Office"
    },
    "invalid_salary_range": {
        "position_title": "Test Position",
        "company": "Test Company", 
        "work_style": "Remote",
        "workplace": "Test Office",
        "min_salary": 100000,
        "max_salary": 50000
    }
}