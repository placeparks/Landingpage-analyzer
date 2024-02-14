from selenium import webdriver
from selenium_stealth import stealth
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options
import time
import requests

client_id = "f9c070d7ce82119"
def upload_to_imgur(image_path):
    headers = {"Authorization": f"Client-ID {client_id}"}
    try:
        with open(image_path, "rb") as image:
            data = {"image": image.read()}
            response = requests.post("https://api.imgur.com/3/upload", headers=headers, files=data)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
            return response.json()['data']['link']
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP error response
        print(response.json())
    except Exception as err:
        print(f"Other error occurred: {err}")  # Other errors
    return None




def capture_web_page_image(url, file_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=chrome_options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    
    driver.get(url)
    time.sleep(4)  # Wait for the page to load

    # Specify the full file path with the .png extension
    screenshot_path = file_path if file_path.endswith('.png') else file_path + '.png'
    driver.save_screenshot(screenshot_path)
    driver.quit()
    return screenshot_path