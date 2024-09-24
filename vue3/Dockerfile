# 使用 Node.js 作为构建阶段
FROM node:16 AS build-stage

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json（如果有）
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制所有源代码到工作目录
COPY . .

# 构建项目
RUN npm run build

# 使用 Nginx 作为生产环境的服务器
FROM nginx:alpine AS production-stage

# 复制构建输出到 Nginx 的静态资源目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 暴露 Nginx 端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
