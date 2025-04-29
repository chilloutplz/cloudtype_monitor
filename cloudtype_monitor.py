from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
import os
import time

def get_github_credentials():
    """환경 변수에서 GitHub 로그인 정보를 가져옵니다."""
    github_id = os.getenv("GITHUB_ID")
    github_password = os.getenv("GITHUB_PASSWORD")
    if not github_id or not github_password:
        raise ValueError("환경 변수 GITHUB_ID와 GITHUB_PASSWORD가 설정되지 않았습니다.")
    return github_id, github_password


def setup_webdriver():
    """Chrome WebDriver를 설정합니다."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 UI 없이 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def login_to_github(driver, github_id, github_password):
    """GitHub 계정으로 로그인합니다."""
    print(f"{datetime.now()} - login_to_github 시작")
    driver.get("https://app.cloudtype.io/@unclebob/unclebob:main")
    time.sleep(3)

    # 로그인 버튼 클릭
    login_button = driver.find_element(By.XPATH, "//*[contains(text(), 'GitHub 계정으로 로그인')]")
    login_button.click()
    time.sleep(3)

    # GitHub 로그인
    driver.switch_to.window(driver.window_handles[-1])
    username_field = driver.find_element(By.ID, "login_field")
    username_field.send_keys(github_id)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(github_password)
    driver.find_element(By.NAME, "commit").click()
    time.sleep(3)
    print(f"{datetime.now()} - login_to_github 완료")


def monitor_service(driver):
    """CloudType 서비스를 모니터링하고 중단 시 재시작합니다."""
    print(f"{datetime.now()} - monito_service 시작")
    try:
        elements = driver.find_elements(By.CLASS_NAME, "bi-play-fill")
        print(f"{datetime.now()}: 발견된 요소 개수 - {len(elements)}")

        for element in elements:
            class_attr = element.get_attribute("class")
            if 'text-muted' in class_attr:
                print(f"{datetime.now()} - 서비스가 실행 중입니다.")
            else:
                parent_element = element.find_element(By.XPATH, "..")
                if 'duration-300' in parent_element.get_attribute("class"):
                    print(f"{datetime.now()} - 서비스가 중단되어 재시작합니다.")
                    parent_element.click()
                    is_restarted = True

    except Exception as e:
        print(f"{datetime.now()} - 요소 탐색 중 오류 발생: {e}")


def main():
    """스크립트의 메인 실행 함수."""
    github_id, github_password = get_github_credentials()
    driver = setup_webdriver()

    try:
        login_to_github(driver, github_id, github_password)
        monitor_service(driver)
    except Exception as e:
        print(f"{datetime.now()} - 스크립트 실행 중 오류 발생: {e}")
    finally:
        driver.quit()
        print(f"{datetime.now()} - WebDriver가 종료되었습니다.")


if __name__ == "__main__":
    main()