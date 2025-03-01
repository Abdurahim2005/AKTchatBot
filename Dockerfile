# Python 3.10 asosidagi rasmni yuklaymiz
FROM python:3.10

# Ishchi katalog yaratamiz
WORKDIR /app

# Kerakli fayllarni konteynerga nusxalash
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Butun loyihani nusxalash
COPY . .

# Botni ishga tushirish
CMD ["python", "main.py"]
