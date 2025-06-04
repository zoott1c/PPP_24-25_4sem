# app/celery/tasks.py

from app.celery.celery_config import app as celery_app
from app.websocket.manager import manager
import time
import asyncio

@celery_app.task(bind=True)
def long_task(self, user_id: str):
    task_id = self.request.id

    # STARTED
    asyncio.run(manager.send_to_user(user_id, {
        "status": "STARTED",
        "task_id": task_id,
        "message": "Задача запущена"
    }))

    # PROGRESS
    for progress in range(0, 101, 25):
        time.sleep(1)
        asyncio.run(manager.send_to_user(user_id, {
            "status": "PROGRESS",
            "task_id": task_id,
            "progress": progress
        }))

    # COMPLETED
    result = {
        "status": "COMPLETED",
        "task_id": task_id,
        "path": [1, 2, 3, 4, 1],
        "total_distance": 10
    }
    asyncio.run(manager.send_to_user(user_id, result))
    return result
