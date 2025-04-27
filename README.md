# CloudType Monitor for Render

## 기능
- CloudType 서비스가 중단되면 자동으로 재시작
- 매일 새벽 2~5시 30분 간격으로 실행 (Render CronJob)

## 사용 방법
1. GitHub에 이 프로젝트 업로드
2. Render에 새로운 "Cron Job" 만들기
3. 환경변수 설정
   - `GITHUB_ID`
   - `GITHUB_PASSWORD`
4. 스케줄 설정 (UTC 기준: 17시~20시 30분 간격)

## 필수
- Python 3.11
- Selenium
- Headless Chrome 환경
