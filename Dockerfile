FROM python:3.12.2
LABEL authors="crusazer"

# Создание и переход в рабочую директорию в контейнере
WORKDIR /CozyGames

# Копирование зависимостей проекта в контейнер
COPY requirements.txt /CozyGames/

# Установка зависимостей проекта
RUN pip install -r requirements.txt

# Копирование остальных файлов проекта в контейнер
COPY . /CozyGames/

# Установка Celery
RUN pip install redis
RUN pip install celery

# Открываем порт, на котором будет работать Django
EXPOSE 8000

#CMD ["sleep", "3" && "python3", "manage.py", "migrate" && "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
CMD ["sh", "-c", "sleep 3 && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000 & celery -A cozygames_core worker --loglevel=info"]