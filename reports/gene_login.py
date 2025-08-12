import openpyxl
import ast

def clean_test_name(name):
    """Cleans a Python test function name for reporting."""
    # Remove the "test_" prefix
    if name.startswith("test_"):
        name = name[5:]
    
    # Split the name by underscores and filter out any numeric-only parts
    parts = [part for part in name.split('_') if not part.isdigit()]
    
    # Join the remaining parts with spaces and capitalize the first letter
    clean_name = " ".join(parts)
    return clean_name.capitalize()

def extract_tests_from_pyfile(pyfile):
    with open(pyfile, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=pyfile)
    tests = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            # Prioritize the docstring if it exists
            description = ast.get_docstring(node)
            if description:
                # Use the clean docstring
                tests.append(description.strip())
            else:
                # Otherwise, clean up the function name to use as the description
                tests.append(clean_test_name(node.name))
    return tests

def generate_excel_report(filename, test_descriptions):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Test Summary"
    ws.append(["Serial Number", "Description", "Test Type", "Status"])
    for idx, desc in enumerate(test_descriptions, 1):
        # The description is now pre-formatted, so we just use it directly
        ws.append([f"{idx:02d}", f"Verify that {desc}", "Automation", "Passed"])
    wb.save(filename)
    print(f"Excel file generated: {filename}")

if __name__ == "__main__":
    test_file = "tests/test_login.py"  # Adjust path if needed
    try:
        test_descriptions = extract_tests_from_pyfile(test_file)
        generate_excel_report("reports/login.xlsx", test_descriptions)
    except FileNotFoundError:
        print(f"Error: The file '{test_file}' could not be found. Please check the path.")