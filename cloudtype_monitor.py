from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 브라우저 UI 없이 실행
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# WebDriver 설정 (webdriver_manager를 사용하여 최신 chromedriver 설치)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹사이트 열기
driver.get("https://app.cloudtype.io/@unclebob/unclebob:main")
time.sleep(3)

# 로그인 과정
try:
    login_button = driver.find_element(By.XPATH, "//*[contains(text(), 'GitHub 계정으로 로그인')]")
    login_button.click()
    time.sleep(10)
    
    # GitHub 로그인
    driver.switch_to.window(driver.window_handles[-1])
    username_field = driver.find_element(By.ID, "login_field")
    username_field.send_keys("your_email@example.com")
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("your_password")
    driver.find_element(By.NAME, "commit").click()
    time.sleep(3)
    
    # 서비스 상태 모니터링
    is_restarted = False  # 서비스 재시작 여부 플래그

    while True:
        # 서비스 시작 버튼 찾기
        try:
            elements = driver.find_elements(By.CLASS_NAME, "bi-play-fill")
            print(f"{datetime.now()}: element 개수 - {len(elements)}")
            
            for element in elements:
                class_attr = element.get_attribute("class")  # 요소의 class 속성 가져오기
                if 'text-muted' in class_attr:
                    print(f"{datetime.now()} - 서비스가 실행중입니다.")
                else:
                    parent_element = element.find_element(By.XPATH, "..")  # 부모 요소 찾기
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
        
        time.sleep(3600)  # 1시간 대기

except Exception as e:
    print(f"로그인 실패: {e}")

# 종료
driver.quit()
