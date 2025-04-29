from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
import os

<<<<<<< HEAD

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
=======
import time, os

# GitHub Secrets에서 값 불러오기
USERNAME = os.getenv('CLOUDTYPE_ID')  # GitHub Actions에서 주입
PASSWORD = os.getenv('CLOUDTYPE_PW')

# 헤드리스로 chrome 브라우저 실행
chrome_options = Options()
chrome_options.add_argument("--headless")  # 헤드리스 모드 (브라우저 UI 없이 실행)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 웹페이지 열기
driver.get("https://app.cloudtype.io/@unclebob/unclebob:main")
# 페이지 로드 대기
time.sleep(3)

###### 로그인 방법 선택 ######
text_to_find = "GitHub 계정으로 로그인"
try:
    element = driver.find_element(By.XPATH, f"//*[contains(text(), '{text_to_find}')]")  # 텍스트 포함된 요소 찾기
    element.click()

except Exception as e:
    print(f"로그인 방법 선택 오류 발생: {e}")
# 페이지 로드 대기
time.sleep(3)

# 새로운 창으로 전환
driver.switch_to.window(driver.window_handles[-1])

###### 로그인 ######
try:
    id_field = driver.find_element(By.XPATH, '//*[@id="login_field"]')  # ID 입력 필드 찾기")  
    id_field.clear()  # 기존 텍스트 지우기
    id_field.send_keys(USERNAME)  # ID 입력
    password_field = driver.find_element(By.ID, "password")
    password_field.clear()  # 기존 텍스트 지우기
    password_field.send_keys(PASSWORD)  # 비밀번호 입력
    commit_button = driver.find_element(By.NAME, "commit")  # 로그인 버튼 찾기
    commit_button.click()  # 로그인 버튼 클릭
except Exception as e:
    print(f"ID 필드 찾기 오류: {e}")
time.sleep(3)  # 페이지 로드 대기

driver.switch_to.window(driver.window_handles[-1])  # 마지막 창으로 전환

is_restarted = False  # 서비스 재재시작 여부 플래그

while True:
    ###### 서비스 버튼 찾기 ######
    try:
        # 서비스 시작 버튼 icon
        elements = driver.find_elements(By.CLASS_NAME, "bi-play-fill")  # 텍스트 포함된 요소 찾기
        print(f"{datetime.now()}: element개수 - {len(elements)}")
        for element in elements:
            class_attr = element.get_attribute("class")  # 요소의 class 속성 가져오기
            # 'text-muted'는 서비스가 실행중을 의미
            if 'text-muted' in class_attr:
                print(f"{datetime.now()} - 서비스가 실행중입니다.")

            # 서비스가 중단된 경우
            else:
                # icon의 부모인 a 요소를 찾기
                parent_element = element.find_element(By.XPATH, "..")  # 부모 요소 찾기
                
                # 'duration-300'은 각 서비스 버튼의 의미
                if 'duration-300' in parent_element.get_attribute("class"):
                    print(f"{datetime.now()} - 서비스가 중단되어 재시작합니다.")
                    parent_element.click()
                    is_restarted = True
        
        if is_restarted:
            # 서비스 재시작 후 2초 대기
            time.sleep(2)
            # 페이지 새로고침
            driver.close() 
            break

    except Exception as e:
        print(f"요소 찾기 오류 발생: {e}")

    time.sleep(3600)  # 서비스 실행 대기
>>>>>>> b9bb1809b418d5082f9ebc0f2a2aa262a692f100
