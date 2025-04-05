import socket
import re

def wait_for_trigger():
    """Ожидает сигнал от сервера на порту 3001"""
    host = '127.0.0.1'
    port = 3001

    print("🔌 Подключение к серверу (порт 3001)...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as trigger_sock:
            trigger_sock.connect((host, port))
            print("⏳ Ожидание сигнала от сервера...")
            data = trigger_sock.recv(1024)
            if data == b"download":
                print("📥 Получен сигнал на загрузку JSON")
                download_json()
            else:
                print("⚠️ Получен неизвестный сигнал:", data)
    except Exception as e:
        print("❌ Ошибка при ожидании сигнала:", e)

def download_json():
    """Подключается к серверу и получает JSON-файл с проверками"""
    host = '127.0.0.1'
    port = 2001
    request = "GET /download_json HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall(request.encode('utf-8'))

            received_data = b""
            chunk_count = 0

            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                chunk_count += 1
                received_data += chunk

        header_end = received_data.find(b"\r\n\r\n")
        if header_end == -1:
            print("⚠️ Некорректный HTTP-ответ (нет заголовков)")
            return

        headers = received_data[:header_end].decode('utf-8', errors='ignore')
        body = received_data[header_end + 4:]

        # Извлекаем имя файла из заголовков
        match = re.search(r'filename="([^"]+)"', headers)
        filename = match.group(1) if match else "неизвестно"

        # Проверка целостности (начало и конец)
        valid_start = body.strip().startswith(b"{")
        valid_end = body.strip().endswith(b"}")

        print("🧾 Получен файл:", filename)
        print("📦 Размер файла:", len(body), "байт")
        print("📶 Пакетов (recv):", chunk_count)

        if valid_start and valid_end:
            print("✅ JSON корректен по структуре (начало и конец)")
        else:
            print("⚠️ Возможно повреждение файла: неправильная структура")

    except Exception as e:
        print("❌ Ошибка при получении JSON:", e)

if __name__ == "__main__":
    wait_for_trigger()
