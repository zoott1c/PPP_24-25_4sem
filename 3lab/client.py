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

    async with websockets.connect(url) as websocket:
        print("Соединение с WebSocket установлено.")
        while True:
            msg = await websocket.recv()
            # Проверим, если это строка, то парсим её в JSON
            try:
                msg = json.loads(msg)  # Преобразуем строку в JSON, если это строка
            except json.JSONDecodeError:
                print(f"Ошибка декодирования JSON: {msg}")
                continue

            print("Получено сообщение:", msg)

            # Обработка сообщений от сервера
            if "status" in msg:
                if msg["status"] == "CONNECTED":
                    print(f"Соединение установлено: {msg['message']}")
                elif msg["status"] == "TASK_STARTED":
                    print(f"Задача начала выполнение. Task ID: {msg['task_id']}")
                elif msg["status"] == "COMPLETED":
                    print(f"Задача завершена. Путь: {msg['path']}, Общая дистанция: {msg['total_distance']}")

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

    async def run_both():
        task = asyncio.create_task(ws_listener(token))
        await asyncio.sleep(1)  
        send_tsp_task(token, email)
        await task  

    asyncio.run(run_both())

if __name__ == "__main__":
    main()
