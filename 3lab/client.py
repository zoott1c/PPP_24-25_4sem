import asyncio
import json
import websockets
import requests

API_URL = "http://127.0.0.1:8000"
WS_URL = "ws://127.0.0.1:8000/ws/tasks/"

async def ws_listener(token):
    url = f"{WS_URL}?token={token}"
    print(">>> Токен для WebSocket:", token)
    print(">>> Полный URL:", url)
    from jose import jwt  # совместимо с сервером
 

    
    SECRET_KEY = "SECRET"
    ALGORITHM = "HS256"

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(">>> JWT payload:", decoded)

    async with websockets.connect(url) as websocket:
        print("Соединение с WebSocket установлено.")
        while True:
            msg = await websocket.recv()
            print("Получено сообщение:", msg)

def authenticate(email, password):
    response = requests.post(
        f"{API_URL}/login/",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()
    return response.json()["access_token"]

def send_tsp_task(token, user_email):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{API_URL}/tsp/run-task/",
        json={"user_id": user_email},
        headers=headers,
    )
    response.raise_for_status()
    task_id = response.json()["task_id"]
    print("Задача отправлена:", task_id)

def main():
    email = input("Email: ").strip()
    password = input("Пароль: ").strip()
    token = authenticate(email, password)
    input("Введите список точек (например: 1,2,3,4): ")

    # Запускаем WebSocket слушатель в фоне и отправляем задачу
    async def run_both():
        task = asyncio.create_task(ws_listener(token))
        await asyncio.sleep(1)  # чуть-чуть подождать, чтобы WebSocket точно подключился
        send_tsp_task(token, email)
        await task  # ждать WebSocket бесконечно

    asyncio.run(run_both())



if __name__ == "__main__":
    main()
