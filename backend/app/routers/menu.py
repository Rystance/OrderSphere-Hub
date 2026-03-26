from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.deps import get_db

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("/", response_model=List[schemas.MenuItem])
def get_menu(db: Session = Depends(get_db)):
    return db.query(models.MenuItem).all()
