from pydantic import BaseModel

class UserBase(BaseModel):
    """
    база любого пользователя
    """
    name: str
    age: int

class UserCreate(UserBase):
    """
    на основе этого класса создадим страницу для добавления пользователя
    """
    pass

class User(UserBase):
    """
    вложенный класс Config, который позволит
    работать с ORM объектами для корректной обработки бд
    на основе данных таблицу в бд создаст
    """
    id: int
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    """
    база любого поста
    """
    title: str
    body: str
    author_id: int

class PostCreate(PostBase):
    """
    на основе этого класса создадим страницу для добавления поста
    """
    pass

# название чтобы не пересекалось с
# названием из файла моделей, чтобы не было ошибки
class PostResponse(PostBase):
    """
    на основе этого класса будет описана таблица в бд
    """
    id: int
    author: User
    class Config:
        orm_mode = True