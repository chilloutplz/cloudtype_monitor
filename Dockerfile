FROM python:3.11-slim

# 기본 패키지 설치
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium-driver \
    chromium

# 작업 디렉토리 설정
WORKDIR /app

# 코드 복사
COPY . .

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 환경변수 예시 (Render Dashboard에 설정하는 게 더 좋아)
# ENV GITHUB_ID=your_id_here
# ENV GITHUB_PASSWORD=your_password_here

# 실행
CMD ["python", "start.py"]
