import os
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database import Base
from models import OfferTemplate
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# PostgreSQL connection
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(bind=engine)
db: Session = SessionLocal()

# ✅ Seed Default Talence AI Template
default_template_path = "templates/default_offer_template.html"
if os.path.exists(default_template_path):
    with open(default_template_path, "r", encoding="utf-8") as file:
        default_template_html = file.read()

    existing_default = db.query(OfferTemplate).filter_by(is_default=True, company_id=None).first()

    if not existing_default:
        default_template = OfferTemplate(
            id=uuid.uuid4(),
            name="Default Talence AI Offer Template",
            content=default_template_html,
            is_default=True,
            company_id=None,
            created_at=datetime.utcnow()
        )
        db.add(default_template)
        print(f"✅ Talence AI default template seeded with ID: {default_template.id}")
    else:
        print("⚠️ Default Talence AI template already exists. Skipping.")
else:
    print("❌ Default template HTML file not found!")

# ✅ Seed Randstad Template
randstad_template_path = "templates/randstad_template.html"
if os.path.exists(randstad_template_path):
    with open(randstad_template_path, "r", encoding="utf-8") as file:
        randstad_template_html = file.read()

    existing_randstad = db.query(OfferTemplate).filter_by(name="Randstad Default Template").first()

    if not existing_randstad:
        randstad_template = OfferTemplate(
            id=uuid.uuid4(),
            name="Randstad Default Template",
            content=randstad_template_html,
            is_default=False,
            company_id=None,  # Replace with UUID if needed
            created_at=datetime.utcnow()
        )
        db.add(randstad_template)
        print(f"✅ Randstad template seeded with ID: {randstad_template.id}")
    else:
        print("⚠️ Randstad template already exists. Skipping.")
else:
    print("❌ Randstad template HTML file not found!")

# ✅ Finalize
db.commit()
db.close()
