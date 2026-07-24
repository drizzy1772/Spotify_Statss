





from fastapi import APIRouter
from celery.result import AsyncResult
from app.celery_app import celery_app

router = APIRouter(tags=["Etl Pipeline"])

@router.get("/sync-spotify/{task_id}")
async def get_task_status(task_id: str):
    
    res = AsyncResult(task_id, app=celery_app)
    
    task_status = res.status
    
    return {
        "task_id": task_id,
        "status": task_status
    }