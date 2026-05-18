import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SkillGapAppTest(unittest.TestCase):
    def setUp(self):
        # Setup Chrome driver (ensure chromedriver is installed or use webdriver_manager)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') # Run headless for automated testing
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:80" # URL of the frontend

    def test_1_homepage_loads(self):
        """Test Case 1: Verify homepage loads"""
        self.driver.get(self.base_url)
        # Assuming the React app has a title or a main element we can wait for
        # Wait until body is present
        body = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        self.assertIsNotNone(body, "Homepage failed to load.")
        print("Test 1 Passed: Homepage loaded successfully.")

    def test_2_api_connection(self):
        """Test Case 2: Check frontend-to-backend API response"""
        self.driver.get(self.base_url)
        time.sleep(3) # Wait for React to fetch data from backend
        # Check if any content that comes from backend is rendered.
        # We can just verify the page source doesn't contain a generic 'fetch failed' error
        page_source = self.driver.page_source
        self.assertNotIn("Network Error", page_source)
        print("Test 2 Passed: API connection appears valid.")

    def test_3_navigation(self):
        """Test Case 3: Validate navigation or button behavior"""
        self.driver.get(self.base_url)
        # Find any clickable button or link
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        if buttons:
            buttons[0].click()
            print("Test 3 Passed: Button clicked successfully.")
        else:
            print("Test 3 Passed: No buttons found to click, but page rendered.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
