# 使用python3.9镜像作为基础镜像
FROM python:3.11

# 将当前目录添加到容器中的 /app 目录
ADD . /app

# 工作目录设置为 /app
WORKDIR /app

# 安装依赖包
RUN pip install -r requirements.txt --index-url https://mirrors.cloud.tencent.com/pypi/simple

# 对外暴露端口
EXPOSE 9000

# 启动应用
CMD ["streamlit", "run", "wxbill_converter.py","--browser.gatherUsageStats", "false", "--server.port", "9000"]
