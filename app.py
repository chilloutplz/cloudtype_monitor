from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
import time

app = Flask(__name__)

# 환경변수 로드
GITHUB_EMAIL = os.getenv('GITHUB_EMAIL')
GITHUB_PASSWORD = os.getenv('GITHUB_PASSWORD')

def init_driver():
    """webdriver-manager로 자동 ChromeDriver 설정"""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 자동 드라이버 설치 및 실행
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

def check_and_restart():
    """CloudType 서비스 확인 및 재시작"""
    driver = init_driver()
    try:
        # 1. CloudType 접속
        driver.get("https://app.cloudtype.io/@unclebob/unclebob:main")
        time.sleep(3)

        # 2. GitHub 로그인
        driver.find_element(By.XPATH, "//*[contains(text(), 'GitHub 계정으로 로그인')]").click()
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element(By.ID, "login_field").send_keys(GITHUB_EMAIL)
        driver.find_element(By.ID, "password").send_keys(GITHUB_PASSWORD)
        driver.find_element(By.NAME, "commit").click()
        time.sleep(5)

        # 3. 서비스 상태 확인
        driver.switch_to.window(driver.window_handles[0])
        buttons = driver.find_elements(By.CSS_SELECTOR, ".bi-play-fill:not(.text-muted)")
        
        if buttons:
            buttons[0].find_element(By.XPATH, "..").click()
            return True  # 재시작 발생
        return False  # 재시작 불필요

    except Exception as e:
        print(f"오류: {str(e)}")
        return False
    finally:
        driver.quit()

@app.route("/monitor", methods=["GET"])
def monitor():
    """모니터링 API 엔드포인트"""
    return jsonify({"restarted": check_and_restart()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
