from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
import crud
import schemas

router = APIRouter()  # ✅ Remove prefix and tags

# ✅ Create a new offer
@router.post("/", response_model=schemas.OfferLetterResponse)
def create_offer(offer: schemas.OfferLetterCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_offer_letter(db=db, offer=offer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Get offer by ID
@router.get("/{offer_id}", response_model=schemas.OfferLetterResponse)
def read_offer(offer_id: UUID, db: Session = Depends(get_db)):
    db_offer = crud.get_offer_letter_by_id(db, offer_id)
    if db_offer is None:
        raise HTTPException(status_code=404, detail="Offer not found")
    return db_offer

# ✅ List all offers
@router.get("/", response_model=list[schemas.OfferLetterResponse])
def list_offers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_offer_letters(db, skip=skip, limit=limit)
