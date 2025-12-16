# импортируем основной класс для работы из библиотеки fastapi
from fastapi import FastAPI
# импортируем класс ошибок HTTPException из библиотеки fastapi
from fastapi import HTTPException
# импортируем класс опционального выбора Optional из библиотеки typing
from typing import Optional
# импортируем класс BaseModel для наследования из библиотеки pydantic
from pydantic import BaseModel
# импортируем класс списка List и класс словаря Dict из библиотеки typing
from typing import List, Dict
# импортируем класс Path, Query для валидации параметров, Body для в. класса из библиотеки fastapi
from fastapi import Path, Query, Body
# импортируем класс для прописи аннотаций Annotated из библиотеки typing
from typing import Annotated
# импортируем класс Field для валидации параметров класса из библиотеки pydantic
from pydantic import Field

# создаём объект на основе этого класса, не передаём никаких параметров
app = FastAPI()

# можем описать обработку различных url адресов
"""
обработка главной страницы
обращаемся к app, как будто это декоратор
и вызываем функцию get (в скобках указываем url адрес обработки)
просто / это обработка главной страницы
"""
@app.get("/")
async def root() -> dict[str, str]:
    """
    создаем функцию,
    которая будет возвращать заданные данные,
    при переходе на главную страницу

    -> dict[str, str] - прописываем, какой тип будет возвращать
    если data из return не совпадает,
    то сервер выдаст ошибку: 500 Internal Server Error

    """
    return {"message": "хмхихи работает? наверное..) трум"} # пусть это будет словарь

@app.get("/contacts")
async def contacts() -> int:
    """
    просто возвращает число 77 :)
    """
    return 77

'''
Для запуска проекта в терминале пишем

( uvicorn learning_FastApi_using:app --reload )

poetry run uvicorn learning_FastApi_using:app --reload --port 8004

poetry run - в нашем случае, так как 
            все пакеты устанавливаются через poetry 
            и само виртуальное окружение от poetry

--reload -  сервер автоматически будет 
            перезагружаться при добавлении 
            чего-либо в файл py
            (только при создании (тестировании)
            проекта используем)
--port 8004 - для нового приложения лучше прописывать новый порт, 
            чтобы комп не путался при запуске
            
Это выдаст нам url адрес, 
по которому переходим на главную страницу, 
что выдаст нам значения нашей функции

Документация всех, нами обрабатываемых в приложении url адресов приложения /docs#

http://127.0.0.1:8004/docs#
'''

# создадим список объектов list[dict]
posts = [
    {'id': 1, 'title': 'News 1', 'content': 'Text 1'},
    {'id': 2, 'title': 'News 2', 'content': 'Text 2'},
    {'id': 3, 'title': 'News 3', 'content': 'Text 3'},
]
@app.get("/items")
async def items():
    """
    заходим на http://127.0.0.1:8004/items,
    жмём галочку автоформатировать и получаем список в красивом виде
    """
    return posts

""" 
создадим динамический url адрес
причем можно сразу несколько параметров выбирать

/items/{id}/{title}/{content}

"""
@app.get("/items/{id}")
async def items(id: int):
    """
    выпишет словарь определенного id,
    пишем детализированную ошибку, если не нашел id в списке
    """
    for post in posts:
        if post['id'] == id:
            return post

    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/search")
async def search(post_id: Optional[int] = None):
    """
    поиск по id: http://127.0.0.1:8013/search?post_id=2
    если параметров несколько, то ищем через знак амперсанта &
    http://127.0.0.1:8013/search?post_id=4&title_name="mummy"
    """
    if post_id:
        for post in posts:
            if post['id'] == post_id:
                return post
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        raise {'data': "No post id provided"}

"""
    В Python не нужно явно прописывать тип данных (int, str и т.д.) 
как в Java, C++ и т.д.
    Но можем запутаться и ошибаться
    Потому стоит прописывать тип данных параметров входных и выходных
Для уверенности в верности и наличии данных. Для описания типов данных 
удобная библиотека pydantic. Можем описывать полноценные отдельные классы, 
что будет возвращать функция
"""

class Poems(BaseModel):
    """
    обозначили чёткую структуру
    """
    id: int
    title: str
    content: str

# создадим список объектов list[dict]
poems = [
    {'id': 1, 'title': 'News 1', 'content': 'Text 1'},
    {'id': 2, 'title': 'News 2', 'content': 'Text 2'},
    {'id': 3, 'title': 'News 3', 'content': 'Text 3'},
]

# распишем подробно, как используется
# class Poems(BaseModel)
"""
@app.get("/smth")
async def smth() -> List[Poems]:   

    # создаём список объектов
    
    poems_objects = []
    
    for poem in poems:
    
        # создаём объект на основе класса и помещаем в список
        
        poems_objects.append(Poems(
            id=poem['id'],
            title=poem['title'],
            content=poem['content'],
        ))
        
    # возвращаем список, гдк каждый элемент это объект,
    # созданный на основе класса Poems(BaseModel)
    # с определённой структурой
    
    return poems_objects
"""

# а теперь в кратце
@app.get("/smth")
async def smth() -> List[Poems]:
    # важно чтоб каждый элемент соответствовал
    # такой структуре, иначе ошибка Internal Server Error
    # Poems(**poem) for poem in poems - означает, что мы
    # объект poem из листа poems конвертируем в класс Poems
    return [Poems(**poem) for poem in poems]

# с Search, так как вернуть может не только элемент класса, но и наш ответ,
# то в выходной тип прописываем Optional[Poems]. А наш ответ пишем None,
# что также подходит к функции Optional[Poems] - возвращает или
# элемент класса, или ничего

# @app.get("/search")
# async def search(post_id: Optional[int] = None) -> Dict[str, Optional[Poems]]:
#     if poem_id:
#         for poem in poems:
#             if poem['id'] == poem_id:
#                 return {"data": Poems(**poem)}
#         raise HTTPException(status_code=404, detail="Poem not found")
#     else:
#         raise {'data': None}


# Связь двух классов используя pydentic classes
class User(BaseModel):
    id: int
    name: str
    age: int

class Book(BaseModel):
    id: int
    title: str
    author: User # опишет всю информацию об авторе

users = [
    {'id': 1, 'name': '<NAME>', 'age': 25},
    {'id': 2, 'name': '<NAME>', 'age': 25},
    {'id': 3, 'name': '<NAME>', 'age': 25},
]

books = [
    {'id': 1, 'title': 'Book 1', 'author': users[0]},
    {'id': 2, 'title': 'Book 2', 'author': users[1]},
    {'id': 3, 'title': 'Book 3', 'author': users[2]},
]

"""
Обработка HTTP запросов

.get напрямую переход к определённому адресу

    example: @app.get("/search")
    
.post передача что-то из формы и добавляем в дату

.put приём данных при редактировании

    ex: @app.put("/items/edit/{item_id}")
        где через динамическую переменную 
        обращаемся к изменяемому объекту

.delete удаление чего-либо

    ex: @app.delete("/items/delete/{item_id}")
        где через динамическую переменную 
        указываем удаляемый объект
    
"""
# создаём класс объекта для добавления новой книги
# тут id принимается автоматически
# author_id: int принимает не всю информацию об авторе, а только его id
class BookCreate(BaseModel):
    title: str
    author_id: int

# можем название адреса использовать повторно,
# так как обработка запросов get, post и т.д. разная!
# next((), None) - функция работающая до 1-го совпадения,
# а если совпадения нет, то выдаёт None
# 404 страница не найдена
@app.post("/books/add")
async def add_book(book: BookCreate) -> Book:
    author = next((user for user in users if user['id'] == book.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    # мы при вызове функции передали ей title, author_id
    # если заданный author_id есть в id пользователей, то
    # у нас создастся новая книга, для нее остаётся задать new_book_id
    # для этого посчитали к-во книг и добавили + 1 для новой
    new_book_id = len(books) + 1
    new_book = {'id': new_book_id, 'title': book.title, 'author': author}
    books.append(new_book)
    # прописываем, что возвращаем книгу, так как задали в
    # параметрах выходных для функции -> Book
    return Book(**new_book)

# Просто зайти по URL адресу не зайти, а вот через /docs# возможно

#-----учимся создавать и валидировать (проверять данные) URL адреса-----
# можем прописывать аннотации для параметров, что выдаёт ф-ция
# за счёт аннотаций можем дописывать проверки сразу в
# момент получения данных. Сразу можно понять ошибку
# и исправить клиентскую часть
#--Импортировали классы Path, Annotated

class Student(BaseModel):
    id: int
    name: str
    grade: int

students = [
    {'id': 1, 'name': 'Olya', 'grade': 100},
    {'id': 2, 'name': 'Katya', 'grade': 100},
]

@app.get("/students/{student_id}")
async def students(student_id: Annotated[int, Path(..., title="where are student's id", ge=1, lt=100)]) -> Student:
    for student in students:
        if student['id'] == student_id:
            return Student(**student)
    raise HTTPException(status_code=404, detail="Student not found")
"""
    Здесь в аннотации можно увидеть тип и описание через Path(title)
Но чтобы увидеть описание требуется в формат документации по пути
http://127.0.0.1:8013/redoc

                        ВАЛИДАЦИЯ 
                    (проверка вх данных)

    Path(...) - означает, что параметр id обязательно доожен быть передан
иначе это ошибка
    Path(ge=1) - Если число id меньше 1, то автоматически ошибка
ge - greater, equal (больше или равно)
lt - less then (меньше чем)
max_length - максимальная длинна 
(можно использовать как для int, так и для str)

    ex: 
    то что на сайте /redoc:
        integer (where are student's id) [1..100) 
    
    то, что по ссылке http://127.0.0.1:8013/students/0:
        {"detail":[{"type":"greater_than_equal","loc":["path","student_id"],"msg":"Input should be greater than or equal to 1","input":"0","ctx":{"ge":1}}]}

"""

@app.get("students/search")
async def search_students(student_id: Annotated[
    Optional[int],
    Query(title="id of student to search", ge=1, le=30)
]) -> Dict[str, Optional[Student]]:
    if student_id:
        for student in students:
            if student['id'] == student_id:
                return {"data": Student(**student)}
        raise HTTPException(status_code=404, detail="Student not found")
    else:
        raise {"data": None}

"""
Тут не можем использовать Path, так как не имеем динамического параметра
Для данных, что идут после знака ? используем класс Query()
"""

"""
ВАЛИДАЦИЮ можно использовать и для классов ;)

тут используется класс Field для валидации параметров класса,
но его импортируем из библиотеки pydantic так как работаем с классом,
остальное по аналогии

для валидации самих классов используем Body(),
где пропишем пример, как должен выглядеть передаваемый объект
это полезно для документации

создадим класс для добавления студента

"""

class StudentCreate(BaseModel):
    name: Annotated[
        str,
        Field(..., title="name of student", min_length=2, max_length=20),
    ]
    grade: Annotated[
        int,
        Field(..., title="grade of student", ge=1, le=100),
    ]

@app.post("/students/add")
async def add_student(student: Annotated[
    StudentCreate,
    Body(..., example={"name": "<NAME>", "grade": 100})
]) -> Student:
    new_student_id = len(students) + 1
    new_student = {'id': new_student_id, 'name': student.name, 'grade': student.grade}
    students.append(new_student)
    return Student(**new_student)


#-----работа с бд---------
# для этого будем пользоваться библиотека ми sqlalchemy и sqllite3
# создадим новый файл, где опишем все классы,
# с которыми взаимодействуем schemas.py
