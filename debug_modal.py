"""
Simple debug to see the Add Role modal fields
"""
import time
from playwright.sync_api import Page
from utils.login_helper import do_login

def test_debug_add_role_modal(page: Page):
    """Debug the Add Role modal to see actual field names"""
    
    # Login and navigate
    do_login(page, "mi003b@onemail.host", "Kabir123#")
    time.sleep(3)
    
    # Select demo agency
    demo_agency = page.get_by_text("demo 06")
    if demo_agency.count() > 0:
        demo_agency.click()
        time.sleep(3)
    
    # Navigate to user management by URL
    page.goto("https://bprp-qa.shadhinlab.xyz/agency/174/role-list")
    time.sleep(3)
    
    # Click Add Role
    add_role_btn = page.get_by_text("Add Role").first
    add_role_btn.click()
    time.sleep(2)
    
    # Take screenshot
    page.screenshot(path="debug_add_role_modal.png")
    
    # Find all input fields
    all_inputs = page.locator("input").all()
    print(f"Found {len(all_inputs)} input fields:")
    for i, input_elem in enumerate(all_inputs):
        try:
            name = input_elem.get_attribute("name") or "No name"
            placeholder = input_elem.get_attribute("placeholder") or "No placeholder" 
            input_type = input_elem.get_attribute("type") or "text"
            print(f"  Input {i}: name='{name}', placeholder='{placeholder}', type='{input_type}'")
        except:
            print(f"  Input {i}: Could not get attributes")
    
    # Find all textareas
    all_textareas = page.locator("textarea").all()
    print(f"Found {len(all_textareas)} textarea fields:")
    for i, textarea in enumerate(all_textareas):
        try:
            name = textarea.get_attribute("name") or "No name"
            placeholder = textarea.get_attribute("placeholder") or "No placeholder"
            print(f"  Textarea {i}: name='{name}', placeholder='{placeholder}'")
        except:
            print(f"  Textarea {i}: Could not get attributes")
    
    # Find all buttons
    all_buttons = page.locator("button").all()
    print(f"Found {len(all_buttons)} buttons:")
    for i, button in enumerate(all_buttons):
        try:
            text = button.text_content() or "No text"
            button_type = button.get_attribute("type") or "button"
            print(f"  Button {i}: text='{text}', type='{button_type}'")
        except:
            print(f"  Button {i}: Could not get text")
