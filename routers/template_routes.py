from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import OfferTemplateCreate, OfferTemplateOut
from models import OfferTemplate
from uuid import uuid4
from datetime import datetime

router = APIRouter(
    prefix="/templates",
    tags=["Offer Templates"]  # ✅ Unique tag
)
@router.post("/", response_model=OfferTemplateOut)
def create_template(template: OfferTemplateCreate, db: Session = Depends(get_db)):
    new_template = OfferTemplate(
        id=uuid4(),
        name=template.name,
        content=template.content,
        is_default=template.is_default,
        company_id=template.company_id,
        created_at=datetime.utcnow()
    )
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    return new_template

@router.get("/", response_model=list[OfferTemplateOut])
def list_templates(db: Session = Depends(get_db)):
    return db.query(OfferTemplate).all()
