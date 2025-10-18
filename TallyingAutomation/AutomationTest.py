import argparse
import requests
import gspread
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from oauth2client.service_account import ServiceAccountCredentials

def get_api_report(start_date, end_date, provider_code):
    url = "http://mcs-report-api-prod-new-2b387e6dd14323e0.elb.ap-southeast-1.amazonaws.com/v1/report/summary-games"

    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "branchCode": [0],
        "providerCode": provider_code,
        "currency": "IDR"
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("API response received successfully.")
        return response.json()
    else:
        print(f"Failed to get data from API. Status Code: {response.status_code}")
        return None

def calculate_total_winlose(data):
    total_winlose = 0
    for game in data:
        total_winlose += game.get("bet_winlose", 0)
    return total_winlose

def input_to_excel(provider, seamless_winlose, provider_winlose):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "C:\\Users\\IT Admin\\PycharmProjects\\SeleniumProject1\\TallyingAutomation\\totemic-inquiry-444608-h9-6e69350e81b0.json",
        scope
    )

    client = gspread.authorize(creds)

    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1ISkTD5gnaPszTakCcQmLAVD9BU3m8sUqlONECcOsAjE/edit?pli=1&hl=fil&gid=2054119203#gid=2054119203"
    )

    worksheet = sheet.worksheet(f"{provider} SEAMLESS")

    worksheet.update(range_name='D21', values=[[str(seamless_winlose)]])
    print("DONE UPDATING SEAMLESS WINLOSE")

    worksheet.update(range_name='O21', values=[[str(provider_winlose)]])
    print("DONE UPDATING PROVIDER WINLOSE")

def get_provider_winlose():
    service = Service(executable_path="C:\\browserdrivers\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get("https://agent.jav8889.com/#/login?redirect=%2FWelCome")
    print("Current tab URL:", driver.current_url)

    wait = WebDriverWait(driver, 10)

    language_icon_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'el-dropdown-link')]")))
    language_icon_span.click()

    english_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'English')]")))
    english_option.click()

    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username_field.clear()
    username_field.send_keys("MPOPLAYIDRK3")

    password_field = driver.find_element(By.NAME, "password")
    password_field.clear()
    password_field.send_keys("MpoTech7788")

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span='Login']")))
    login_button.click()

    navigation_bar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.el-submenu__title")))
    navigation_bar.click()

    report_section = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[span[text()='Report']]")))
    report_section.click()

    date_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='开始日期']")))
    date_input.click()

    all_dates = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.available span")))

    for start_date in all_dates:
        if start_date.text == "17":
            start_date.click()
            break

    for end_date in all_dates:
        if end_date.text == "17":
            end_date.click()
            break

    ok_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.el-button.el-picker-panel__link-btn.el-button--default.el-button--mini.is-plain")))
    ok_button.click()

    search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.btn button.el-button.el-button--primary span")))
    search_button.click()

    time.sleep(3)

    net_win_value = wait.until(EC.presence_of_element_located((By.XPATH, "//tr[contains(@class, 'el-table__row')]/td[8]//div[@class='cell']")))
    print("HCG Net Win:", net_win_value.text)

    return net_win_value.text

def main(provider):
    start_date = input("Input startDate (YYYY-MM-DD): ")
    end_date = input("Input endDate (YYYY-MM-DD): ")

    print(f"\nMaking API call for provider: {provider} from {start_date} to {end_date}...")
    api_data = get_api_report(start_date, end_date, provider)

    if api_data and api_data.get("success"):
        games_data = api_data.get("data", [])
        seamless_winlose = calculate_total_winlose(games_data)
        print(f"Total Win/Lose amount: {seamless_winlose}")

        provider_winlose = get_provider_winlose()
        input_to_excel(provider, seamless_winlose, provider_winlose)
    else:
        print("No data found or API call failed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch win/lose data from the API.")
    parser.add_argument("--provider", required=True, help="Provider code (e.g., 'hcg', 'provider_code')")
    args = parser.parse_args()

    main(args.provider)