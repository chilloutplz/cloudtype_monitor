FROM python:3.12-slim

# 크롬 및 드라이버 설치 (최적화 버전)
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 먼저 복사 (레이어 캐싱 활용)
COPY requirements.txt .

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 코드 복사
COPY . .

# 환경변수 설정 (실제로는 GitHub Actions에서 주입)
ENV PYTHONUNBUFFERED=1 \
    CHROME_BIN=/usr/bin/chromium

# 실행 권한 부여 (필요한 경우)
RUN chmod +x start.py

# 헬스체크 추가 (선택사항)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)"

ENTRYPOINT ["python"]
CMD ["start.py"]