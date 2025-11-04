"""
JD (Job Description) Locators for BPRP Web Application
Contains all locators for JD management features including creation, editing, listing, search, and filtering
"""

from playwright.sync_api import Page, Locator
import re


class JDLocators:
    def __init__(self, page: Page):
        self.page = page

        # ===== NAVIGATION & MAIN PAGE ELEMENTS =====
        self.jd_page_url = "https://bprp-qa.shadhinlab.xyz/agency/{agency_id}/jd"
        self.jd_page_heading = page.get_by_role("heading", name="Job Descriptions")
        self.search_input = page.get_by_role("textbox", name="Search...")
        self.filters_button = page.get_by_role("button", name="Filters")
        self.add_jd_button = page.get_by_role("button", name="Add JD")
        self.upload_file_button = page.get_by_role("button", name="Upload File")

        # ===== JD CREATION MODAL ELEMENTS =====
        self.jd_modal_heading = page.get_by_role("heading", name="Add New JD")
        self.jd_modal_body = page.locator(".modal-body, [class*='modal']")
        self.close_modal_button = page.get_by_role("button", name="Close modal")

        # Mandatory fields
        self.position_job_title_input = page.get_by_role(
            "textbox", name="Position Job Title"
        )
        # Company dropdown - more specific locator
        self.company_dropdown = page.locator("form").locator("div:has-text('Company'):not(:has-text('Work Style')):not(:has-text('Currency'))").locator(".chevron").first
        self.company_select_trigger = page.locator(".select-trigger").filter(
            has_text="Company"
        )
        
        # Work Style dropdown - more specific locator  
        self.work_style_dropdown = page.locator("form").locator("div:has-text('Work Style'):not(:has-text('Company')):not(:has-text('Currency'))").locator(".chevron").first
        self.work_style_select_trigger = page.locator(".select-trigger").filter(
            has_text="Work Style"
        )
        self.jd_workplace_input = page.get_by_role("textbox", name="JD Workplace")

        # Salary and compensation fields
        self.minimum_salary_input = page.get_by_role("textbox", name="Minimum Salary")
        self.maximum_salary_input = page.get_by_role("textbox", name="Maximum Salary")
        self.currency_dropdown = page.get_by_text('Currency')
        self.currency_select_trigger = page.locator(".select-trigger").filter(
            has_text="Currency"
        )

        # Age and experience fields
        self.job_age_min_input = page.get_by_role("textbox", name="Job Age Min")
        self.job_age_max_input = page.get_by_role("textbox", name="Job Age Max")
        self.target_age_min_input = page.get_by_role("textbox", name="Target Age Min")
        self.target_age_max_input = page.get_by_role("textbox", name="Target Age Max")

        # Language and skills - use the chevron/trigger to open dropdowns
        self.japanese_level_dropdown = page.get_by_text('Japanese Level')
        self.japanese_level_select_trigger = page.locator(".select-trigger").filter(
            has_text="Japanese Level"
        )
        self.english_level_dropdown = page.get_by_text('English Level')
        
        self.english_level_select_trigger = page.locator(".select-trigger").filter(
            has_text="English Level"
        )

        # Additional fields - use the chevron/trigger to open dropdowns
        # Priority Grade dropdown - use .last to avoid conflicts with multiple "Priority Grade" texts
        self.priority_grade_dropdown = page.get_by_text('Priority Grade').last
        self.priority_grade_select_trigger = page.locator(".select-trigger").filter(
            has_text="Priority Grade"
        )
        # Client dropdown - using .last to get the one in modal (not sidebar)
        # First "Client" is sidebar menu link, last "Client" is in the modal form
        self.client_dropdown = page.get_by_text('Client').last
        self.client_select_trigger = page.locator(".select-trigger").filter(
            has_text="Client"
        )
        self.hiring_status_dropdown = page.get_by_text("Hiring Status").last
        self.hiring_status_select_trigger = page.locator(".select-trigger").filter(
            has_text="Hiring Status"
        )
        self.employment_type_dropdown = page.get_by_text('Employment Type').last
        self.employment_type_select_trigger = page.locator(".select-trigger").filter(
            has_text="Employment Type"
        )
        self.department_input = page.get_by_role("textbox", name="Department")
        self.direct_report_input = page.get_by_role("textbox", name="Direct Report")
        self.job_function_input = page.get_by_role("textbox", name="Job Function")

        # File upload
        self.upload_jd_file_area = page.locator("div").filter(
            has_text="Upload JD file (optional)"
        )
        self.file_upload_input = page.locator("input[type='file']")
        self.upload_area = page.locator(".upload, [class*='upload']")

        # Modal actions
        self.save_button = page.get_by_role("button", name="Save")
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.update_button = page.get_by_role("button", name="Update")

        # ===== DROPDOWN OPTIONS =====
        # Company options (dynamic based on available companies)
        self.company_option = lambda company_name: page.get_by_text(
            company_name, exact=True
        )

        # Work style options
        self.remote_work_option = page.get_by_text("Remote")
        self.onsite_work_option = page.get_by_text("On-site")
        self.hybrid_work_option = page.get_by_text("Hybrid")

        # Currency options
        self.jpy_currency_option = page.get_by_text("JPY")
        self.usd_currency_option = page.get_by_text("USD")
        self.eur_currency_option = page.get_by_text("EUR")
        self.gbp_currency_option = page.get_by_text("GBP")

        # Client options (actual system values)
        self.client_new_option = page.get_by_text("client new")

        # Language level options (actual options from the system)
        # Using .first to handle duplicate text between Japanese and English dropdowns
        self.native_level_option = page.get_by_text("Native").first
        self.fluent_level_option = page.get_by_text("Fluent").first
        self.conversational_level_option = page.get_by_text("Conversational").first
        self.basic_level_option = page.get_by_text("Basic").first

        # Priority grade options (actual system values)
        self.aaa_priority_option = page.get_by_text("AAA")
        self.aa_priority_option = page.get_by_text("AA")
        self.a_priority_option = page.get_by_text("A")
        self.bbb_priority_option = page.get_by_text("BBB")
        self.bb_priority_option = page.get_by_text("BB")

        # Hiring status options (actual system values)
        self.open_status_option = page.get_by_text("Open")
        self.urgent_status_option = page.get_by_text("Urgent")
        self.closed_status_option = page.get_by_text("Closed")

        # Employment type options (actual system values)
        self.part_time_option = page.get_by_text("Part-time")
        self.permanent_option = page.get_by_text("Permanent")
        self.self_employed_option = page.get_by_text("Self-employed")
        self.freelance_option = page.get_by_text("Freelance")
        self.contract_option = page.get_by_text("Contract")
        self.internship_option = page.get_by_text("Internship")
        self.apprenticeship_option = page.get_by_text("Apprenticeship")
        self.indirect_contract_option = page.get_by_text("Indirect Contract")

        # ===== VALIDATION ERROR MESSAGES =====
        # Required field errors (matching actual validation messages from the page)
        self.position_title_required_error = page.get_by_text(" Job title is required.")
        self.company_required_error = page.get_by_text("Company is required.")
        self.work_style_required_error = page.get_by_text("Work style is required.")
        self.salary_required_error = page.get_by_text(" Salary is required")
        self.target_age_min_required_error = page.get_by_text(" Target age min is required")
        self.target_age_max_required_error = page.get_by_text(" Target age max is required")
        self.client_required_error = page.get_by_text("Client is required.")
        self.hiring_status_required_error = page.get_by_text("Hiring status is required.")

        # Format validation errors
        self.invalid_salary_range_error = page.get_by_text(
            "Minimum salary must be lesser than maximum salary."
        )
        self.invalid_age_range_error = page.get_by_text(
            "Maximum age must be greater than minimum age"
        )
        self.invalid_target_age_range_error = page.get_by_text(
            "Minimum target age must be lesser than maximum age."
        )
        self.invalid_email_format_error = page.get_by_text(
            "Please enter a valid email address"
        )
        self.invalid_url_format_error = page.get_by_text("Please enter a valid URL")

        # Character limit errors
        self.position_title_max_length_error = page.get_by_text(
            "Position title cannot exceed 100 characters"
        )
        self.workplace_max_length_error = page.get_by_text(
            "Workplace cannot exceed 200 characters"
        )
        self.department_max_length_error = page.get_by_text(
            "Department cannot exceed 100 characters"
        )
        self.job_function_max_length_error = page.get_by_text(
            "Job function cannot exceed 200 characters"
        )

        # File upload errors
        self.file_format_error = page.get_by_text("Only accept PDF, DOC, DOCX files")
        self.file_size_error = page.get_by_text("File can't be larger than 10 MB")
        self.file_upload_failed_error = page.get_by_text("File upload failed")

        # Numeric validation errors
        self.invalid_salary_format_error = page.get_by_text(
            "Please enter a valid salary amount"
        )
        self.invalid_age_format_error = page.get_by_text("Please enter a valid age")
        self.negative_salary_error = page.get_by_text("Salary cannot be negative")
        self.negative_age_error = page.get_by_text("Age cannot be negative")

        # ===== SUCCESS MESSAGES =====
        self.jd_created_successfully_message = page.get_by_text(
            "JD created successfully"
        )
        self.jd_updated_successfully_message = page.get_by_text(
            "JD updated successfully"
        )
        self.jd_deleted_successfully_message = page.get_by_text(
            "JD deleted successfully"
        )
        self.bulk_jd_deleted_successfully_message = page.get_by_text(
            "Selected JDs deleted successfully"
        )
        self.bulk_status_updated_successfully_message = page.get_by_text(
            "JD status updated successfully"
        )
        self.file_uploaded_successfully_message = page.get_by_text(
            "File uploaded successfully"
        )

        # ===== JD LIST ELEMENTS =====
        self.no_jds_message = page.get_by_text("No JD found")
        self.add_new_jd_button = page.get_by_role("button", name="Add new JD")
        self.jd_list_container = page.locator(".jd-list, [class*='jd-list']")
        self.jd_cards_container = page.locator(".jd-cards, [class*='cards']")

        # JD card elements (dynamic based on JD data)
        self.jd_card = lambda title: page.get_by_role("heading", name=title)
        self.jd_card_by_company = lambda company: page.locator(
            f"[data-company='{company}'], .jd-card:has-text('{company}')"
        )
        self.jd_card_title = page.locator(".jd-title, [class*='title']")
        self.jd_card_company = page.locator(".jd-company, [class*='company']")
        self.jd_card_status = page.locator(".jd-status, [class*='status']")
        self.jd_card_work_style = page.locator(".jd-work-style, [class*='work-style']")
        self.jd_card_salary = page.locator(".jd-salary, [class*='salary']")

        # JD actions (edit, delete, view)
        self.jd_actions_menu = page.locator(".jd-actions, [class*='actions']")
        self.jd_three_dots_menu = page.locator(".three-dots, [class*='menu']")
        self.edit_jd_button = page.get_by_role("button", name="Edit")
        self.delete_jd_button = page.get_by_role("button", name="Delete")
        self.view_jd_button = page.get_by_role("button", name="View")

        # Dynamic JD action buttons by title
        self.edit_jd_button_by_title = lambda title: page.locator(
            f".jd-card:has-text('{title}')"
        ).get_by_role("button", name="Edit")
        self.delete_jd_button_by_title = lambda title: page.locator(
            f".jd-card:has-text('{title}')"
        ).get_by_role("button", name="Delete")
        self.view_jd_button_by_title = lambda title: page.locator(
            f".jd-card:has-text('{title}')"
        ).get_by_role("button", name="View")

        # ===== FILTER PANEL ELEMENTS =====
        self.filter_panel = page.locator(".filter-panel, [class*='filter']")
        self.filter_overlay = page.locator(".filter-overlay, .backdrop")
        self.close_filter_button = page.get_by_role("button", name="Close filters")

        # Filter options
        self.company_name_filter = page.get_by_text("Company Name")
        self.company_filter_dropdown = page.locator(
            ".company-filter select, [name='companyFilter']"
        )
        self.position_title_filter = page.get_by_text("Position Job Title")
        self.position_filter_input = page.locator(
            "input[name='positionFilter'], .position-filter input"
        )
        self.hiring_status_filter = page.get_by_text("Hiring Status")
        self.status_filter_dropdown = page.locator(
            ".status-filter select, [name='statusFilter']"
        )
        self.work_style_filter = page.get_by_text("Work Style")
        self.work_style_filter_dropdown = page.locator(
            ".work-style-filter select, [name='workStyleFilter']"
        )
        self.salary_range_filter = page.get_by_text("Salary Range")
        self.min_salary_filter_input = page.locator(
            "input[name='minSalaryFilter'], .min-salary-filter input"
        )
        self.max_salary_filter_input = page.locator(
            "input[name='maxSalaryFilter'], .max-salary-filter input"
        )

        # Filter actions
        self.apply_filters_button = page.get_by_role("button", name="Apply Filters")
        self.all_clear_button = page.get_by_role("button", name="All clear")
        self.reset_filters_button = page.get_by_role("button", name="Reset")

        # ===== SEARCH ELEMENTS =====
        self.search_results_container = page.locator(
            ".search-results, [class*='results']"
        )
        self.search_no_results_message = page.get_by_text("No results found")
        self.search_results_count = page.locator(".results-count, [class*='count']")
        self.clear_search_button = page.get_by_role("button", name="Clear search")
        self.search_highlight = page.locator(".highlight, [class*='highlight']")

        # ===== PAGINATION ELEMENTS =====
        self.pagination_container = page.locator("ul.pagination-container")
        self.next_page_button = page.locator(
            "ul.pagination-container > li:last-child:not(.disabled)"
        )
        self.previous_page_button = page.locator(
            "ul.pagination-container > li:first-child:not(.disabled)"
        )
        self.page_number = lambda num: page.get_by_role("button", name=str(num))
        self.current_page_indicator = page.locator(".current-page, [class*='current']")
        self.total_pages_indicator = page.locator(".total-pages, [class*='total']")
        self.items_per_page_dropdown = page.locator(
            "select[name='itemsPerPage'], .items-per-page select"
        )

        # ===== BULK OPERATIONS =====
        self.select_all_checkbox = page.get_by_role("checkbox", name="Select all")
        self.jd_checkbox = lambda title: page.locator(
            f".jd-card:has-text('{title}') input[type='checkbox']"
        )
        self.selected_items_count = page.locator(".selected-count, [class*='selected']")
        self.bulk_actions_menu = page.locator(".bulk-actions, [class*='bulk']")
        self.bulk_delete_button = page.get_by_role("button", name="Delete Selected")
        self.bulk_status_update_button = page.get_by_role(
            "button", name="Update Status"
        )
        self.bulk_export_button = page.get_by_role("button", name="Export Selected")

        # Bulk operation confirmations
        self.bulk_delete_confirmation_modal = page.get_by_role("dialog")
        self.bulk_delete_confirmation_heading = page.get_by_role(
            "heading", name="Delete Selected JDs"
        )
        self.confirm_bulk_delete_button = page.get_by_role(
            "button", name="Yes, Delete All"
        )
        self.cancel_bulk_delete_button = page.get_by_role("button", name="Cancel")

        # ===== DELETE CONFIRMATION =====
        self.delete_confirmation_modal = page.get_by_role("dialog")
        self.delete_confirmation_heading = page.get_by_role("heading", name="Delete JD")
        self.delete_confirmation_message = page.get_by_text(
            "Are you sure you want to delete this JD?"
        )
        self.confirm_delete_button = page.get_by_role("button", name="Yes, Delete")
        self.cancel_delete_button = page.get_by_role("button", name="Cancel")
        
        # Single JD deletion elements
        self.delete_jd_confirmation_text = page.get_by_text("This action cannot be undone")
        self.jd_deletion_warning = page.get_by_text("This JD has associated data that will also be deleted")
        self.force_delete_checkbox = page.get_by_role("checkbox", name="I understand the consequences")
        
        # Deletion error messages
        self.deletion_failed_error = page.get_by_text("Failed to delete JD")
        self.deletion_network_error = page.get_by_text("Network error occurred during deletion")
        self.deletion_permission_error = page.get_by_text("You don't have permission to delete this JD")
        self.deletion_associated_data_error = page.get_by_text("Cannot delete JD with associated applications")

        # ===== FILE UPLOAD MODAL =====
        self.file_upload_modal = page.get_by_role("dialog")
        self.file_upload_modal_heading = page.get_by_role(
            "heading", name="Upload JD File"
        )
        self.file_drop_area = page.locator(".file-drop-area, [class*='drop-area']")
        self.browse_files_button = page.get_by_role("button", name="Browse Files")
        self.upload_progress_bar = page.locator(".progress-bar, [class*='progress']")
        self.upload_cancel_button = page.get_by_role("button", name="Cancel Upload")

        # ===== TOAST/NOTIFICATION MESSAGES =====
        self.toast_message = page.locator(
            ".toast, .alert, [class*='toast'], [class*='alert']"
        )
        self.success_toast = page.locator(
            ".toast-success, .alert-success, [class*='success']"
        )
        self.error_toast = page.locator(".toast-error, .alert-error, [class*='error']")
        self.warning_toast = page.locator(
            ".toast-warning, .alert-warning, [class*='warning']"
        )
        self.info_toast = page.locator(".toast-info, .alert-info, [class*='info']")

        # ===== LOADING STATES =====
        self.loading_spinner = page.locator(".loading, .spinner, [class*='loading']")
        self.jd_list_loading = page.locator(".jd-list-loading, [class*='list-loading']")
        self.modal_loading = page.locator(".modal-loading, [class*='modal-loading']")

        # ===== FORM VALIDATION HELPERS =====
        self.required_field_indicator = page.locator(
            ".required, [class*='required'], .mandatory"
        )
        self.form_validation_error = page.locator(
            ".error, .validation-error, [class*='error']"
        )
        self.field_error_message = page.locator(".field-error, [class*='field-error']")

        # ===== ACCESSIBILITY & RESPONSIVE =====
        self.main_content = page.locator("main, [role='main']")
        self.navigation_menu = page.locator("nav, [role='navigation']")
        self.mobile_menu_toggle = page.locator(".mobile-menu, [class*='mobile']")
        self.breadcrumb = page.locator(".breadcrumb, [class*='breadcrumb']")

        # ===== EDIT MODE SPECIFIC ELEMENTS =====
        self.edit_jd_modal_heading = page.get_by_role("heading", name="Edit JD")
        self.edit_mode_indicator = page.locator(".edit-mode, [class*='edit-mode']")
        self.unsaved_changes_warning = page.get_by_text("You have unsaved changes")
        self.discard_changes_button = page.get_by_role("button", name="Discard Changes")
        self.save_changes_button = page.get_by_role("button", name="Save Changes")

        # Edit modal form elements (same as creation but in edit context)
        self.edit_position_job_title_input = page.get_by_role(
            "textbox", name="Position Job Title"
        )
        self.edit_company_dropdown = page.locator("div").filter(has_text="Company")
        self.edit_work_style_dropdown = page.locator("div").filter(
            has_text="Work Style"
        )
        self.edit_jd_workplace_input = page.get_by_role("textbox", name="JD Workplace")
        self.edit_minimum_salary_input = page.get_by_role(
            "textbox", name="Minimum Salary"
        )
        self.edit_maximum_salary_input = page.get_by_role(
            "textbox", name="Maximum Salary"
        )

        # Edit mode navigation and URL patterns
        self.edit_jd_url_pattern = (
            "https://bprp-qa.shadhinlab.xyz/agency/{agency_id}/jd/edit/{jd_id}"
        )
        self.edit_modal_close_button = page.get_by_role("button", name="Close")

        # Pre-filled data verification elements
        self.prefilled_data_container = page.locator(
            ".prefilled-data, [class*='prefilled']"
        )
        self.form_field_value = lambda field_name: page.locator(
            f"[name='{field_name}'], #{field_name}"
        )

        # Edit confirmation and cancellation
        self.confirm_edit_button = page.get_by_role("button", name="Update")
        self.cancel_edit_button = page.get_by_role("button", name="Cancel")
        self.discard_changes_confirmation = page.get_by_text(
            "Are you sure you want to discard changes?"
        )
        self.confirm_discard_button = page.get_by_role("button", name="Yes, Discard")
        self.keep_editing_button = page.get_by_role("button", name="Keep Editing")

        # ===== JD DETAIL VIEW =====
        self.jd_detail_container = page.locator(".jd-detail, [class*='detail']")
        self.jd_detail_title = page.locator(".jd-detail-title, [class*='detail-title']")
        self.jd_detail_company = page.locator(
            ".jd-detail-company, [class*='detail-company']"
        )
        self.jd_detail_description = page.locator(
            ".jd-detail-description, [class*='description']"
        )
        self.jd_detail_requirements = page.locator(
            ".jd-detail-requirements, [class*='requirements']"
        )
        self.back_to_list_button = page.get_by_role("button", name="Back to List")

        # ===== DYNAMIC LOCATORS FOR DATA-DRIVEN TESTING =====
        def get_jd_card_by_title(self, title: str):
            """Get JD card by position title"""
            return self.page.locator(
                f".jd-card:has-text('{title}'), [data-title='{title}']"
            )

        def get_jd_card_by_company(self, company: str):
            """Get JD card by company name"""
            return self.page.locator(
                f".jd-card:has-text('{company}'), [data-company='{company}']"
            )

        def get_dropdown_option(self, option_text: str):
            """Get dropdown option by text"""
            return self.page.get_by_text(option_text, exact=True)

        def get_validation_error_by_field(self, field_name: str):
            """Get validation error for specific field"""
            return self.page.locator(
                f"[data-field='{field_name}'] .error, .{field_name}-error"
            )

        def get_filter_option(self, filter_type: str, option_value: str):
            """Get filter option by type and value"""
            return self.page.locator(
                f".{filter_type}-filter option[value='{option_value}']"
            )
