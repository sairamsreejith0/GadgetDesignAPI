from app.database import engine,Base,SessionLocal,get_db
from fastapi import APIRouter,Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import random,uuid
from uuid import UUID
from app.models import Gadget
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from fastapi.encoders import jsonable_encoder
from app.routers.auth import get_current_user
from sqlalchemy import cast,String
router = APIRouter()



def generate_codename(db):
    codenames = ["The Nightingale", "The Kraken", "Phantom", "Shadow Hawk"]
    while True:
        new_codename = f"{random.choice(codenames)}-{str(uuid.uuid4())[:8]}"
        existing = db.query(Gadget).filter(Gadget.name == new_codename).first()
        if not existing:
            return new_codename
    
class GadgetCreate(BaseModel):
    status: Optional[str]=None

class GadgetResponse(BaseModel):
    id: str
    name: str
    status: str
    success_probability: str

class GadgetUpdate(BaseModel):
    name: Optional[str]=None
    status: Optional[str] = None
    decommissioned_at: Optional[datetime] = None 



@router.post("/gadgets", response_model=dict)
def add_gadgets(gadget: GadgetCreate, db: Session = Depends(get_db)):
    try:
        if gadget.status == "":
            gadget.status = "Available"
        elif gadget.status and gadget.status not in ["Available", "Deployed", "Destroyed", "Decommissioned"]:
            raise HTTPException(status_code=400, detail="Invalid status value")

        new_gadget = Gadget(
        id=uuid.uuid4(),
        name=generate_codename(db),
        status=gadget.status
    )
        db.add(new_gadget)
        db.commit()
        db.refresh(new_gadget)
    
        return {
        "message": "Gadget added successfully",
        "id": str(new_gadget.id),
        "name": new_gadget.name,
        "status": new_gadget.status
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))

    
@router.get("/gadgets",response_model=list[GadgetResponse])
def get_gadgets(db:Session=Depends(get_db)):
    gadgets = db.query(Gadget).all()
    gadget_list = []  
    for gadget in gadgets:
        gadget_dict = {
            "id" : str(gadget.id),
            "name": gadget.name,
            "status":gadget.status,
            "success_probability": f"{random.randint(50, 100)}%"
        }
        gadget_list.append(gadget_dict)
    
    return gadget_list
    
@router.get("/gadgets/{id}", response_model=dict)
def get_gadget_id(id: UUID, db: Session = Depends(get_db)):
    gadget = db.query(Gadget).filter(Gadget.id == id).first()
    if not gadget:
        raise HTTPException(status_code=404, detail="Gadget not found")
    
    return {
        "id": str(gadget.id),
        "name": gadget.name,
        "status": gadget.status,
        "success_probability": f"{random.randint(50, 100)}%"
    }

    
@router.delete("/gadgets/{id}")
def remove_gadget(id:UUID,db:Session=Depends(get_db)):
    gadget = db.query(Gadget).filter(Gadget.id==id).first()
    if not gadget:
        raise HTTPException(status_code=404, detail="Gadget not found")

    gadget.status = "Decommissioned"
    gadget.decommissioned_at = datetime.now(timezone.utc)
    db.commit()
    return {"message": f"Gadget {gadget.name} decommissioned"}


@router.patch("/gadgets/{id}")
def update_gadget(id: UUID, gadget_update: GadgetUpdate, db: Session = Depends(get_db)):
    gadget = db.query(Gadget).filter(Gadget.id == id).first()
    if not gadget:
        raise HTTPException(status_code=404, detail="Gadget not found")

    if gadget_update.name is not None:
        gadget.name = gadget_update.name

    if gadget_update.status is not None:
        if gadget_update.status not in ["Available", "Deployed", "Destroyed", "Decommissioned"]:
            raise HTTPException(status_code=400, detail="Invalid status value")
        gadget.status = gadget_update.status

        # If status is changed to "Decommissioned", set decommissioned_at timestamp
        if gadget.status == "Decommissioned":
            gadget.decommissioned_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(gadget)

    return {
        "message": "Gadget updated successfully",
        "updated_gadget": {
            "id": str(gadget.id),
            "name": gadget.name,
            "status": gadget.status,
            "decommissioned_at": gadget.decommissioned_at
        }
    }



@router.post("/gadgets/{id}/self-destruct")
def self_destruct(id: UUID, db: Session = Depends(get_db)):
    gadget = db.query(Gadget).filter(Gadget.id == id).first()
    if not gadget:
        raise HTTPException(status_code=404, detail="Gadget not found")

    confirmation_code = uuid.uuid4().hex.upper()
    return {"message": "Self-destruct initiated", "confirmation_code": confirmation_code}


@router.get("/gadgets-by-status",response_model=list[GadgetResponse])
def get_gadget_status(status:str,db:Session=Depends(get_db)):
    gadgets = db.query(Gadget).filter(cast(Gadget.status, String) == status).all()
    if not gadgets:
        return []
    gadget_list = [] 
    for gadget in gadgets:
        gadget_dict = {
            "id" : str(gadget.id),
            "name": gadget.name,
            "status":gadget.status,
            "success_probability": f"{random.randint(50, 100)}%"
        }
        gadget_list.append(gadget_dict)
    return gadget_list
