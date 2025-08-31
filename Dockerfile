# استخدام Python 3.11 slim كصورة أساسية
FROM python:3.11-slim

# تعيين مجلد العمل
WORKDIR /app

# نسخ ملفات المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ ملفات البوت
COPY main.py .
COPY run_bot.py .

# إنشاء مجلد للبيانات
RUN mkdir -p /app/data

# تعيين متغير البيئة للبيانات
ENV DATA_DIR=/app/data

# تعيين المستخدم غير الجذر للأمان
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# عرض المنفذ (اختياري للمراقبة)
EXPOSE 8000

# تشغيل البوت
CMD ["python", "main.py"]