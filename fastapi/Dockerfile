FROM python:3.10

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app/backend

WORKDIR /app/backend

# 初始化 Aerich 数据库
RUN aerich init-db

CMD ["sh", "-c", "aerich upgrade && uvicorn main:app --host 0.0.0.0 --port 8000 & python app/runTask/runMain.py"]
