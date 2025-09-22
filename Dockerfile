FROM python:3.9-slim

# Python 環境最佳化
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 設定工作目錄
WORKDIR /app

# 先複製需求並安裝（利用快取）
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 再複製專案程式碼
COPY . ./

# 可在執行容器時以 -e 覆蓋下列環境變數
ENV PTT_ID=your_PTT_ID \
    PTT_PW=your_PTT_PW \
    LOG_DIR=logs \
    LOG_LEVEL=INFO

# 預設執行
CMD ["python", "main.py"]
