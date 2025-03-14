
import socket
import json
import os
import urllib.parse
import shutil

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
    """ Загружаем HTML-страницу """
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    path = request_data.split(' ')[1]
    if "new_path=" in request_data:
            try:
                request_body = request_data.split("\r\n\r\n")[1]  
                new_path = request_body.split("=")[1].replace("+", " ")  
                new_path = urllib.parse.unquote(new_path) 
                if update_root(new_path):  
                    print("Директория успешно обновлена!") 
            except Exception as e:
                return HDRS.encode('utf-8') + f"<h1>Ошибка: {str(e)}</h1>".encode('utf-8')
    
    if path.startswith("/download_json"):
            return download_json()
    

    if path.startswith("/shutdown"):
        print("Выключение сервера...")
        os._exit(0) 

    try:
        with open("1lab/templates/main.html", "r", encoding="utf-8") as file:
            response = file.read()
    except FileNotFoundError:
        return HDRS.encode('utf-8') 


    if os.path.exists("structure.json"):  
        with open("structure.json", "r", encoding="utf-8") as structure_file:
            fcc_data = json.load(structure_file)
            pretty_text = format_structure(fcc_data).replace("\n", "<br>")
    else:
        pretty_text = "Файл structure.json отсутствует"

    response = response.replace("{{ fails }}", pretty_text) 
    return HDRS.encode('utf-8') + response.encode('utf-8')

def download_json():
    """ Скачиваем JSON  """
    if os.path.exists("structure.json"):
        with open("structure.json", "r", encoding="utf-8") as file:
            json_data = file.read()
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
    start_server()


