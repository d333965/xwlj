# 基于 python:3.10 镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制 FastAPI 项目到容器
COPY . .

# 安装项目依赖
RUN pip install --no-cache-dir -r backend/requirements.txt

# 暴露端口
EXPOSE 8000

# 默认命令，后续会在 docker-compose 中覆盖
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
