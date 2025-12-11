from fastapi import FastAPI, Depends, HTTPException, Query  # Используем HTTPException из FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session
import uvicorn
from pydantic import BaseModel
from typing import List, Optional


# -------- Define the DB and ORM Model
class Base(DeclarativeBase):
    """
    This is the minimum base class
    from which all SQLAlchemy models must inherit.
    """
    pass


# Define Book model (SQLAlchemy ORM)
class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[Optional[int]] = mapped_column(nullable=True)  # year должен быть опциональным


# Create database engine
engine = create_engine('sqlite:///book.db',
                       connect_args={"check_same_thread": False})  # Добавил connect_args для SQLite
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# --------Create FastAPI Application
app = FastAPI(title="Book Collection API")


# Pydantic schemas (ОТДЕЛЬНО от SQLAlchemy моделей!)
class BookCreate(BaseModel):  # Для создания книги (без ID)
    title: str
    author: str
    year: Optional[int] = None


class BookUpdate(BaseModel):  # Для обновления книги (все поля опциональны)
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None


class BookResponse(BaseModel):  # Для ответа (с ID)
    id: int
    title: str
    author: str
    year: Optional[int] = None

    class Config:
        from_attributes = True  # Позволяет конвертировать SQLAlchemy модель в Pydantic


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoints
@app.get("/")
def read_root():
    return {"Hello": "Welcome to Book Collection API"}


@app.post('/books', response_model=BookResponse, status_code=201)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Add a book to the database
    """
    db_book = Book(**book.model_dump())  # Создаем SQLAlchemy модель
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get('/books', response_model=List[BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    """
    Get all books in the database
    """
    db_books = db.query(Book).all()
    return db_books


@app.delete('/books/{book_id}')  # Переименовал параметр для ясности
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book by id
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()  # Используем filter вместо get
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": f"Book with ID {book_id} deleted"}


@app.put('/books/{book_id}', response_model=BookResponse)
def update_book_details(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    """
    Update book details
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Обновляем только переданные поля
    update_data = book_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@app.get('/books/search/', response_model=List[BookResponse])
def search_books(
        title: Optional[str] = Query(None, description="Search by title"),
        author: Optional[str] = Query(None, description="Search by author"),
        year: Optional[int] = Query(None, description="Search by year"),
        db: Session = Depends(get_db)
):
    """
    Search books by title, author, or year
    """
    query = db.query(Book)  # Используем Book (SQLAlchemy модель), а не BookDB

    if title:
        query = query.filter(Book.title.contains(title))
    if author:
        query = query.filter(Book.author.contains(author))
    if year:
        query = query.filter(Book.year == year)

    books = query.all()
    return books


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

# Open on localhost http://127.0.0.1:8080/docs#/