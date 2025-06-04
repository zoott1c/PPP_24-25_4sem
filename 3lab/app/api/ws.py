# app/api/ws.py

from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from jose import JWTError, jwt
from app.auth.auth import SECRET_KEY, ALGORITHM
from app.websocket.manager import manager

import logging

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

@router.websocket("/ws/tasks/")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        logger.warning("WebSocket: отсутствует токен в query-параметрах")
        await websocket.close(code=1008)
        return

    try:
        # Расшифровка JWT токена
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            logger.warning("WebSocket: токен не содержит 'sub'")
            await websocket.close(code=1008)
            return
    except JWTError as e:
        logger.warning(f"WebSocket: ошибка JWT — {e}")
        await websocket.close(code=1008)
        return
    except Exception as e:
        logger.error(f"WebSocket: непредвиденная ошибка — {e}")
        await websocket.close(code=1011)
        return

    # Успешное подключение
    await manager.connect(user_id, websocket)
    logger.info(f"WebSocket: пользователь {user_id} подключен")

    try:
        await websocket.send_json({"status": "CONNECTED", "message": "WebSocket OK"})
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.info(f"WebSocket: пользователь {user_id} отключился")
        manager.disconnect(user_id)
    except Exception as e:
        logger.error(f"WebSocket: ошибка при приеме сообщения — {e}")
        manager.disconnect(user_id)
        await websocket.close(code=1011)
