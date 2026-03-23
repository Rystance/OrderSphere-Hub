from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..deps import get_db, get_admin_user

router = APIRouter(prefix="/admin/orders", tags=["admin-orders"])


@router.get("/", response_model=List[schemas.Order])
def get_all_orders(db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    return db.query(models.Order).all()


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    db.delete(order)
    db.commit()
    return {"msg": "删除成功"}
