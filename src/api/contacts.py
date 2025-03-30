from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.repository.database.db import get_db
from src.repository import contacts
from src.schemas import ContactCreate, ContactUpdate

router = APIRouter(prefix="/contacts", tags=["Contacts"])

@router.post("/", response_model=ContactCreate)
def create(contact: ContactCreate, db: Session = Depends(get_db)):
    try:
        return contacts.create_contact(db, contact)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def read(name: str = None, email: str = None, db: Session = Depends(get_db)):
    return contacts.get_contacts(db, name, email)

@router.get("/{contact_id}")
def read_one(contact_id: int, db: Session = Depends(get_db)):
    contact = contacts.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}")
def update(contact_id: int, contact_update: ContactUpdate, db: Session = Depends(get_db)):
    updated_contact = contacts.update_contact(db, contact_id, contact_update)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

@router.delete("/{contact_id}")
def delete(contact_id: int, db: Session = Depends(get_db)):
    deleted_contact = contacts.delete_contact(db, contact_id)
    if not deleted_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"detail": "Contact deleted"}
