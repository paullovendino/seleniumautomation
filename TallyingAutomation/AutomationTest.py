import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# service = Service(executable_path="C:\\browserdrivers\\chromedriver-win64\\chromedriver.exe")
# driver = webdriver.Chrome(service=service)
# driver.get("https://be.myadminmatrix.com/")
# driver.maximize_window()
# print("Current tab URL:", driver.current_url)
# time.sleep(2)
#
# driver.execute_script("window.open('');")
# driver.switch_to.window(driver.window_handles[-1])
# driver.get("https://docs.google.com/spreadsheets/d/1cFhayE3yAzLfUps2LN-dM_cm8KU8VSsoYNwgAUt2514/edit?pli=1&gid=2054119203#gid=2054119203")
# print("Current tab URL:", driver.current_url)
# time.sleep(2)
#
# #back to dashboard
# driver.switch_to.window(driver.window_handles[0])
# print("Current tab URL:", driver.current_url)
#
# #input credentials on the login page
# username_field = driver.find_element(By.NAME, "username")
# username_field.clear()
# username_field.send_keys("rjaysan")
#
# password_field = driver.find_element(By.NAME, "password")
# password_field.clear()
# password_field.send_keys("rjaysan")
#
# # Wait until captcha input is present
# wait = WebDriverWait(driver, 10)
#
# captcha_input = wait.until(EC.presence_of_element_located((By.NAME, "captcha")))
# driver.execute_script("arguments[0].focus();", captcha_input)
# print("Please Enter the captcha within 10 seconds")
#
# wait.until(lambda d: len(d.find_element(By.NAME, "captcha").get_attribute("value")) == 5)
# print("Captcha detected with 5 characters. Proceeding to login...")
#
# #proceed to login
# login_button = driver.find_element(By.XPATH, "//button[contains(text(),'Login')]")
# login_button.click()
#
# report_element = driver.find_element(By.XPATH, "//span[text()='0. Report']")
# report_element.click()
#
# plprovider_element = driver.find_element(By.XPATH, "//span[text()='0.1. P&L Provider']")
# plprovider_element.click()
#
# time.sleep(3)
# search_button = wait.until(EC.element_to_be_clickable((By.ID, "reportProviderSearch")))
# search_button.click()
#
# time.sleep(10)

def main(username, password):
    service = Service(executable_path="C:\\browserdrivers\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://be.myadminmatrix.com/")
    driver.maximize_window()
    print("Current tab URL:", driver.current_url)
    time.sleep(2)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(
        "https://docs.google.com/spreadsheets/d/1cFhayE3yAzLfUps2LN-dM_cm8KU8VSsoYNwgAUt2514/edit?pli=1&gid=2054119203#gid=2054119203")
    print("Current tab URL:", driver.current_url)
    time.sleep(2)

    # back to dashboard
    driver.switch_to.window(driver.window_handles[0])
    print("Current tab URL:", driver.current_url)

    wait = WebDriverWait(driver, 10)

    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username_field.clear()
    username_field.send_keys(username)

    password_field = driver.find_element(By.NAME, "password")
    password_field.clear()
    password_field.send_keys(password)

    # Wait for captcha input and focus it
    captcha_value = input("Please enter the CAPTCHA displayed on the website: ")

    # Wait until captcha input is present
    captcha_input = wait.until(EC.presence_of_element_located((By.NAME, "captcha")))

    # Fill the captcha input field with the CLI input
    captcha_input.clear()
    captcha_input.send_keys(captcha_value)
    print("Captcha entered. Proceeding to login...")

    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    time.sleep(5)

    report_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='0. Report']")))
    report_element.click()

    plprovider_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='0.1. P&L Provider']")))
    plprovider_element.click()
    time.sleep(5)

    search_button = wait.until(EC.element_to_be_clickable((By.ID, "reportProviderSearch")))
    search_button.click()

    time.sleep(30)
    # driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Login script with Selenium")
    parser.add_argument("-u", "--username", required=True, help="Username for login")
    parser.add_argument("-p", "--password", required=True, help="Password for login")
    args = parser.parse_args()

    main(args.username, args.password)