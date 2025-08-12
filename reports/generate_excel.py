import openpyxl
import ast
import os
import pytest

# --- Helper functions (no changes here) ---
def clean_test_name(name):
    """Cleans a Python test function name for reporting."""
    if name.startswith("test_"):
        name = name[5:]
    
    parts = [part for part in name.split('_') if not part.isdigit()]
    clean_name = " ".join(parts)
    return clean_name.capitalize()

def extract_test_descriptions(pyfile):
    """Extracts docstrings or clean names from a test file."""
    with open(pyfile, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=pyfile)
    
    descriptions = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            docstring = ast.get_docstring(node)
            if docstring:
                descriptions[node.name] = docstring.strip()
            else:
                descriptions[node.name] = clean_test_name(node.name)
    return descriptions

# --- New Function to Run Tests and Capture Results ---
def run_tests_and_get_results(test_file_path):
    """
    Runs tests using pytest and captures the outcome of each test.
    Returns a dictionary mapping test name to its status ('Passed', 'Failed', etc.).
    """
    
    class ResultCollector:
        def __init__(self):
            self.results = {}

        def pytest_runtest_logreport(self, report):
            # This hook is called for each test phase (setup, call, teardown)
            if report.when == 'call':
                # We only care about the 'call' phase result
                test_name = report.nodeid.split("::")[-1]
                self.results[test_name] = report.outcome.capitalize()

    # Create an instance of our result collector
    result_collector = ResultCollector()
    
    # Run pytest on the specified file, using our collector as a plugin
    pytest.main([test_file_path, "-v"], plugins=[result_collector])
    
    return result_collector.results

# --- Updated Excel Generation Function ---
def generate_excel_report(filename, test_descriptions, test_results):
    wb = openpyxl.Workbook()
    ws = wb.active
    title = os.path.basename(filename).replace(".xlsx", "").replace("_", " ").title()
    ws.title = f"{title} Summary"
    
    ws.append(["Serial Number", "Description", "Test Type", "Status"])
    
    # Loop through the collected test descriptions
    for idx, (test_name, desc) in enumerate(test_descriptions.items(), 1):
        # Get the status from the results, default to 'Skipped' if not found
        status = test_results.get(test_name, "Skipped")
        
        ws.append([f"{idx:02d}", f"Verify that {desc}", "Automation", status])
    
    wb.save(filename)
    print(f"Excel file generated: {filename}")

# --- Main Execution Block ---
if __name__ == "__main__":
    tests_dir = "tests"
    reports_dir = "reports"

    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    for filename in os.listdir(tests_dir):
        if filename.startswith("test_") and filename.endswith(".py"):
            test_file_path = os.path.join(tests_dir, filename)
            report_filename = filename.replace("test_", "").replace(".py", ".xlsx")
            report_file_path = os.path.join(reports_dir, report_filename)

            try:
                print(f"\n--- Processing: {test_file_path} ---")
                # 1. Run the tests and get real results
                test_results = run_tests_and_get_results(test_file_path)
                # 2. Statically extract descriptions
                test_descriptions = extract_test_descriptions(test_file_path)
                if test_descriptions:
                    # 3. Generate the report with descriptions and results
                    generate_excel_report(report_file_path, test_descriptions, test_results)
                else:
                    print(f"No tests found in {test_file_path}")

            except Exception as e:
                print(f"An error occurred while processing {test_file_path}: {e}")