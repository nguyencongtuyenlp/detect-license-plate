# Sử dụng Python 3.9
FROM python:3.9-slim

# Cài đặt các thư viện hệ thống cần thiết cho OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file yêu cầu và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Hugging Face Spaces mặc định chạy cổng 7860
EXPOSE 7860

# Chạy ứng dụng Flask
# Lưu ý: Sửa port thành 7860 và host 0.0.0.0 trong app.py
CMD ["python", "app.py"]
