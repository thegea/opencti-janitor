FROM python:3.9-slim

# Installera systemberoenden (libmagic är kritiskt för pycti)
RUN apt-get update && \
    apt-get install -y --no-install-recommends libmagic1 && \
    rm -rf /var/lib/apt/lists/*

# Installera python-bibliotek
RUN pip install --no-cache-dir pycti

# Kopiera in skriptet
COPY cleanup.py /app/cleanup.py

WORKDIR /app

# Kör skriptet
CMD ["python", "cleanup.py"]