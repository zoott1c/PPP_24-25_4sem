
import socket
import json
import os
import urllib.parse
import shutil
import threading


user_socket = None  # клиент user подключится к порту 3001



def listen_user_trigger():
    """Ожидает подключения клиента-user на втором порту"""
    global user_socket
    user_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    user_server.bind(('127.0.0.1', 3001))
    user_server.listen(1)
    print("Ожидаем подключения user на порту 3001...")
    user_socket, addr = user_server.accept()
    print("✅ User подключился:", addr)


def start_server():
    """Основное тело сервера"""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1',2001))

        server.listen(4)
        while True:
            print('Worcing ...')
            client_socket, addeess = server.accept()

            data = client_socket.recv(1024).decode('utf-8')

            #content = json.dumps(fcc_data).encode('utf-8')
            content = load_page(data)
            client_socket.send(content)
            client_socket.shutdown(socket.SHUT_WR)
            client_socket.close()
    except KeyboardInterrupt:
        server.close()
        print('hi')


def recursive_scan(path):
    """Созжания JSON"""
    structure = {'path': path, 'files': [], 'dirs': []}
    try:
        for entry in os.scandir(path):
            if entry.is_dir():
                structure['dirs'].append(recursive_scan(entry.path))
            else:
                structure['files'].append(entry.name)
    except PermissionError:
        pass 
    return structure

#def json_to_xml(json_file, xml_file):
    #with open(json_file, "r", encoding="utf-8") as f:
        #data = json.load(f)
    #xml_data = dicttoxml.dicttoxml(data, custom_root="root", attr_type=False)  
    #with open(xml_file, "wb") as f:
        #f.write(xml_data) 


def format_structure(data, indent=0):
    """ Форматирует структуру файлов и папок в красивый текст """
    result = ""
    prefix = " " * (indent * 4)  # Отступы для дерева

    # Добавляем путь текущей директории
    result += f"{prefix}📂 {data['path']}\n"

    # Выводим файлы в текущей директории
    for file in data.get("files", []):
        result += f"{prefix}  📄 {file}\n"

    # Рекурсивно обрабатываем вложенные папки
    for subdir in data.get("dirs", []):
        result += format_structure(subdir, indent + 1)

    return result

JSON_PATH = os.path.join(os.getcwd(), "structure.json")

def update_root(new_path):
    """ Меняет корневую директорию удаляет JSON и создаёт новый """
    print(f"Получен новый путь: {new_path}")  

    if os.path.exists(new_path) and os.path.isdir(new_path): 
        print(f"Меняем директорию на: {new_path}")  

        
        if os.path.exists(JSON_PATH):  
            try:
                os.remove(JSON_PATH)  
                print("Файл structure.json удалён.")
            except PermissionError:
                print("Ошибка: нет прав на удаление structure.json. Пробуем удалить через shutil.")
                shutil.rmtree(JSON_PATH, ignore_errors=True)  

        structure = recursive_scan(new_path)  

        with open('structure.json', 'w', encoding='utf-8') as f:
            json.dump(structure, f, ensure_ascii=False, indent=4)
            print("Создан новый structure.json.")  

        return True
    return False


def load_page(request_data):
    """Загружает HTML-страницу или обрабатывает спец-запросы"""
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'

    try:
        path = request_data.split(' ')[1]
    except IndexError:
        return HDRS.encode('utf-8') 

    if "new_path=" in request_data:
        try:
            request_body = request_data.split("\r\n\r\n")[1]  
            new_path = urllib.parse.unquote(request_body.split("=")[1].replace("+", " "))
            update_root(new_path)
        except Exception as e:
            return HDRS.encode('utf-8') + f"<h1>Ошибка: {str(e)}</h1>".encode('utf-8')

    if path.startswith("/download_json"):
        return download_json()

    if path.startswith("/shutdown"):
        os._exit(0)

    if path == "/" or path.endswith(".html"):
        try:
            html_path = os.path.join(os.path.dirname(__file__), "templates", "main.html")
            with open(html_path, "r", encoding="utf-8") as file:
                response = file.read()
        except FileNotFoundError:
            return HDRS.encode('utf-8') 

        if os.path.exists("structure.json"):
            with open("structure.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                pretty_text = format_structure(data).replace("\n", "<br>")
        else:
            pretty_text = "Файл structure.json отсутствует"

        response = response.replace("{{ fails }}", pretty_text)
        return HDRS.encode('utf-8') + response.encode('utf-8')

    return 'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n\r\n<h1>Страница не найдена</h1>'.encode('utf-8')


def download_json():
    """ Отдаёт JSON и уведомляет user-клиента """
    global user_socket
    if os.path.exists("structure.json"):
        with open("structure.json", "r", encoding="utf-8") as file:
            json_data = file.read()

        # отправка сигнала user-клиенту
        if user_socket:
            try:
                user_socket.sendall(b"download")
                print("📤 Сигнал отправлен user-клиенту")
            except Exception as e:
                print("⚠️ Не удалось отправить сигнал user:", e)

        HDRS = 'HTTP/1.1 200 OK\r\nContent-Disposition: attachment; filename="structure.json"\r\nContent-Type: application/json\r\n\r\n'
        return HDRS.encode('utf-8') + json_data.encode('utf-8')

    return 'HTTP/1.1 404 NOT FOUND\r\n\r\nФайл не найден'.encode('utf-8')



if __name__ == "__main__":
    #json_to_xml("structure.json", "structure.xml")
    root = os.getcwd()
    structure = recursive_scan(root)
    with open('structure.json', 'w', encoding='utf-8') as f:
        json.dump(structure, f, ensure_ascii=False, indent=4)
    print("Перейдите в http://127.0.0.1:2001/main.html")
    threading.Thread(target=listen_user_trigger, daemon=True).start()
    start_server()