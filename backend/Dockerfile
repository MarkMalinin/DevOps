
FROM python:3.11-slim

# Prevents python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
# For local dev we can run the builtin server; replace CMD with gunicorn for prod
CMD ["python", "app.py"]
# Production alternative (uncomment to use gunicorn):
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
