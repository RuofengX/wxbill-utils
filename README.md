# 微信PDF账单转换

## 部署
### 预先依赖
- Python3.11

### 安装依赖
- （可选）创建虚拟环境 `python -m venv .env`
- 安装依赖`pip install -r requirements.txt`

### 运行服务器
`python -m streamlit run wxbill_converter.py`

## 开发
使用
```shell
pipreqs --ignore ".venv"  --force --encoding=utf8 --mode no-pin .
```
更新依赖