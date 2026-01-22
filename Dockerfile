# Sử dụng Python 3.9
FROM python:3.9-slim

# Cài đặt các thư viện hệ thống cần thiết cho OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Tạo người dùng mới với UID 1000 (yêu cầu của Hugging Face)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file yêu cầu và cài đặt thư viện
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container (với quyền sở hữu của user)
COPY --chown=user . .

# Hugging Face Spaces chạy cổng 7860
EXPOSE 7860

# Chạy ứng dụng Flask
# Thiết lập biến môi trường PORT cho app.py nhận diện
ENV PORT=7860

CMD ["python", "app.py"]
