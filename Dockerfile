FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 DATABASE_PATH=/data/names.db
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/* && groupadd --system --gid 10001 app && useradd --system --uid 10001 --gid app --home-dir /app app && mkdir -p /data && chown -R app:app /app /data
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=app:app app.py .
RUN mkdir -p /tmp && chmod 1777 /tmp
USER 10001:10001
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 CMD curl -fsS http://127.0.0.1:8080/healthz || exit 1
CMD ["gunicorn","--bind","0.0.0.0:8080","--workers","2","--access-logfile","-","--error-logfile","-","app:app"]
