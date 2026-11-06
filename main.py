from typing import Annotated

from authx import AuthX, AuthXConfig
from fastapi import Depends, FastAPI, Form, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Booking, Hall, Seat, Show, Status, User
from schemas import LoginForm, RegisterForm

app = FastAPI()

config = AuthXConfig(
    JWT_SECRET_KEY='Artem Vadimovich',
    JWT_TOKEN_LOCATION=['cookies'],
)

auth = AuthX(config)

auth.handle_errors(app)

app.mount('/static', StaticFiles(directory='static'), 'static')
templates = Jinja2Templates(directory='templates')

Base.metadata.create_all(bind=engine)


@app.get('/')
def index(request: Request, db: Annotated[Session, Depends(get_db)]):
    shows = db.execute(select(Show)).scalars().all()
    return templates.TemplateResponse(request, 'index.html', {'shows': shows})

@app.get('/register', name='register')
def get_register(request: Request):
    return templates.TemplateResponse(request, 'register.html')

@app.post('/register')
def post_register(
    request: Request,
    form_data: Annotated[RegisterForm, Form()], 
    db: Annotated[Session, Depends(get_db)],
):
    user = db.execute(select(User).where(User.email == form_data.email)).scalars().first()
    if user:
        return templates.TemplateResponse(request, 'register.html', {'error': 'Пользователь с таким email уже существует'})
    
    user = User(
                name=form_data.name,
                surname=form_data.surname,
                email=form_data.email,
                password=form_data.password
            )
    db.add(user)
    db.commit()
    
    token = auth.create_access_token(uid=str(user.id))
    response = RedirectResponse(url='/', status_code=303)
    auth.set_access_cookies(token, response)

    return response



@app.get('/login', name='login')
def get_login(request: Request):
    return templates.TemplateResponse(request, 'login.html')

@app.post('/login', name='login')
def post_login(
    request: Request,
    form_data: Annotated[LoginForm, Form()],
    db: Annotated[Session, Depends(get_db)],
):
    user = db.execute(select(User).where(User.email == form_data.email)).scalars().first()
    if not user:
        return templates.TemplateResponse(request, 'login.html', {'error': 'Пользователь с таким email не найден'})
    if user.password != form_data.password:
        return templates.TemplateResponse(request, 'login.html', {'error': 'Неверный пароль'})
    token = auth.create_access_token(uid=str(user.id))
    response = RedirectResponse(url='/', status_code=303)
    auth.set_access_cookies(token, response)
    return response


@app.post('/logout')
def logout(request: Request, response: Response):
    auth.unset_cookies(response)
    return templates.TemplateResponse(request, 'index.html')

@app.get('/hall/{show_id}', name='show_hall')
def show_hall(request: Request, show_id: int, db: Annotated[Session, Depends(get_db)]):
    show = db.execute(select(Show).where(Show.id == show_id)).scalars().first()
    seats = db.execute(select(Seat).where(Seat.hall_id == show.hall_id)).scalars().all()
    
    return templates.TemplateResponse(request, 'hall.html', {'show': show, 'seats': seats})


@app.post('/booking')