from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from typing import Optional, List, Dict, Annotated
from sqlalchemy.orm import Session
from models import Base, User, Post
from database import engine, session_local
from schemas import UserCreate, User as DbUser, PostCreate, PostResponse
# для налады сувязі
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# _______ налады CORS
# адраса, што маюць доступ да бэкэнд прыкладання
origins = [
    "http://localhost:8081",
    "http://192.168.1.60:8081",
    "http://127.0.0.1:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# дзеля стварэння табліц на аснове класаў

Base.metadata.create_all(bind=engine)

def get_db():
    """
    ф-цыя далучэння да бд
    стварае сэсію для далучэння да бд
    праз yield спрабуе далучыцца
    і ў незалежнасці ад спробы па выніках зачыняе яе
    """
    db = session_local()
    try:
        yield db # вяртае сэсію бд для выкарыстання ў маршрутах
    finally:
        db.close()

@app.post("/users/", response_model=DbUser) # аргумент: класс з schemas
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> DbUser:
    """
    Ф-цыя прыманне аб'екту і ствараць новага карыстальніка ў бд
    Пры пераходзе па спасылцы /users/ прымае: клас UserCreate і далучаецца да бд
    У ходзе апрацоўцы: дадае новага карыстальніка ў бд і абнаўляе бд
    Ф-цыя вяртае: даданага карыстальніка
    """
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostResponse:
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post

@app.get("/posts/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)) -> List[PostResponse]:
    return db.query(Post).all()

@app.get("/users/{name}", response_model=DbUser)
async def get_user(name: str, db: Session = Depends(get_db)) -> DbUser:
    db_user = db.query(User).filter(User.name == name).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#____будзем ствараць кліентскую частку (фронтэнд) альбо знешні выгляд праекту
# можна пісаць на Java script, ці з выкарыстаннем frameworks,
# such as React, Angular and etc.
# будзем выкарыcтоўваць Vue.js:
#           (Progressive framework (incrementally adoptable),
#           gentle learning curve, reactive data binding, lightweight.
#
#           Startups, small to medium-sized projects, or for integrating
#           into existing projects that need enhanced interactivity)
#
#1) ствараем папку public
#2) пераходзім ў яе праз термінальcd
#       "C:\Users\Sabina Alieva\PycharmProjects\innowise_laboratory\lecture_5\book_api\public"
#3)у ёй ствараем vue.js праект
#
#  але перад гэтым на іх сайце https://cli.vuejs.org/guide/installation.html
# трэба запампаваць Node.js і ўсталяваць.
# АЛЕ! без усіх астатніх прапанаваных утілітаў (навошта памяць задурваць)
#
#   ( . кропка азначае, што стварем мінавіта ў гэтай папцы, дзе знаходзімся):
#       vue create .
#           Vue CLI v5.0.9
#           ? Generate project in current directory? Yes
#           ? Please pick a preset: Default ([Vue 3] babel, eslint)
#
# але праз терміналь pyCharm не атрымалася, закінула тую ж аперацыю
# ў PowerShell пад імём адміністратара і паперш перашоўшы ў патрэбную папку,
# а перад гэтым дазвол на выкананне скрыптоў:
# Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
# (дарэчы, мажліва такое праканала б і ў terminal pycharm **) )
# усталёўваем nmp install axios
# бібліятэка, што дазволіць карыстальніку ( з боку папкі Public) звяртацца
# па пэўнаму url адрасу да сервернага прыкладання
#   не атрымалася ўсталяваць праз Pycharm, таму зноў каманду праз PowerShell
#    з-за геа.палітыкі npm вельмі марудна пампуе. Вырашэнне:
#   npm install -g yarn
#   yarn add axios
# пры ўсім пры гэтым yarn працуе толькі з node.js больш старой версіі (22)
# таму яшчэ і версію трэба па новай пампаваць
# перад гэтым старую версію зруініць : Пуск -- Nude.js -- Uninstall Nude.js
# не забываемся перазапускать pyCharm, каб ён падхапіў усе навіны
# запускаем сервер фронтэнд првкладання npm run serve
# яна запусціць лакальны сервер унутры папцы public (унутры фронтэнд првкладання)
        #   App running at:
        #   - Local:   http://localhost:8080/
        #   - Network: http://192.168.1.60:8080/
#
#4) цяпер будзем рэдактаваць. у папцы public -- src -- App.vue
#
#
#
#
#