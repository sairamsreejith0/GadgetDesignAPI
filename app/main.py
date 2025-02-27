from fastapi import FastAPI
from .routers import auth, gadgets  # Import routers
from .database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IMF Gadget API", version="1.0")

# Include Authentication & Gadgets Routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(gadgets.router, prefix="/gadgets", tags=["Gadgets"])
