from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

app = Flask(__name__)

# 환경변수에서 GitHub 계정 정보 로드
GITHUB_EMAIL = os.getenv('GITHUB_EMAIL')
GITHUB_PASSWORD = os.getenv('GITHUB_PASSWORD')

def init_driver():
    """Chrome WebDriver 초기화"""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def check_cloudtype_service():
    """CloudType 서비스 상태 확인 및 재시작"""
    driver = init_driver()
    try:
        # 1. CloudType 로그인 페이지 접속
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
        play_buttons = driver.find_elements(By.CLASS_NAME, "bi-play-fill")
        
        for btn in play_buttons:
            if 'text-muted' not in btn.get_attribute("class"):
                btn.find_element(By.XPATH, "..").click()  # 재시작
                return True  # 재시작 발생
        return False  # 재시작 불필요

    except Exception as e:
        print(f"오류 발생: {e}")
        return False
    finally:
        driver.quit()

@app.route("/check", methods=["GET"])
def run_check():
    """외부에서 호출할 API 엔드포인트"""
    is_restarted = check_cloudtype_service()
    return jsonify({"restarted": is_restarted})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)