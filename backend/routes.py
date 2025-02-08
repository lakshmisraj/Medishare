from fastapi import APIRouter
from database import collection
from models import Record

router = APIRouter()

@router.get("/api/records")
async def get_records():
    records = list(collection.find({}, {"_id": 0}))  # Exclude `_id`
    return records

@router.post("/api/records/add")
async def add_record(record: Record):
    collection.insert_one(record.dict())
    return {"message": "Record added successfully!"}