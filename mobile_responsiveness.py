from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import streamlit as st

def check_mobile_responsiveness(url, device_name='iPhone 6'):
    # Set Chrome options for incognito mode and mobile emulation
    mobile_emulation = {"deviceName": device_name}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    # Initialize WebDriver in a with-statement to ensure it closes after use
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url)
        try:
            # Example: Wait for a specific element that should be visible on mobile
            # Adjust the selector as needed for your specific responsiveness check
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
            st.write(f"The page {url} is responsive on {device_name}.")
            return True  # Indicating successful responsiveness check
        except TimeoutException:
            st.write(f"The page {url} may have responsiveness issues on {device_name}.")
            return False  # Indicating potential responsiveness issues
