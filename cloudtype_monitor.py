import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def start_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-software-rasterizer")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def main():
    CLOUDTYPE_URL = "https://app.cloudtype.io/@unclebob/unclebob:main"
    GITHUB_ID = os.getenv("GITHUB_ID")
    GITHUB_PASSWORD = os.getenv("GITHUB_PASSWORD")

    driver = start_browser()
    driver.get(CLOUDTYPE_URL)
    time.sleep(3)

    try:
        # GitHub 로그인 버튼 클릭
        element = driver.find_element(By.XPATH, "//*[contains(text(), 'GitHub 계정으로 로그인')]")
        element.click()
        time.sleep(3)
        
        # GitHub 로그인 창
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element(By.ID, "login_field").send_keys(GITHUB_ID)
        driver.find_element(By.ID, "password").send_keys(GITHUB_PASSWORD)
        driver.find_element(By.NAME, "commit").click()
        time.sleep(3)
        
        driver.switch_to.window(driver.window_handles[-1])
    except Exception as e:
        print(f"[{datetime.now()}] 로그인 실패: {e}")
        driver.quit()
        return

    is_restarted = False

    try:
        elements = driver.find_elements(By.CLASS_NAME, "bi-play-fill")
        print(f"[{datetime.now()}] element 개수 - {len(elements)}")

        for element in elements:
            class_attr = element.get_attribute("class")
            if 'text-muted' in class_attr:
                print(f"[{datetime.now()}] 서비스 실행중")
            else:
                parent_element = element.find_element(By.XPATH, "..")
                if 'duration-300' in parent_element.get_attribute("class"):
                    print(f"[{datetime.now()}] 서비스가 중단되어 재시작합니다.")
                    parent_element.click()
                    is_restarted = True

    except Exception as e:
        print(f"[{datetime.now()}] 서비스 상태 체크 실패: {e}")

    time.sleep(2)
    driver.quit()

if __name__ == "__main__":
    main()
