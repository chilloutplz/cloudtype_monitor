FROM python:3.9-slim

# 필수 패키지 설치 (Chrome 실행 환경)
RUN apt-get update && apt-get install -y \
    wget \
    libnss3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]