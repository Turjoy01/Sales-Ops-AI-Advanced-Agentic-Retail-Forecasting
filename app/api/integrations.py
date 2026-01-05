"""
Salesforce Integration API Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.salesforce_service import salesforce_service

router = APIRouter(prefix="/api/v1/integrations/salesforce", tags=["Integrations"])

class SyncRequest(BaseModel):
    start_date: str
    end_date: str

class TaskRequest(BaseModel):
    subject: str
    description: str
    priority: str
    due_date: str

@router.post("/sync")
async def sync_salesforce(request: SyncRequest):
    """Trigger Salesforce Data Sync"""
    try:
        return salesforce_service.sync_opportunities(request.start_date, request.end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-task")
async def create_salesforce_task(request: TaskRequest):
    """Create a task in Salesforce"""
    try:
        return salesforce_service.create_task(request.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
