import pytest
import time
import re
from playwright.sync_api import Page, expect
from utils import company_helper
from utils.company_helper import ComprehensiveCompanyTestHelper
from utils.enhanced_assertions import enhanced_assert_visible
from pages.company_page import CompanyPage

def test_TC_01_comprehensive_company_creation_and_editing(page: Page):
    """Verify all the fields of summary tab are editable and retain values after editing."""
    
    # Use helper function for company creation and navigation
    initial_values, updated_values, company_page = ComprehensiveCompanyTestHelper.company_create_to_details_page(page)
    
    # Use helper function for company name editing with validation
    ComprehensiveCompanyTestHelper.edit_and_assert_company_name_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for website editing with validation
    ComprehensiveCompanyTestHelper.edit_and_assert_website_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for industry editing
    ComprehensiveCompanyTestHelper.edit_and_assert_industry_field(page, company_page, initial_values, updated_values)
        
    # Use helper function for HQ in Japan editing
    ComprehensiveCompanyTestHelper.edit_and_assert_hq_in_japan_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for Global HQ editing
    ComprehensiveCompanyTestHelper.edit_and_assert_global_hq_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for Country of Origin editing
    ComprehensiveCompanyTestHelper.edit_and_assert_country_of_origin_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for address editing
    ComprehensiveCompanyTestHelper.edit_and_assert_address_field(page, company_page, initial_values, updated_values)

    # Use helper function for Company hiring status editing
    ComprehensiveCompanyTestHelper.edit_and_assert_company_hiring_status_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for Job opening editing
    ComprehensiveCompanyTestHelper.edit_and_assert_job_opening_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for Total employees JPN editing
    ComprehensiveCompanyTestHelper.edit_and_assert_total_employees_jpn_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for Company grade editing
    ComprehensiveCompanyTestHelper.edit_and_assert_company_grade_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for Main TEL editing
    ComprehensiveCompanyTestHelper.edit_and_assert_main_tel_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for HR TEL editing
    ComprehensiveCompanyTestHelper.edit_and_assert_hr_tel_field(page, company_page, initial_values, updated_values)
    
    
    print("🎉 COMPREHENSIVE TEST COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("📊 SUMMARY:")
    print(f"✅ Created company: {initial_values['company_name']}")
    print(f"✅ Navigated to details page successfully")
    print(f"✅ Edited company name field successfully with validation")
    print(f"✅ Edited website field successfully with validation") 
    print(f"✅ Edited industry field successfully")
    print(f"✅ Edited address field successfully")
    print(f"✅ Edited HQ in Japan field successfully")
    print(f"✅ Edited Global HQ field successfully")
    print(f"✅ Edited Country of Origin field successfully")
    print(f"✅ Edited Company hiring status field successfully")
    print(f"✅ Edited Job opening field successfully")
    print(f"✅ Edited Total employees JPN field successfully")
    print(f"✅ Edited Company grade field successfully")
    print(f"✅ Edited Main TEL field successfully")
    print(f"✅ Edited HR TEL field successfully")
    print(f"✅ All {13} Summary tab fields edited and assertions passed")
    print(f"🏆 Final company name: {updated_values['company_name']}")
    print("=" * 80)
