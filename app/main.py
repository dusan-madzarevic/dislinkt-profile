from datetime import datetime, date
from typing import Union
import uvicorn
from sqlalchemy.ext.declarative import declarative_base
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from fastapi import Request

import models
from dto import UserDTO
from models import User

from users import UserCreate
from userform import UserCreateForm

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = sessionmaker()
local_session = Session(bind=engine)

models.Base.metadata.create_all(bind=engine)

# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods="*",
    allow_headers="*",
)

# app.include_router(auth.router)
# app.include_router(route_users.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/register")
async def register(request: Request):
    req = await request.json()
    print(req)
    user = User()
    user.username = req['username']
    user.email = req['email']
    user.password = req['password']
    user.ime = req['ime']
    user.prezime = req['prezime']
    user.telefon = req['telefon']
    # user.datumRodjenja = datetime.date(req['datumRodjenja'])
    date_time_str = req['datumRodjenja']
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
    user.datumRodjenja = datetime.date(date_time_obj)
    user.pol = req['pol']
    user.role = "reg_user"
    local_session.add(user)
    local_session.commit()

    return {
        "code": "success",
        "message": "registration successful"
    }


# @app.post("/register/")
# async def register(request: Request): #, db: Session = Depends(get_db)):
#     form = UserCreateForm(request)
#     await form.load_data()
#     if await form.is_valid():
#         user = UserCreate(
#             username=form.username, email=form.email, password=form.password
#         )
#         # try:
#         #     user = create_new_user(user=user, db=db)
#         #     return responses.RedirectResponse(
#         #         "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
#         #     )  # default is post request, to use get request added status code 302
#         # except IntegrityError:
#         #     form.__dict__.get("errors").append("Duplicate username or email")
#         #     return templates.TemplateResponse("users/register.html", form.__dict__)
#     return {
#         "code": "success",
#         "message": "registration successful"
#     }


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    uvicorn.run(app, port=8000, host="0.0.0.0")

