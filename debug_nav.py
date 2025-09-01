"""
Quick test to debug the user management navigation
"""
import pytest
import time
from playwright.sync_api import Page
from utils.login_helper import do_login

def test_debug_user_management(page: Page):
    """Debug user management page structure"""
    
    # Login first
    do_login(page, "mi003b@onemail.host", "Kabir123#")
    time.sleep(3)
    
    # Click on demo 06
    demo_links = page.locator("text=demo 06")
    if demo_links.count() > 0:
        demo_links.first.click()
        time.sleep(3)
    
    # Click on User Management
    user_mgmt_link = page.get_by_text("User Management")
    if user_mgmt_link.count() > 0:
        user_mgmt_link.click()
        time.sleep(3)
        
    page.screenshot(path="debug_user_mgmt_page.png")
    print(f"Current URL: {page.url}")
    
    # Look for all buttons
    all_buttons = page.locator("button").all()
    print(f"Found {len(all_buttons)} buttons:")
    for i, btn in enumerate(all_buttons[:10]):  # Show first 10
        try:
            text = btn.text_content()
            if text and text.strip():
                print(f"  Button {i}: '{text.strip()}'")
        except:
            pass
    
    # Look for tabs
    print("\nLooking for tab-like elements:")
    tab_selectors = [
        "button:has-text('Roles')",
        "a:has-text('Roles')", 
        "[role='tab']",
        ".tab",
        "button:has-text('User List')",
        "a:has-text('User List')"
    ]
    
    for selector in tab_selectors:
        elements = page.locator(selector)
        if elements.count() > 0:
            print(f"  Found {elements.count()} elements with selector: {selector}")
            for i in range(min(elements.count(), 3)):
                try:
                    text = elements.nth(i).text_content()
                    print(f"    - {text}")
                except:
                    pass
    
    # Look for Create Role button
    create_role_selectors = [
        "button:has-text('Create Role')",
        "button:has-text('Create')",
        "a:has-text('Create Role')",
        "[class*='create']:has-text('Role')"
    ]
    
    print("\nLooking for Create Role button:")
    for selector in create_role_selectors:
        elements = page.locator(selector)
        if elements.count() > 0:
            print(f"  Found {elements.count()} elements with selector: {selector}")
            
    # Try clicking on Roles & Access if it exists
    roles_tab = page.get_by_text("Roles & Access")
    if roles_tab.count() > 0:
        print("Clicking on 'Roles & Access'...")
        roles_tab.click()
        time.sleep(3)
        page.screenshot(path="debug_after_roles_tab.png")
        print(f"URL after roles tab: {page.url}")
        
        # Look for all buttons again
        all_buttons_after = page.locator("button").all()
        print(f"Found {len(all_buttons_after)} buttons after clicking tab:")
        for i, btn in enumerate(all_buttons_after[:15]):  # Show first 15
            try:
                text = btn.text_content()
                if text and text.strip():
                    print(f"  Button {i}: '{text.strip()}'")
            except:
                pass
        
        # Now look for Create Role button again
        create_role_btn = page.locator("button:has-text('Create Role')")
        if create_role_btn.count() > 0:
            print(f"✅ Found Create Role button after clicking tab: {create_role_btn.count()}")
        else:
            print("❌ Still no Create Role button after clicking tab")
            
            # Try other variations
            create_variations = [
                "button:has-text('Create')",
                "button:has-text('Add Role')", 
                "button:has-text('New Role')",
                "[class*='create']",
                "a:has-text('Create')"
            ]
            
            for variation in create_variations:
                elements = page.locator(variation)
                if elements.count() > 0:
                    print(f"  Found {elements.count()} elements with '{variation}'")
                    for j in range(min(elements.count(), 2)):
                        try:
                            text = elements.nth(j).text_content()
                            print(f"    - {text}")
                        except:
                            pass
