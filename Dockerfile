FROM python:3.12.1-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.0.1

RUN groupadd -g 1000 appgroup && \
    useradd -m -u 1000 -g appgroup appuser

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY src /app/src

RUN chown -R appuser:appgroup /app

USER appuser

ENV PYTHONPATH="/app/src"

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]