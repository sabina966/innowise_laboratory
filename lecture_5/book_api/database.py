#-----в этом файле описывается подключение к бд-----

# Импортируем функцию для подключения к бд
from sqlalchemy import create_engine
# Импортируем функцию для создания сессий
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

# пропишем url файла бд
SQL_DB_URL = 'sqlite:///database.db'

# переменная с функцией в которую передаём адрес бд и
# снимаем ограничение на подключение из различных потоков
engine = create_engine(SQL_DB_URL, connect_args={"check_same_thread": False})

# взаимодействие с сессией. здесь указываем аргументы,
# что позволяют автоматическую синхронизацию отключает
# и с каким движком работаем
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# функция, что создаст базовый класс из моделей
# позже из них будут таблицы в бд созданы
Base = declarative_base()