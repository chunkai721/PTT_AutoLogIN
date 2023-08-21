# 使用官方的 Python 基礎映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製當前目錄的內容到容器的 /app 目錄
COPY . /app

# 使用 requirements.txt 安裝所需的 Python 套件
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# 設置環境變數（您可以在運行容器時覆蓋它們）
ENV PTT_ID=your_PTT_ID
ENV PTT_PW=your_PTT_PW
ENV PTTAUTOLOGIN_LINE_TOKEN=your_LINE_TOKEN

# 執行 Python 程式
CMD ["python", "main.py"]
