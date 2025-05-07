from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from datetime import datetime
import os
import time

def get_github_credentials():
    """환경 변수에서 GitHub 로그인 정보를 가져옵니다."""
    github_id = os.environ.get("CLOUDTYPE_ID")
    github_password = os.environ.get("CLOUDTYPE_PW")
    if not github_id or not github_password:
        raise ValueError("환경 변수 CLOUDTYPE_ID와 CLOUDTYPE_PW가 설정되지 않았습니다.")
    return github_id, github_password


def setup_webdriver():
    """Chrome WebDriver를 설정합니다."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 UI 없이 실행 (필요 시 활성화)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")  # 알림 비활성화
    chrome_options.add_argument("--disable-popup-blocking")  # 팝업 차단 비활성화
    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,  # 비밀번호 저장 창 비활성화
        "profile.password_manager_enabled": False  # 비밀번호 관리 비활성화
    })
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def login_to_github(driver, github_id, github_password):
    """GitHub 계정으로 로그인합니다."""
    print(f"{datetime.now()} - login_to_github 시작")
    driver.get("https://app.cloudtype.io/@starnew/unclebob:main")

    # JavaScript 렌더링 완료 대기
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "app"))  # 렌더링 완료를 확인할 수 있는 요소
        )
        print(f"{datetime.now()} - JavaScript 렌더링이 완료되었습니다.")
    except Exception as e:
        print(f"{datetime.now()} - JavaScript 렌더링 대기 중 오류 발생: {e}")
        return

    # JavaScript 렌더링 완료 후 페이지 소스를 저장
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"page_source_{timestamp}.html"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        print(f"{datetime.now()} - 페이지 소스가 {file_path} 파일에 저장되었습니다.")
    except Exception as save_error:
        print(f"{datetime.now()} - 페이지 소스 저장 중 오류 발생: {save_error}")

    # 로그인 버튼 대기
    try:
        login_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(., 'GitHub 계정으로 로그인')]"))
        )
        login_button.click()
        print(f"{datetime.now()} - GitHub 계정으로 로그인 버튼을 클릭했습니다.")
    except Exception as e:
        print(f"{datetime.now()} - 로그인 버튼을 찾을 수 없습니다: {e}")
        return

    # GitHub 로그인
    try:
        driver.switch_to.window(driver.window_handles[-1])
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login_field"))
        )
        username_field.send_keys(github_id)

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(github_password)
        driver.find_element(By.NAME, "commit").click()
        print(f"{datetime.now()} - login_to_github 완료")
    except Exception as e:
        print(f"{datetime.now()} - GitHub 로그인 중 오류 발생: {e}")

    # 활성 창으로 전환 - 비밀번호 변경 경고창 우회
    try:
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[0])  # 첫 번째 창으로 전환
            print(f"{datetime.now()} - 활성 창으로 전환했습니다.")
        else:
            print(f"{datetime.now()} - 활성 창이 없습니다.")
    except Exception as e:
        print(f"{datetime.now()} - 창 전환 중 오류 발생: {e}")


def monitor_service(driver):
    """CloudType 서비스를 모니터링하고 중단 시 재시작합니다."""
    print(f"{datetime.now()} - monitor_service 시작")

    # 현재 창의 개수 출력
    print(f"{datetime.now()} - 현재 창 개수: {len(driver.window_handles)}")

    # 현재 창의 인덱스 확인
    current_window_handle = driver.current_window_handle
    window_index = driver.window_handles.index(current_window_handle)
    print(f"{datetime.now()} - 현재 창의 인덱스: {window_index}")

    driver.switch_to.window(driver.window_handles[0])

    try:
        # 비밀번호 변경 경고창 확인
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(f"{datetime.now()} - 경고창 텍스트: {alert.text}")
            alert.accept()  # 확인 버튼 클릭
            print(f"{datetime.now()} - 경고창을 닫았습니다.")
        except Exception:
            print(f"{datetime.now()} - 경고창이 없습니다.")

        # 요소가 나타날 때까지 대기
        elements = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//*[contains(@class, 'bi-play-fill')]")
            )
        )
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

    except Exception as e:
        print(f"{datetime.now()} - 요소 탐색 중 오류 발생: {e}")
    finally:
        # 페이지 소스를 항상 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"page_source_{timestamp}.html"
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(driver.page_source)
            print(f"{datetime.now()} - 페이지 소스가 {file_path} 파일에 저장되었습니다.")
        except Exception as save_error:
            print(f"{datetime.now()} - 페이지 소스 저장 중 오류 발생: {save_error}")


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
