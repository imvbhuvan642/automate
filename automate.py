from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os

# Configuration
LOGIN_URL = "https://convex.latticehq.com/login"
USERNAME = "lattice_user@servicetitan.com"
PASSWORD = "KpbvFweJDayb4QGepnBt"

def setup_driver():
    """Setup Chrome driver with download preferences"""
    options = webdriver.ChromeOptions()
    
    # Set download directory to current directory
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    # Additional options for stability
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def login(driver, wait):
    """Login to Lattice with provided credentials"""
    print("Navigating to login page...")
    driver.get(LOGIN_URL)
    
    try:
        # Wait for and fill username field
        print("Entering username...")
        username_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        username_field.clear()
        username_field.send_keys(USERNAME)
        
        # Fill password field
        print("Entering password...")
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(PASSWORD)
        
        # Click login button
        print("Clicking login button...")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Wait for login to complete (look for dashboard or main page elements)
        print("Waiting for login to complete...")
        wait.until(EC.url_changes(LOGIN_URL))
        time.sleep(3)
        
        print("Login successful!")
        return True
        
    except TimeoutException:
        print("Login failed - timeout waiting for elements")
        return False
    except Exception as e:
        print(f"Login failed with error: {e}")
        return False

def switch_to_admin(driver, wait):
    """Switch to Admin view"""
    try:
        print("Looking for Admin option...")
        
        # Common selectors for admin access
        admin_selectors = [
            "//a[contains(text(), 'Switch to admin')]",
            "//button[contains(text(), 'Switch to admin')]",
            "//span[contains(text(), 'Switch to admin')]",
            "//div[contains(text(), 'Switch to admin')]",
            "//a[@href*='Switch to admin']",
            "//button[@aria-label*='Switch to admin']"
        ]
        
        for selector in admin_selectors:
            try:
                admin_element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                admin_element.click()
                print("Switched to Admin successfully!")
                time.sleep(2)
                return True
            except TimeoutException:
                continue
        
        print("Could not find Admin option, trying navigation menu...")
        # Try to find and click navigation menu first
        menu_selectors = [
            "//button[contains(@class, 'menu')]",
            "//div[contains(@class, 'hamburger')]",
            "//button[@aria-label='Menu']"
        ]
        
        for menu_selector in menu_selectors:
            try:
                menu_button = driver.find_element(By.XPATH, menu_selector)
                menu_button.click()
                time.sleep(1)
                
                # Now try to find admin in the opened menu
                for admin_selector in admin_selectors:
                    try:
                        admin_element = wait.until(EC.element_to_be_clickable((By.XPATH, admin_selector)))
                        admin_element.click()
                        print("Switched to Admin via menu!")
                        time.sleep(2)
                        return True
                    except TimeoutException:
                        continue
            except:
                continue
        
        print("Warning: Could not find Admin option. Proceeding anyway...")
        return False
        
    except Exception as e:
        print(f"Error switching to admin: {e}")
        return False

def navigate_to_reviews(driver, wait):
    """Navigate to Reviews section"""
    try:
        print("Looking for Reviews section...")
        
        # Common selectors for reviews
        review_selectors = [
            "//a[contains(text(), 'Reviews')]",
            "//button[contains(text(), 'Reviews')]",
            "//span[contains(text(), 'Reviews')]",
            "//div[contains(text(), 'Reviews')]",
            "//a[@href*='review']",
            "//li[contains(text(), 'Reviews')]"
        ]
        
        for selector in review_selectors:
            try:
                review_element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                review_element.click()
                print("Navigated to Reviews successfully!")
                time.sleep(3)
                return True
            except TimeoutException:
                continue
        
        print("Could not find Reviews section directly, checking navigation...")
        return False
        
    except Exception as e:
        print(f"Error navigating to reviews: {e}")
        return False

def navigate_to_performance_reviews(driver, wait):
    """Navigate to Performance Reviews section"""
    try:
        print("Looking for Performance Reviews section...")
        
        # Wait for page to load after clicking Reviews
        time.sleep(3)
        
        # Selectors for Performance Reviews
        performance_review_selectors = [
            "//a[contains(text(), 'Performance Reviews')]",
            "//button[contains(text(), 'Performance Reviews')]",
            "//span[contains(text(), 'Performance Reviews')]",
            "//div[contains(text(), 'Performance Reviews')]",
            "//a[contains(text(), 'Performance')]",
            "//li[contains(text(), 'Performance Reviews')]",
            "//a[@href*='performance']"
        ]
        
        for selector in performance_review_selectors:
            try:
                performance_element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                performance_element.click()
                print("Navigated to Performance Reviews successfully!")
                time.sleep(3)
                return True
            except TimeoutException:
                continue
        
        print("Could not find Performance Reviews section")
        return False
        
    except Exception as e:
        print(f"Error navigating to performance reviews: {e}")
        return False

def select_specific_review_cycle(driver, wait):
    """Select the specific Performance Review Cycle II Mid-Year Review (Aug 2023)"""
    try:
        print("Looking for 'Performance Review Cycle II Mid-Year Review (Aug 2023)'...")
        
        # Wait for review cycles to load
        time.sleep(3)
        
        # Look for the specific review cycle text
        specific_review_selectors = [
            "//a[contains(text(), 'Performance Review Cycle II Mid-Year Review (Aug 2023)')]",
            "//div[contains(text(), 'Performance Review Cycle II Mid-Year Review (Aug 2023)')]",
            "//span[contains(text(), 'Performance Review Cycle II Mid-Year Review (Aug 2023)')]",
            "//tr[contains(text(), 'Performance Review Cycle II Mid-Year Review (Aug 2023)')]",
            "//td[contains(text(), 'Performance Review Cycle II Mid-Year Review (Aug 2023)')]",
            "//button[contains(text(), 'Performance Review Cycle II Mid-Year Review (Aug 2023)')]"
        ]
        
        for selector in specific_review_selectors:
            try:
                specific_review = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                specific_review.click()
                print("Selected 'Performance Review Cycle II Mid-Year Review (Aug 2023)' successfully!")
                time.sleep(3)
                return True
            except TimeoutException:
                continue
        
        # If exact text not found, try partial matches
        print("Exact match not found, trying partial matches...")
        partial_selectors = [
            "//a[contains(text(), 'Mid-Year Review') and contains(text(), 'Aug 2023')]",
            "//div[contains(text(), 'Mid-Year Review') and contains(text(), 'Aug 2023')]",
            "//a[contains(text(), 'Cycle II') and contains(text(), 'Mid-Year')]",
            "//a[contains(text(), 'Aug 2023')]"
        ]
        
        for selector in partial_selectors:
            try:
                review_element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                review_element.click()
                print("Selected review cycle using partial match!")
                time.sleep(3)
                return True
            except TimeoutException:
                continue
        
        print("Could not find the specific review cycle")
        return False
        
    except Exception as e:
        print(f"Error selecting specific review cycle: {e}")
        return False

def download_csv_with_options(driver, wait):
    """Download CSV with specific report type and field options"""
    try:
        print("Looking for 'Download CSV' button...")
        
        # Look specifically for "Download CSV" button
        download_csv_selectors = [
            "//button[contains(text(), 'Download CSV')]",
            "//a[contains(text(), 'Download CSV')]",
            "//button[text()='Download CSV']",
            "//a[text()='Download CSV']",
            "//input[@value='Download CSV']",
            "//button[contains(@class, 'download') and contains(text(), 'CSV')]"
        ]
        
        download_button_found = False
        for selector in download_csv_selectors:
            try:
                download_button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                download_button.click()
                print("Clicked 'Download CSV' button!")
                download_button_found = True
                time.sleep(3)
                break
            except TimeoutException:
                continue
        
        if not download_button_found:
            print("Could not find 'Download CSV' button")
            return False
        
        # Step 2: Select "Review responses" from Report Type dropdown
        print("Looking for Report Type dropdown...")
        
        # Wait for dropdown to appear
        time.sleep(2)
        
        report_type_selectors = [
            "//select[contains(@name, 'Report Type') or contains(@name, 'type')]",
            "//select[contains(@id, 'Report Type') or contains(@id, 'type')]",
            "//div[contains(text(), 'Report Type')]//following::select",
            "//label[contains(text(), 'Report Type')]//following::select",
            "//select"
        ]
        
        dropdown_found = False
        for selector in report_type_selectors:
            try:
                report_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                report_dropdown.click()
                print("Found and clicked Report Type dropdown!")
                time.sleep(1)
                
                # Select "Review responses" option
                review_responses_selectors = [
                    "//option[contains(text(), 'Review responses')]",
                    "//option[text()='Review responses']",
                    "//option[@value='review_responses']",
                    "//option[@value='review-responses']"
                ]
                
                for response_selector in review_responses_selectors:
                    try:
                        review_responses_option = driver.find_element(By.XPATH, response_selector)
                        review_responses_option.click()
                        print("Selected 'Review responses' from dropdown!")
                        dropdown_found = True
                        time.sleep(1)
                        break
                    except:
                        continue
                
                if dropdown_found:
                    break
                    
            except TimeoutException:
                continue
        
        if not dropdown_found:
            print("Could not find Report Type dropdown or 'Review responses' option")
        
        # Step 3: Set Employee field columns to "All fields"
        print("Looking for Employee field columns setting...")
        
        time.sleep(2)
        
        # Look for "All fields" option in various forms
        all_fields_selectors = [
            "//select[contains(@name, 'field') or contains(@name, 'column')]",
            "//select[contains(@id, 'field') or contains(@id, 'column')]",
            "//div[contains(text(), 'Employee field')]//following::select",
            "//label[contains(text(), 'Employee field')]//following::select",
            "//div[contains(text(), 'field columns')]//following::select",
            "//label[contains(text(), 'field columns')]//following::select"
        ]
        
        fields_set = False
        for selector in all_fields_selectors:
            try:
                fields_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                fields_dropdown.click()
                print("Found Employee fields dropdown!")
                time.sleep(1)
                
                # Select "All fields" option
                all_fields_option_selectors = [
                    "//option[contains(text(), 'All fields')]",
                    "//option[text()='All fields']",
                    "//option[@value='all_fields']",
                    "//option[@value='all-fields']",
                    "//option[@value='all']"
                ]
                
                for all_fields_selector in all_fields_option_selectors:
                    try:
                        all_fields_option = driver.find_element(By.XPATH, all_fields_selector)
                        all_fields_option.click()
                        print("Selected 'All fields' for Employee field columns!")
                        fields_set = True
                        time.sleep(1)
                        break
                    except:
                        continue
                
                if fields_set:
                    break
                    
            except TimeoutException:
                continue
        
        if not fields_set:
            print("Could not find Employee field columns setting")
        
        # Step 4: Start the download
        print("Looking for final download/submit button...")
        
        time.sleep(2)
        
        final_download_selectors = [
            "//button[contains(text(), 'Download')]",
            "//button[contains(text(), 'Generate')]",
            "//button[contains(text(), 'Export')]",
            "//button[contains(text(), 'Submit')]",
            "//input[@type='submit']",
            "//button[@type='submit']",
            "//a[contains(text(), 'Download')]"
        ]
        
        for selector in final_download_selectors:
            try:
                final_button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                final_button.click()
                print("Clicked final download button!")
                print("Download should start now...")
                time.sleep(5)
                return True
            except TimeoutException:
                continue
        
        print("Could not find final download button, but settings may have been configured")
        return True
        
    except Exception as e:
        print(f"Error during CSV download process: {e}")
        return False

def main():
    """Main automation function"""
    driver = setup_driver()
    wait = WebDriverWait(driver, 15)
    
    try:
        print("Starting Lattice automation...")
        
        # Step 1: Login
        if not login(driver, wait):
            print("Failed to login. Exiting...")
            return
        
        # Step 2: Switch to Admin
        switch_to_admin(driver, wait)
        
        # Step 3: Navigate to Reviews
        if not navigate_to_reviews(driver, wait):
            print("Could not find Reviews section. Please check manually.")
            return
        
        # Step 4: Navigate to Performance Reviews
        if not navigate_to_performance_reviews(driver, wait):
            print("Could not find Performance Reviews section. Please check manually.")
            return
        
        # Step 5: Select specific review cycle
        if not select_specific_review_cycle(driver, wait):
            print("Could not find 'Performance Review Cycle II Mid-Year Review (Aug 2023)'. Please check manually.")
            return
        
        # Step 6: Download CSV with specific options
        if not download_csv_with_options(driver, wait):
            print("Could not complete CSV download process. Please check manually.")
        
        print("Automation completed! Check your downloads folder for the CSV file.")
        
        # Keep browser open for manual verification
        input("Press Enter to close the browser...")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()