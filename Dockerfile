FROM python:3.9-slim-bookworm

WORKDIR /code

# Instala o git e remove os caches pra manter a imagem leve
RUN apt-get update \
    && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

COPY uv.lock pyproject.toml /code/
COPY ./app /code/app

RUN pip install uv \
    && uv sync --frozen

# Set the timezone
ENV TZ=America/Sao_Paulo
EXPOSE 4411

ENV PATH="/code/.venv/bin:$PATH"
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "-b", "0.0.0.0:4411"]