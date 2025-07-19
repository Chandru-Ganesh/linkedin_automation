import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException


LINKEDIN_USERNAME = "jayampt75@gmail.com"
LINKEDIN_PASSWORD = "jayampt75@password.com"
TARGET_PROFILE_URL = "https://www.linkedin.com/in/monica-r-52645029a/"
CUSTOM_MESSAGE = "Hi! I'd like to connect with you regarding a professional opportunity. 😊"


def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return uc.Chrome(options=options)

def safe_click(driver, element, description="element"):
    """Safely click an element with multiple methods"""
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(1)
        
        driver.execute_script("arguments[0].style.border='3px solid red'", element)
        time.sleep(0.5)
        
        element.click()
        print(f"[✓] Successfully clicked {description}")
        return True
    except ElementNotInteractableException:
        try:
            driver.execute_script("arguments[0].click();", element)
            print(f"[✓] Successfully clicked {description} with JavaScript")
            return True
        except Exception as e:
            print(f"[!] Failed to click {description}: {e}")
            return False

def login(driver):
    print("[1/6] 🔑 Logging into LinkedIn...")
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)

    try:
        # Enter username
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.clear()
        username_field.send_keys(LINKEDIN_USERNAME)
        
        # Enter password
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(LINKEDIN_PASSWORD)
        
        # Click login
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        safe_click(driver, login_button, "login button")
        
        print("[✓] Login completed - waiting for page load...")
        time.sleep(5)
        
        WebDriverWait(driver, 10).until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, '//div[@id="global-nav"]')),
                EC.presence_of_element_located((By.XPATH, '//nav[@aria-label="Primary Navigation"]'))
            )
        )
        print("[✓] Successfully logged in!")
        return True
        
    except Exception as e:
        print(f"[✗] Login failed: {e}")
        return False

def visit_profile(driver):
    print(f"[2/6] 👤 Visiting target profile: {TARGET_PROFILE_URL}")
    driver.get(TARGET_PROFILE_URL)
    time.sleep(5)
    
    try:
        WebDriverWait(driver, 15).until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, '//h1[contains(@class,"text-heading-xlarge")]')),
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"pv-text-details__left-panel")]'))
            )
        )
        print("[✓] Profile loaded successfully")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
    except TimeoutException:
        print("[!] Profile may not have loaded completely, but proceeding...")

def is_in_main_profile_area(driver, element):
    """Check if element is in the main profile area, not in recommendations"""
    try:
        location = driver.execute_script("return arguments[0].getBoundingClientRect();", element)
        
        window_width = driver.execute_script("return window.innerWidth;")
        main_area_boundary = window_width * 0.7
        
        if location['left'] > main_area_boundary:
            print(f"[DEBUG] Element at position {location['left']} is in RIGHT SIDE (likely recommendations)")
            return False
            
        try:
            element.find_element(By.XPATH, "./ancestor::*[contains(@class,'aside') or contains(@class,'people-also-viewed') or contains(@class,'recommendations') or contains(@class,'people-you-may-know')]")
            print("[DEBUG] Element found in recommendations section")
            return False
        except NoSuchElementException:
            pass
            
        try:
            element.find_element(By.XPATH, "./ancestor::*[contains(@class,'pv-top-card') or contains(@class,'profile-header') or contains(@class,'pv-profile-section')]")
            print("[DEBUG] Element confirmed in main profile area")
            return True
        except NoSuchElementException:
            pass
            
        print(f"[DEBUG] Element at position {location['left']} is in LEFT SIDE (main profile area)")
        return True
        
    except Exception as e:
        print(f"[DEBUG] Error checking element position: {e}")
        return True  

def find_direct_connect_button(driver):
    """Look for Connect button directly visible in main profile area"""
    print("[→] Searching for direct Connect button in main profile...")
    
    main_profile_connect_selectors = [
        '//main//section[contains(@class,"pv-top-card")]//button[contains(text(),"Connect")]',
        '//div[contains(@class,"pv-top-card-v2-ctas")]//button[contains(text(),"Connect")]',
        '//div[contains(@class,"pv-top-card")]//button[contains(@aria-label,"Invite") and contains(text(),"Connect")]',
        '//section[contains(@class,"artdeco-card") and contains(@class,"pv-top-card")]//button[contains(text(),"Connect")]',
        '//div[contains(@class,"profile-header")]//button[contains(text(),"Connect")]',       
        '//main//div[contains(@class,"ph5")]//button[contains(text(),"Connect")]', 
        '//button[contains(text(),"Connect") and not(ancestor::aside)]',
    ]
    
    for i, selector in enumerate(main_profile_connect_selectors):
        print(f"[→] Trying selector {i+1}: Looking for direct Connect button...")
        try:
            connect_buttons = driver.find_elements(By.XPATH, selector)
            
            for btn in connect_buttons:
                if is_in_main_profile_area(driver, btn):
                    print(f"[✓] Found valid Connect button in main profile area!")
                    if safe_click(driver, btn, f"Direct Connect button (selector {i+1})"):
                        return True
                else:
                    print(f"[!] Connect button found but in wrong area (recommendations)")
                    
        except Exception as e:
            print(f"[!] Selector {i+1} failed: {e}")
            continue
    
    return False

def find_more_button_and_connect(driver):
    """Look for More button in main profile and find Connect in dropdown"""
    print("[→] Connect not found directly, searching in 'More' dropdown...")
    
    more_button_selectors = [
        '//main//section[contains(@class,"pv-top-card")]//button[contains(@aria-label,"More actions")]',
        '//div[contains(@class,"pv-top-card-v2-ctas")]//button[contains(text(),"More")]',
        '//div[contains(@class,"pv-top-card")]//button[contains(@aria-label,"More actions")]',
        
        '//main//button[@data-control-name="overflow_menu"]',
        '//section[contains(@class,"pv-top-card")]//button[contains(@class,"artdeco-dropdown__trigger")]',
        '//main//button[contains(@class,"artdeco-button--tertiary") and contains(@aria-label,"More")]',
        
        '//main//button[contains(text(),"Resources")]',
        '//div[contains(@class,"pv-top-card")]//button[contains(text(),"Resources")]',
    ]
    
    for i, more_selector in enumerate(more_button_selectors):
        print(f"[→] Trying More button selector {i+1}...")
        try:
            more_buttons = driver.find_elements(By.XPATH, more_selector)
            
            for more_btn in more_buttons:
                if is_in_main_profile_area(driver, more_btn):
                    print(f"[✓] Found More button in main profile area!")
                    
                    if safe_click(driver, more_btn, f"More button (selector {i+1})"):
                        time.sleep(2)
                        
                        dropdown_connect_selectors = [
                            '//div[contains(@class,"artdeco-dropdown__content")]//button[contains(text(),"Connect")]',
                            '//div[contains(@class,"artdeco-dropdown__content")]//span[text()="Connect"]/parent::*',
                            '//div[@role="menu"]//button[contains(text(),"Connect")]',
                            '//ul[@role="menu"]//span[text()="Connect"]/parent::*',
                            '//div[contains(@class,"overflow-menu")]//button[contains(text(),"Connect")]',
                            
                            '//li//button[contains(text(),"Connect")]',
                            '//div[contains(@class,"dropdown")]//button[contains(text(),"Connect")]',
                        ]
                        
                        for j, dropdown_selector in enumerate(dropdown_connect_selectors):
                            print(f"[→] Looking for Connect in dropdown (pattern {j+1})...")
                            try:
                                connect_dropdown = WebDriverWait(driver, 3).until(
                                    EC.element_to_be_clickable((By.XPATH, dropdown_selector))
                                )
                                
                                if safe_click(driver, connect_dropdown, f"Connect from dropdown (pattern {j+1})"):
                                    print("[✓] Successfully clicked Connect from More dropdown!")
                                    return True
                                    
                            except (NoSuchElementException, TimeoutException):
                                continue
                        
                        print("[!] Connect not found in dropdown, closing dropdown")
                        driver.execute_script("document.body.click();")
                        time.sleep(1)
                else:
                    print(f"[!] More button found but in wrong area (recommendations)")
                    
        except Exception as e:
            print(f"[!] More button selector {i+1} failed: {e}")
            continue
    
    return False

def find_and_click_connect(driver):
    print("[3/6] 🔍 Looking for Connect button in main profile...")
    
    if find_direct_connect_button(driver):
        return True
    
    if find_more_button_and_connect(driver):
        return True
    
    print("[→] Final attempt: Scrolling to profile top and retrying...")
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)
    
    if find_direct_connect_button(driver):
        return True
    
    print("[✗] Connect button not found in main profile area")
    return False

def handle_connection_dialog(driver):
    print("[4/6] 💬 Waiting for connection dialog...")
    
    try:

        dialog_selectors = [
            '//div[contains(@class,"send-invite")]',
            '//div[@role="dialog"]',
            '//div[contains(@class,"artdeco-modal")]',
            '//div[contains(@class,"invitation-modal")]',
            '//div[contains(@id,"modal")]'
        ]
        
        dialog_found = False
        for selector in dialog_selectors:
            try:
                WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                print("[✓] Connection dialog appeared")
                dialog_found = True
                break
            except TimeoutException:
                continue
        
        if not dialog_found:
            print("[!] Connection dialog not found, trying to send without note")
            return send_connection_without_note(driver)
        
        time.sleep(2)
        
        note_selectors = [
            '//button[contains(text(),"Add a note")]',
            '//button[contains(@aria-label,"Add a note")]',
            '//span[text()="Add a note"]/parent::button',
            '//button[contains(@class,"artdeco-button--secondary") and contains(text(),"Add a note")]'
        ]
        
        note_button_found = False
        for selector in note_selectors:
            try:
                note_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                if safe_click(driver, note_btn, "Add a note button"):
                    note_button_found = True
                    print("[✓] Add a note button clicked")
                    break
            except (NoSuchElementException, TimeoutException):
                continue
        
        if not note_button_found:
            print("[!] Add note button not found, sending without note")
            return send_connection_without_note(driver)
        
        time.sleep(3)
        
        message_selectors = [
            '//textarea[@id="custom-message"]',
            '//textarea[@name="message"]',
            '//textarea[contains(@id,"custom")]',
            '//textarea[contains(@placeholder,"message")]',
            '//textarea[contains(@class,"connect-request")]',
            '//textarea'  
        ]
        
        message_added = False
        for selector in message_selectors:
            try:
                textarea = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                
                textarea.clear()
                time.sleep(1)
                textarea.send_keys(CUSTOM_MESSAGE)
                print(f"[✓] Added custom message: '{CUSTOM_MESSAGE}'")
                message_added = True
                break
            except (NoSuchElementException, TimeoutException):
                continue
        
        if not message_added:
            print("[!] Could not find message textarea")
        
        time.sleep(2)
        return send_invitation(driver)
        
    except Exception as e:
        print(f"[!] Error handling dialog: {e}")
        return False

def send_invitation(driver):
    print("[5/6] 📤 Sending connection invitation...")
    
    send_selectors = [
        '//button[@aria-label="Send now"]',
        '//button[contains(text(),"Send invitation")]',
        '//button[contains(text(),"Send") and not(contains(text(),"without"))]',
        '//span[text()="Send"]/parent::button',
        '//button[contains(@class,"artdeco-button--primary")]//span[text()="Send"]/parent::button'
    ]
    
    for selector in send_selectors:
        try:
            send_btn = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            if safe_click(driver, send_btn, "Send invitation button"):
                print("[✅] Connection request sent successfully with custom note!")
                time.sleep(3)
                return True
        except (NoSuchElementException, TimeoutException):
            continue
    
    print("[!] Could not find Send button")
    return False

def send_connection_without_note(driver):
    print("[4/6] 📤 Sending connection without note...")
    
    send_selectors = [
        '//button[contains(text(),"Send without a note")]',
        '//button[@aria-label="Send without a note"]',
        '//button[contains(text(),"Send now")]',
        '//button[contains(text(),"Send")]'
    ]
    
    for selector in send_selectors:
        try:
            send_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            if safe_click(driver, send_btn, "Send without note button"):
                print("[✅] Connection request sent without note!")
                return True
        except (NoSuchElementException, TimeoutException):
            continue
    
    print("[!] Could not send connection request")
    return False

def follow_user(driver):
    print("[6/6] 👥 Attempting to follow user...")
    time.sleep(3)
    
    follow_selectors = [
        '//main//button[contains(text(),"Follow")]',
        '//div[contains(@class,"pv-top-card")]//button[contains(text(),"Follow")]',
        '//button[@aria-label="Follow"]',
        '//span[text()="Follow"]/parent::button'
    ]
    
    for selector in follow_selectors:
        try:
            follow_buttons = driver.find_elements(By.XPATH, selector)
            
            for follow_btn in follow_buttons:
                if is_in_main_profile_area(driver, follow_btn):
                    if safe_click(driver, follow_btn, "Follow button"):
                        print("[✅] Successfully followed user")
                        return True
        except Exception as e:
            continue
    
    print("[!] Follow button not found (might already be following)")
    return False

def main():
    driver = None
    try:
        print("🚀 STARTING LINKEDIN CONNECT AUTOMATION")
        print("=" * 60)
        print("🎯 Target Profile:", TARGET_PROFILE_URL)
        print("📝 Custom Message:", CUSTOM_MESSAGE)
        print("=" * 60)
        
        driver = setup_driver()
        if not login(driver):
            print("[❌] Login failed - stopping automation")
            return
        
        visit_profile(driver)
        
        connect_success = find_and_click_connect(driver)
        
        if connect_success:
            dialog_success = handle_connection_dialog(driver)
            if not dialog_success:
                print("[⚠️] Connection dialog handling failed")
        else:
            print("[⚠️] Connect button not found, skipping to follow")
        
        follow_user(driver)
        
        print("\n" + "=" * 60)
        print("🏁 AUTOMATION COMPLETED!")
        print("=" * 60)
        time.sleep(3)
        
    except Exception as e:
        print(f"[💥] CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            print("\n[🔧] Closing browser...")
            try:
                driver.save_screenshot("linkedin_automation_final_state.png")
                print("[📸] Screenshot saved: linkedin_automation_final_state.png")
                
                time.sleep(2)
                driver.quit()
                print("[✓] Browser closed successfully")
            except:
                pass
        
        print("\n🎉 AUTOMATION FINISHED!")

if __name__ == "__main__":
    main()