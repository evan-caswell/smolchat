# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Add this line to create and set permissions for .streamlit directory
RUN mkdir -p /home/appuser/.streamlit && chown appuser:appuser /home/appuser/.streamlit

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8501

CMD streamlit run 'app.py' --server.port=8501 --server.address=0.0.0.0
