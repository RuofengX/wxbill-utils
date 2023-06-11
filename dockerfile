# 使用python3.9镜像作为基础镜像
FROM python:3.11

# 将当前目录添加到容器中的 /app 目录
ADD . /app

# 工作目录设置为 /app
WORKDIR /app

# 安装依赖包
RUN pip install --upgrade pip && pip install -r requirements.txt

# 设置环境变量
ENV PORT 9000

# 对外暴露端口
EXPOSE ${PORT}

# 启动应用
CMD ["streamlit", "run", "wxbill_converter.py"' "--server.port", "8000"]
