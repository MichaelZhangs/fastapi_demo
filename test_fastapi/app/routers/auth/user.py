from config.configs import api
from fastapi import APIRouter, Request
import datetime
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.config.database_config import async_session, SessionLocal, engine
from app.crud import crud
from typing import List


router = APIRouter(prefix="/user")


async def request_info(request: Request):
    api.logger.info(f"{request.method} {request.url}")
    try:
        body = await request.json()
        api.logger.debug("request_json: ")
    except:
        try:
            body = await request.body()
            print("body = ", body)
            if len(body) != 0:
                # 有请求体，记录日志
                api.logger.debug(body)
        except:
            # 忽略文件上传类型的数据
            pass


def f():
    print("Hello FastApi .....")


# @router.get("/")
# def read_root():
#     api.logger.info("进入 user 路由")
#     cur_time = datetime.datetime.now()
#     next_time = cur_time + datetime.timedelta(seconds=5)
#     api.scheduler.add_job(func=f, next_run_time=next_time, timezone="Asia/Shanghai")
#     return {"Hello": "World"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# async def get_db():
#     async with async_session() as session:
#         db = session
#     try:
#         yield db
#     finally:
#         await db.close()


@router.post("/create/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print("user_dict = ", schemas.UserCreate.password)
    db_user = crud.get_user_by_email(db, email=user.email)
    print(db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/list/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    print("response_model = ",schemas.User.schema_json())
    print(db_user.to_dict())
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items