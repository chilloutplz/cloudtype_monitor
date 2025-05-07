from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import os
import time

<<<<<<< HEAD
def setup_driver():
    """Chrome WebDriver 설정"""
=======
def get_github_credentials():
    """환경 변수에서 GitHub 로그인 정보를 가져옵니다."""
    github_id = os.environ.get("CLOUDTYPE_ID")
    github_password = os.environ.get("CLOUDTYPE_PW")
    if not github_id or not github_password:
        raise ValueError("환경 변수 CLOUDTYPE_ID와 CLOUDTYPE_PW가 설정되지 않았습니다.")
    return github_id, github_password


def setup_webdriver():
    """Chrome WebDriver를 설정합니다."""
>>>>>>> 32493ca4d884d2979e39d488c9b62d9a8aa11e0c
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # GitHub Actions에서는 헤드리스 필수
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    
    service = Service(executable_path="/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=chrome_options)

def login_to_cloudtype(driver):
    """CloudType에 로그인"""
    try:
        # GitHub Secrets에서 인증 정보 가져오기
        USER_ID = os.environ["CLOUDTYPE_ID"]
        USER_PW = os.environ["CLOUDTYPE_PW"]
        
        driver.get("https://app.cloudtype.io/@unclebob/unclebob:main")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'GitHub 계정으로 로그인')]"))
        ).click()
        
        # GitHub 로그인 창으로 전환
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        
        # GitHub 로그인 수행
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login_field"))
        ).send_keys(USER_ID)
        
        driver.find_element(By.ID, "password").send_keys(USER_PW)
        driver.find_element(By.NAME, "commit").click()
        
        # 원래 창으로 돌아가기
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 1)
        driver.switch_to.window(driver.window_handles[0])
        
        print(f"{datetime.now()} - 로그인 성공")
        return True
        
    except Exception as e:
        print(f"{datetime.now()} - 로그인 실패: {e}")
        return False

def monitor_service(driver):
    """서비스 모니터링 및 재시작"""
    try:
        elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "bi-play-fill"))
        )
        
        for element in elements:
            if 'text-muted' not in element.get_attribute("class"):
                parent = element.find_element(By.XPATH, "..")
                if 'duration-300' in parent.get_attribute("class"):
                    print(f"{datetime.now()} - 서비스 재시작 시도")
                    parent.click()
                    time.sleep(5)  # 재시작 대기
                    return True
        return False
    except Exception as e:
        print(f"{datetime.now()} - 모니터링 오류: {e}")
        return False

def main():
    driver = setup_driver()
    try:
        if login_to_cloudtype(driver):
            while True:
                if monitor_service(driver):
                    print(f"{datetime.now()} - 서비스 재시작 완료")
                else:
                    print(f"{datetime.now()} - 서비스 정상 동작 중")
                
                print(f"{datetime.now()} - 10분 후 다시 확인")
                time.sleep(600)  # 10분 대기
                
    finally:
        driver.quit()
        print(f"{datetime.now()} - 작업 완료")

if __name__ == "__main__":
    main()
