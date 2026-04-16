FROM python:3.9-slim

# 1. Installera systembiblioteket libmagic1
# Vi lägger till --no-install-recommends för att hålla imagen liten
RUN apt-get update && \
    apt-get install -y --no-install-recommends libmagic1 && \
    rm -rf /var/lib/apt/lists/*

# 2. Installera pycti (som drar in python-magic som beroende)
RUN pip install --no-cache-dir pycti

# 3. Resten av din setup
COPY cleanup.py /app/cleanup.py
WORKDIR /app

CMD ["python", "cleanup.py"]