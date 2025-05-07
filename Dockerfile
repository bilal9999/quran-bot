FROM python:3.10-slim

# تثبيت المتطلبات الأساسية
RUN apt update && apt install -y build-essential ffmpeg && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد التطبيق
WORKDIR /app

# نسخ ملفات المشروع إلى الحاوية
COPY . /app

# تثبيت مكتبات بايثون
RUN pip install --no-cache-dir -r requirements.txt

# أمر تشغيل البوت
CMD ["python", "main.py"]
