FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 添加 Aerich 数据库迁移命令
CMD ["sh", "-c", "aerich init-db && aerich migrate && aerich upgrade && uvicorn main:app --host 0.0.0.0 --port 8000 & python app/runTask/runMain.py"]
