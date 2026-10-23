# Resmi Python imajını kullanıyoruz
FROM python:3.11-slim

# Sistem gereksinimlerini güncelliyoruz (PostgreSQL ve Derin Öğrenme için)
RUN apt-get update && apt-get install -y libpq-dev gcc

# Çalışma dizinini ayarlıyoruz
WORKDIR /app

# Gereksinim dosyasını kopyalayıp kütüphaneleri kuruyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projenin tüm kodlarını konteynere kopyalıyoruz
COPY . .

# Gunicorn ile Django'yu yayına alıyoruz (Dışarıdan gelen isteklere 8000 portunu açıyoruz)
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]