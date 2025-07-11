from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from routers.offer_routes import router as offer_router
from routers.template_routes import router as template_router  # ✅ New route

# Auto-create all tables at startup
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Talence AI Offer Management",
    description="APIs for offer letter creation, PDF generation, eSign, and template management.",
    version="1.0.0"
)

# Include routers
app.include_router(offer_router, prefix="/offers", tags=["Offer Letters"])
app.include_router(template_router, prefix="/templates", tags=["Offer Templates"])  # ✅ New

# Root test route
@app.get("/")
def root():
    return {"message": "🎉 Talence AI Offer Management API is running!"}

# Serve static PDF files
app.mount("/static", StaticFiles(directory="static"), name="static")
