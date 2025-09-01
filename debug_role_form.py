"""
Debug script to check the actual form fields in Add Role modal
"""
from playwright.sync_api import sync_playwright
import time

def debug_role_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to login
        page.goto("https://bprp-qa.shadhinlab.xyz")
        
        # Login
        page.fill("input[type='email']", "mi003b@onemail.host")
        page.fill("input[type='password']", "Kabir123#")
        page.click("button[type='submit']")
        time.sleep(3)
        
        # Select demo agency
        page.click("text='demo 06'")
        time.sleep(2)
        
        # Navigate to user management via URL
        current_url = page.url
        agency_id = current_url.split("/agency/")[1].split("/")[0] if "/agency/" in current_url else None
        if agency_id:
            page.goto(f"https://bprp-qa.shadhinlab.xyz/agency/{agency_id}/role-list?page=1")
        time.sleep(3)
        
        # Click Add Role button
        page.click("text='Add Role'")
        time.sleep(2)
        
        # Debug all input fields in the modal
        print("🔍 Checking all input fields in the modal:")
        inputs = page.locator("input").all()
        for i, input_elem in enumerate(inputs):
            try:
                name_attr = input_elem.get_attribute("name")
                placeholder = input_elem.get_attribute("placeholder") 
                input_type = input_elem.get_attribute("type")
                label = ""
                try:
                    # Try to find associated label
                    label_elem = input_elem.locator("xpath=//label[@for='" + input_elem.get_attribute("id") + "']")
                    if label_elem.count() > 0:
                        label = label_elem.text_content()
                except:
                    pass
                
                if input_elem.is_visible():
                    print(f"Input {i}: name='{name_attr}', type='{input_type}', placeholder='{placeholder}', label='{label}'")
            except Exception as e:
                print(f"Error checking input {i}: {e}")
        
        # Check textareas too
        print("\n🔍 Checking all textarea fields:")
        textareas = page.locator("textarea").all()
        for i, textarea in enumerate(textareas):
            try:
                name_attr = textarea.get_attribute("name")
                placeholder = textarea.get_attribute("placeholder")
                if textarea.is_visible():
                    print(f"Textarea {i}: name='{name_attr}', placeholder='{placeholder}'")
            except Exception as e:
                print(f"Error checking textarea {i}: {e}")
                
        # Check form labels
        print("\n🔍 Checking all labels in modal:")
        labels = page.locator("label").all()
        for i, label in enumerate(labels):
            try:
                if label.is_visible():
                    text = label.text_content()
                    for_attr = label.get_attribute("for")
                    print(f"Label {i}: text='{text}', for='{for_attr}'")
            except Exception as e:
                print(f"Error checking label {i}: {e}")
        
        input("Press Enter to close browser...")
        browser.close()

if __name__ == "__main__":
    debug_role_form()
