from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/orders", tags=["orders"])


# 创建订单
@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    new_order = models.Order(
        customer_name=order.customer_name,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # 添加订单项
    for item in order.items:
        db_item = models.OrderItem(
            order_id=new_order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity
        )
        db.add(db_item)

    db.commit()
    db.refresh(new_order)
    return new_order


# 获取所有订单
@router.get("/", response_model=List[schemas.Order])
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()
