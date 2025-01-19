# Python 3.12 기반 이미지 사용
FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /app

# Poetry 설치
RUN pip install --no-cache-dir poetry

# 프로젝트 의존성 파일 복사
COPY pyproject.toml poetry.lock /app/

# Poetry 설정 (가상환경 비활성화) 및 의존성 설치
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# 소스 코드 복사
COPY src /app/src

# 환경 변수로 PYTHONPATH 설정
ENV PYTHONPATH="/app/src"

# FastAPI 실행 (포트 8000)
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]