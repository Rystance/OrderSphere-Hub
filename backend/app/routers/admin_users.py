from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.deps import get_db, get_admin_user

router = APIRouter(prefix="/admin/users", tags=["admin-users"])


class UserSimple(schemas.User):
    pass


router = APIRouter(prefix="/admin/users", tags=["admin-users"])


@router.get("/", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    return db.query(models.User).all()


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    db.delete(user)
    db.commit()
    return {"msg": "删除成功"}


@router.post("/{user_id}/make_admin")
def make_admin(user_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    user.is_admin = True
    db.commit()
    return {"msg": "已设为管理员"}
