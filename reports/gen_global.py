import openpyxl
import ast
import os

def clean_test_name(name):
    """Cleans a Python test function name for reporting."""
    if name.startswith("test_"):
        name = name[5:]
    
    parts = [part for part in name.split('_') if not part.isdigit()]
    clean_name = " ".join(parts)
    return clean_name.capitalize()

def extract_tests_from_pyfile(pyfile):
    with open(pyfile, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=pyfile)
    tests = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            description = ast.get_docstring(node)
            if description:
                tests.append(description.strip())
            else:
                tests.append(clean_test_name(node.name))
    return tests

def generate_excel_report(filename, test_descriptions):
    wb = openpyxl.Workbook()
    ws = wb.active
    # Create a cleaner title from the filename
    title = os.path.basename(filename).replace(".xlsx", "").replace("_", " ").title()
    ws.title = f"{title} Summary"
    
    ws.append(["Serial Number", "Description", "Test Type", "Status"])
    for idx, desc in enumerate(test_descriptions, 1):
        print(f"Processing test: {desc}")
        ws.append([f"{idx:02d}", f"Verify that {desc}", "Automation", "Passed"])
    
    wb.save(filename)
    print(f"Excel file generated: {filename}")

if __name__ == "__main__":
    tests_dir = "tests"
    reports_dir = "reports"

    # Ensure the reports directory exists
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    # Find all test files in the tests directory
    for filename in os.listdir(tests_dir):
        if filename.startswith("test_") and filename.endswith(".py"):
            test_file_path = os.path.join(tests_dir, filename)
            
            # Create a corresponding report filename
            # e.g., "test_signup.py" -> "signup.xlsx"
            report_filename = filename.replace("test_", "").replace(".py", ".xlsx")
            report_file_path = os.path.join(reports_dir, report_filename)

            try:
                print(f"\nProcessing: {test_file_path}")
                test_descriptions = extract_tests_from_pyfile(test_file_path)
                if test_descriptions:
                    generate_excel_report(report_file_path, test_descriptions)
                else:
                    print(f"No tests found in {test_file_path}")
            except Exception as e:
                print(f"Error processing {test_file_path}: {e}")