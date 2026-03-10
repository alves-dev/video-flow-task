FROM python:3.13-slim-bookworm

WORKDIR /code

# Instala dependências do sistema e  remove os caches
RUN apt-get update \
    && apt-get install -y git ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml uv.lock /code/
RUN uv sync --frozen

COPY ./app /code/app

ENV TZ=America/Sao_Paulo
ENV PATH="/code/.venv/bin:$PATH"

EXPOSE 4411

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "-b", "0.0.0.0:4411"]