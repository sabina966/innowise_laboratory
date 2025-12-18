FROM python:3.14-slim

# усталёўваем сістэмные залежнасці 
# каб можна было праверыць працу сервера праз тэрміналь кантэйнера
RUN apt-get update && apt-get install -y curl

# усталёўваем poetry
RUN pip install poetry

WORKDIR /app

# капіруем залежнасці
# * азначаем, што ня будзе памылкі, калі poetry.lock ня будзе існаваць
COPY pyproject.toml poetry.lock* ./

# усталёўваем гэтыя залежнасці без стварэння віртуальнага асяроддзя
RUN poetry install --no-interaction --no-root

# капіруем код
COPY main_6.py .

# адкрываем порт
EXPOSE 8039

# запускаем
CMD ["poetry", "run", "uvicorn", "main_6:app", "--host", "0.0.0.0", "--port", "8039"]
