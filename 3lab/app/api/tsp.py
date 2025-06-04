# app/api/tsp.py

from fastapi import APIRouter, Request
from app.celery.tasks import long_task

router = APIRouter()

@router.post("/run-task/")
async def run_task(request: Request):
    body = await request.json()
    user_id = body.get("user_id")

    task = long_task.apply_async(args=[user_id])
    return {"task_id": task.id}
