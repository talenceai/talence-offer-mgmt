from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from uuid import UUID
from datetime import datetime
from enum import Enum

# -------------------------
# ✉️ Offer Letter Section
# -------------------------

class SignStatusEnum(str, Enum):
    draft = "Draft"
    sent = "Sent"
    viewed = "Viewed"
    signed = "Signed"
    rejected = "Rejected"
    expired = "Expired"

# ✅ For creating a new offer
class OfferLetterCreate(BaseModel):
    candidate_id: UUID
    job_id: UUID
    template_id: Optional[UUID] = None
    offer_data: Dict[str, str]  # e.g. {"CTC": "10 LPA", "DOJ": "2025-08-01"}
    created_by: UUID

# ✅ For responding with offer details
class OfferLetterResponse(BaseModel):
    id: UUID
    candidate_id: UUID
    job_id: UUID
    template_id: Optional[UUID]
    offer_data: Dict[str, str]
    pdf_url: Optional[str]
    sign_status: SignStatusEnum
    sent_at: Optional[datetime]
    signed_at: Optional[datetime]
    created_at: datetime
    revoked: bool
    version: int
    created_by: UUID

    class Config:
        orm_mode = True  # Allows SQLAlchemy → Pydantic conversion


# -------------------------
# 📄 Offer Template Section
# -------------------------

class OfferTemplateCreate(BaseModel):
    name: str
    content: str  # Jinja2 HTML template string
    is_default: Optional[bool] = False
    company_id: Optional[UUID] = None

class OfferTemplateOut(OfferTemplateCreate):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True  # For Pydantic v2 compatibility (instead of orm_mode)
