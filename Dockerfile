FROM python:3.9-slim
RUN pip install --no-cache-dir pycti
COPY cleanup.py /app/cleanup.py
WORKDIR /app
CMD ["python", "cleanup.py"]