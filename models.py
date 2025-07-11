from sqlalchemy import Column, String, Boolean, DateTime, Integer, Enum, JSON, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from database import Base

class OfferLetter(Base):
    __tablename__ = "offer_letters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), nullable=False)
    job_id = Column(UUID(as_uuid=True), nullable=False)
    template_id = Column(UUID(as_uuid=True), ForeignKey("offer_templates.id"), nullable=True)
    offer_data = Column(JSON, nullable=False)  # All dynamic values like CTC, DOJ, etc.
    pdf_url = Column(String, nullable=True)

    sign_status = Column(
        Enum("Draft", "Sent", "Viewed", "Signed", "Rejected", "Expired", name="status_enum"),
        default="Draft"
    )
    sent_at = Column(DateTime)
    signed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked = Column(Boolean, default=False)
    version = Column(Integer, default=1)
    created_by = Column(UUID(as_uuid=True), nullable=False)


class OfferTemplate(Base):
    __tablename__ = "offer_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)  # e.g., "Default Template", "TCS Template"
    content = Column(Text, nullable=False)  # Jinja2-based HTML
    is_default = Column(Boolean, default=False)  # Global fallback template
    company_id = Column(UUID(as_uuid=True), nullable=True)  # Null for Talence global templates
    created_at = Column(DateTime, default=datetime.utcnow)
