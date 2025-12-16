FROM python:3.9

WORKDIR /app

# Копируем файл зависимостей первым для эффективного кэширования
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код из локальной папки src в /app в контейнере
COPY src/ .

#CMD ["python", "main.py"] если в main.py name=main
CMD ["uvicorn", "main.py", "--host", "0.0.0.0", "--port", "80"]