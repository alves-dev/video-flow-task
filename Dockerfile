FROM python:3.13-slim-bookworm AS builder

WORKDIR /code

RUN apt-get update \
    && apt-get install -y git ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock /code/

RUN uv sync --frozen

COPY ./app /code/app


FROM python:3.13-slim-bookworm

WORKDIR /code

RUN apt-get update \
    && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /code/.venv /code/.venv
COPY --from=builder /code/app /code/app

ENV PATH="/code/.venv/bin:$PATH"
ENV TZ=America/Sao_Paulo

EXPOSE 4411

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "-b", "0.0.0.0:4411"]