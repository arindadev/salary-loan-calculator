# frontend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["sh", "-c", "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"]