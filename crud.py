from sqlalchemy.orm import Session
from models import OfferLetter, OfferTemplate
from schemas import OfferLetterCreate
from uuid import uuid4
from datetime import datetime, timezone
from utils.pdf_generator import generate_offer_pdf


# ✅ Create a new offer letter
def create_offer_letter(db: Session, offer: OfferLetterCreate):
    # Step 1: Use custom template or fallback to default
    if offer.template_id:
        template = db.query(OfferTemplate).filter(OfferTemplate.id == offer.template_id).first()
    else:
        template = db.query(OfferTemplate).filter(OfferTemplate.is_default == True).first()

    if not template:
        raise Exception("❌ No offer template found. Seed a default template first.")

    # Step 2: Generate offer letter PDF using the HTML template + dynamic data
    pdf_url = generate_offer_pdf(
        template_html=template.content,
        offer_data=offer.offer_data,
        candidate_id=offer.candidate_id,
        job_id=offer.job_id
    )

    # Step 3: Persist in database
    new_offer = OfferLetter(
        id=uuid4(),
        candidate_id=offer.candidate_id,
        job_id=offer.job_id,
        template_id=template.id,
        offer_data=offer.offer_data,
        created_by=offer.created_by,
        created_at=datetime.now(timezone.utc),
        version=1,
        sign_status="Draft",
        revoked=False,
        pdf_url=pdf_url
    )

    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return new_offer


# ✅ Fetch an offer letter by its UUID
def get_offer_letter_by_id(db: Session, offer_id: str):
    return db.query(OfferLetter).filter(OfferLetter.id == offer_id).first()


# ✅ List all offer letters (paginated)
def get_all_offer_letters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(OfferLetter).offset(skip).limit(limit).all()
