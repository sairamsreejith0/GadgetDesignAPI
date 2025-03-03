from fastapi import FastAPI,Depends
from .routers import auth, gadgets  # Import routers
from .database import Base, engine
from app.routers.auth import get_current_user

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IMF Gadget API", version="1.0")

# Include Authentication & Gadgets Routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(gadgets.router, prefix="/gadgets", tags=["Gadgets"],dependencies=[Depends(get_current_user)])
