import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
LOGIN_URL = "https://www.facebook.com"
print("Enter Username: ")
USERNAME = str(input())     # Or replace with your actual username
print("Enter Password: ")
PASSWORD = str(input())      # Or replace with your actual password
POST_LOGIN_TARGET_URL = "https://www.facebook.com"  # After login URL (Facebook homepage)

# Example list of profile links (replace with actual URLs you want to interact with
"""
PROFILE_LINKS = [
    "https://www.facebook.com/profile1",
    "https://www.facebook.com/profile2",
    "https://www.facebook.com/profile3"
]
"""

PROFILE_LINKS = list()
print("Enter number profiles: (Enter done to terminate)")

running = True
while running:	
	s=str(input())
	
	if s == "done":
		running = False
		break
	else:
		PROFILE_LINKS.append(s)

# Message you want to send
#MESSAGE_TEXT = "Hello, this is an automated message!"
print("Enter protocol")
MESSAGE_TEXT = str(input())

# --- Browser Options ---
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Maximize the browser window on start
chrome_options.add_experimental_option("detach", True)  # Keeps the browser open after the script finishes

def setup_driver():
    """Sets up the Selenium WebDriver for Chrome."""
    driver = None
    try:
        # Use webdriver_manager to automatically get the correct driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("WebDriver initialized successfully.")
        return driver
    except Exception as e:
        print(f"Error setting up WebDriver: {e}")
        return None

def login_to_facebook(driver, url, username, password):
    """
    Navigate to Facebook login page, fill in credentials, and submit.
    """
    print(f"Navigating to login page: {url}")
    driver.get(url)

    try:
        # Wait for email field to be visible and enter the username
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        username_field.send_keys(username)

        # Wait for password field to be visible and enter the password
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pass"))
        )
        password_field.send_keys(password)

        # Wait for login button to be clickable and click it
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "login"))
        )
        login_button.click()

        # Wait for the post-login URL to load
        WebDriverWait(driver, 10).until(
            EC.url_changes(url)
        )
        print("Login successful!")
        return True

    except TimeoutException:
        print("Login failed: Timeout waiting for elements or page to load.")
        return False
    except NoSuchElementException as e:
        print(f"Login failed: Could not find an element - {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during login: {e}")
        return False

def send_message_to_profile(driver, profile_url, message):
    """
    Navigate to a profile page and send a message.
    """
    print(f"Navigating to profile: {profile_url}")
    driver.get(profile_url)

    try:
        # Wait for the message box to be available
        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Write a message..."]'))
        )
        message_box.click()

        # Type the message in the input field
        message_box = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Write a message..."]')
        message_box.send_keys(message)

        # Press Enter to send the message
        message_box.send_keys(Keys.RETURN)

        print(f"Message sent to {profile_url}")

    except TimeoutException:
        print(f"Error: Message box not found on {profile_url}")
    except NoSuchElementException as e:
        print(f"Error: Could not interact with message box on {profile_url} - {e}")
    except Exception as e:
        print(f"An unexpected error occurred while sending message to {profile_url}: {e}")

def main():
    driver = None
    try:
        driver = setup_driver()
        if not driver:
            print("Driver setup failed. Exiting.")
            return

        if login_to_facebook(driver, LOGIN_URL, USERNAME, PASSWORD):
            print("\nSuccessfully logged in. Automating message sending...")
            
            # Iterate through the profile links and send messages
            for profile_link in PROFILE_LINKS:
                send_message_to_profile(driver, profile_link, MESSAGE_TEXT)
                time.sleep(3)  # Add a short delay between requests/messages to avoid rate limiting

        else:
            print("\nLogin failed. Browser will remain open for inspection.")

    except Exception as e:
        print(f"An unhandled error occurred: {e}")
    finally:
        print("Script finished. Browser session remains active.")
        pass  # Browser remains open

if __name__ == "__main__":
    main()
