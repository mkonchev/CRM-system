FROM python:3.12-slim as builder

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --all-extras

FROM python:3.12-slim

COPY --from=builder /.venv /.venv

COPY . .

ENV PATH="/.venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

WORKDIR /app