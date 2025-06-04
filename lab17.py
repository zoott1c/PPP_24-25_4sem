import psycopg2

# Параметры подключения к базе данных
db_params = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",         # замените на свой username
    "password": "root",   # замените на свой пароль
    "dbname": "appliance_store_db"  # замените на имя своей БД
}

def connect_to_db():
    """Устанавливает соединение с базой данных и возвращает connection и cursor."""
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        print("Соединение с базой данных установлено.")
        return conn, cur
    except Exception as e:
        print("Ошибка подключения к базе данных:", e)
        return None, None

def close_db(conn, cur):
    """Закрывает соединение и курсор."""
    if cur:
        cur.close()
    if conn:
        conn.close()
        print("Соединение с базой данных закрыто.")

#--------------------------------------------------------------------------------------------------------------------------
# 2
#--------------------------------------------------------------------------------------------------------------------------

def insert_store(address, phone, director, employee_count):
    """Добавляет один магазин."""
    query = """
        INSERT INTO stores (address, phone, director, employee_count)
        VALUES (%s, %s, %s, %s)
        RETURNING store_id
    """
    conn, cur = connect_to_db()
    try:
        cur.execute(query, (address, phone, director, employee_count))
        conn.commit()
        store_id = cur.fetchone()[0]
        print(f"Магазин добавлен с store_id={store_id}")
        return store_id
    except Exception as e:
        print("Ошибка при добавлении магазина:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)


def insert_many_stores(stores_list):
    """
    Добавляет сразу несколько магазинов.
    stores_list — список кортежей (address, phone, director, employee_count)
    """
    query = """
        INSERT INTO stores (address, phone, director, employee_count)
        VALUES (%s, %s, %s, %s)
    """
    conn, cur = connect_to_db()
    try:
        cur.executemany(query, stores_list)
        conn.commit()
        print(f"{cur.rowcount} магазинов добавлено.")
    except Exception as e:
        print("Ошибка при добавлении магазинов:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)

def insert_product(name, brand, weight, price):
    """Добавляет одну запись о товаре."""
    query = """
        INSERT INTO products (name, brand, weight, price)
        VALUES (%s, %s, %s, %s)
        RETURNING product_id
    """
    conn, cur = connect_to_db()
    try:
        cur.execute(query, (name, brand, weight, price))
        conn.commit()
        product_id = cur.fetchone()[0]
        print(f"Товар добавлен с product_id={product_id}")
        return product_id
    except Exception as e:
        print("Ошибка при добавлении товара:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)

def insert_many_products(products_list):
    """
    Добавляет сразу несколько товаров.
    products_list — список кортежей (name, brand, weight, price)
    """
    query = """
        INSERT INTO products (name, brand, weight, price)
        VALUES (%s, %s, %s, %s)
    """
    conn, cur = connect_to_db()
    try:
        cur.executemany(query, products_list)
        conn.commit()
        print(f"{cur.rowcount} товаров добавлено.")
    except Exception as e:
        print("Ошибка при добавлении товаров:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)

def insert_product_in_store(store_id, product_id, quantity):
    """Добавляет одну запись о наличии товара в магазине."""
    query = """
        INSERT INTO products_in_stores (store_id, product_id, quantity)
        VALUES (%s, %s, %s)
        RETURNING id
    """
    conn, cur = connect_to_db()
    try:
        cur.execute(query, (store_id, product_id, quantity))
        conn.commit()
        row_id = cur.fetchone()[0]
        print(f"Запись о наличии добавлена с id={row_id}")
        return row_id
    except Exception as e:
        print("Ошибка при добавлении записи о наличии:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)

def insert_many_products_in_stores(items_list):
    """
    Добавляет сразу несколько записей о наличии.
    items_list — список кортежей (store_id, product_id, quantity)
    """
    query = """
        INSERT INTO products_in_stores (store_id, product_id, quantity)
        VALUES (%s, %s, %s)
    """
    conn, cur = connect_to_db()
    try:
        cur.executemany(query, items_list)
        conn.commit()
        print(f"{cur.rowcount} записей о наличии добавлено.")
    except Exception as e:
        print("Ошибка при добавлении записей о наличии:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)

#--------------------------------------------------------------------------------------------------------------------------
# 3
#--------------------------------------------------------------------------------------------------------------------------

def select_all_stores():
    """Выбирает все магазины."""
    query = "SELECT * FROM stores"
    conn, cur = connect_to_db()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print(row)
        return rows
    except Exception as e:
        print("Ошибка при выборе магазинов:", e)
    finally:
        close_db(conn, cur)


def select_stores_by_address(address):
    """Выбирает магазины по адресу (полное совпадение)."""
    query = "SELECT * FROM stores WHERE address = %s"
    conn, cur = connect_to_db()
    try:
        cur.execute(query, (address,))
        rows = cur.fetchall()
        for row in rows:
            print(row)
        return rows
    except Exception as e:
        print("Ошибка при выборе магазинов по адресу:", e)
    finally:
        close_db(conn, cur)


def select_all_products():
    """Выбирает все товары."""
    query = "SELECT * FROM products"
    conn, cur = connect_to_db()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print(row)
        return rows
    except Exception as e:
        print("Ошибка при выборе товаров:", e)
    finally:
        close_db(conn, cur)


def select_products_by_brand(brand):
    """Выбирает товары по бренду."""
    query = "SELECT * FROM products WHERE brand = %s"
    conn, cur = connect_to_db()
    try:
        cur.execute(query, (brand,))
        rows = cur.fetchall()
        for row in rows:
            print(row)
        return rows
    except Exception as e:
        print("Ошибка при выборе товаров по бренду:", e)
    finally:
        close_db(conn, cur)


def select_all_products_in_stores():
    """Выбирает все записи о наличии товаров в магазинах."""
    query = "SELECT * FROM products_in_stores"
    conn, cur = connect_to_db()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print(row)
        return rows
    except Exception as e:
        print("Ошибка при выборе наличия товаров:", e)
    finally:
        close_db(conn, cur)

def select_products_in_store(store_id):
    """Выбирает все товары, имеющиеся в конкретном магазине."""
    query = "SELECT * FROM products_in_stores WHERE store_id = %s"
    conn, cur = connect_to_db()
    try:
        cur.execute(query, (store_id,))
        rows = cur.fetchall()
        for row in rows:
            print(row)
        return rows
    except Exception as e:
        print("Ошибка при выборе товаров по магазину:", e)
    finally:
        close_db(conn, cur)

def select_products_with_store_info(store_id):
    """
    Выбирает товары, их количество и информацию о магазине по store_id (JOIN).
    """
    query = """
        SELECT s.store_id, s.address, p.product_id, p.name, p.brand, ps.quantity
        FROM products_in_stores ps
        JOIN stores s ON ps.store_id = s.store_id
        JOIN products p ON ps.product_id = p.product_id
        WHERE s.store_id = %s
    """
    conn, cur = connect_to_db()
    try:
        cur.execute(query, (store_id,))
        rows = cur.fetchall()
        for row in rows:
            print(row)
        return rows
    except Exception as e:
        print("Ошибка при выборке с соединением:", e)
    finally:
        close_db(conn, cur)

def select_stores_with_product(product_id):
    """
    Показывает список магазинов, где есть заданный товар (JOIN).
    """
    query = """
        SELECT s.store_id, s.address, p.product_id, p.name, ps.quantity
        FROM products_in_stores ps
        JOIN stores s ON ps.store_id = s.store_id
        JOIN products p ON ps.product_id = p.product_id
        WHERE p.product_id = %s
    """
    conn, cur = connect_to_db()
    try:
        cur.execute(query, (product_id,))
        rows = cur.fetchall()
        for row in rows:
            print(row)
        return rows
    except Exception as e:
        print("Ошибка при выборке магазинов с товаром:", e)
    finally:
        close_db(conn, cur)


#--------------------------------------------------------------------------------------------------------------------------
# 4
#--------------------------------------------------------------------------------------------------------------------------

def update_store(store_id, address=None, phone=None, director=None, employee_count=None):
    """
    Обновляет поля магазина по его store_id.
    Только те поля, которые переданы не None.
    """
    fields = []
    values = []
    if address is not None:
        fields.append("address = %s")
        values.append(address)
    if phone is not None:
        fields.append("phone = %s")
        values.append(phone)
    if director is not None:
        fields.append("director = %s")
        values.append(director)
    if employee_count is not None:
        fields.append("employee_count = %s")
        values.append(employee_count)
    if not fields:
        print("Нет данных для обновления.")
        return

    values.append(store_id)
    query = f"UPDATE stores SET {', '.join(fields)} WHERE store_id = %s"
    conn, cur = connect_to_db()
    try:
        cur.execute(query, tuple(values))
        conn.commit()
        print(f"Магазин с id={store_id} обновлён. Изменено строк: {cur.rowcount}")
    except Exception as e:
        print("Ошибка при обновлении магазина:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)

def update_product(product_id, name=None, brand=None, weight=None, price=None):
    """
    Обновляет поля товара по product_id.
    Только те поля, которые переданы не None.
    """
    fields = []
    values = []
    if name is not None:
        fields.append("name = %s")
        values.append(name)
    if brand is not None:
        fields.append("brand = %s")
        values.append(brand)
    if weight is not None:
        fields.append("weight = %s")
        values.append(weight)
    if price is not None:
        fields.append("price = %s")
        values.append(price)
    if not fields:
        print("Нет данных для обновления.")
        return

    values.append(product_id)
    query = f"UPDATE products SET {', '.join(fields)} WHERE product_id = %s"
    conn, cur = connect_to_db()
    try:
        cur.execute(query, tuple(values))
        conn.commit()
        print(f"Товар с id={product_id} обновлён. Изменено строк: {cur.rowcount}")
    except Exception as e:
        print("Ошибка при обновлении товара:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)

def update_product_in_store(row_id, store_id=None, product_id=None, quantity=None):
    """
    Обновляет поля записи о наличии товара по id.
    Только те поля, которые переданы не None.
    """
    fields = []
    values = []
    if store_id is not None:
        fields.append("store_id = %s")
        values.append(store_id)
    if product_id is not None:
        fields.append("product_id = %s")
        values.append(product_id)
    if quantity is not None:
        fields.append("quantity = %s")
        values.append(quantity)
    if not fields:
        print("Нет данных для обновления.")
        return

    values.append(row_id)
    query = f"UPDATE products_in_stores SET {', '.join(fields)} WHERE id = %s"
    conn, cur = connect_to_db()
    try:
        cur.execute(query, tuple(values))
        conn.commit()
        print(f"Запись с id={row_id} обновлена. Изменено строк: {cur.rowcount}")
    except Exception as e:
        print("Ошибка при обновлении наличия товара:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)


#--------------------------------------------------------------------------------------------------------------------------
# 5
#--------------------------------------------------------------------------------------------------------------------------

def delete_store_by_id(store_id):
    """Удаляет магазин по store_id (и все связанные записи о наличии товаров)."""
    query = "DELETE FROM stores WHERE store_id = %s"
    conn, cur = connect_to_db()
    try:
        cur.execute(query, (store_id,))
        conn.commit()
        print(f"Магазин с id={store_id} удалён. Строк удалено: {cur.rowcount}")
    except Exception as e:
        print("Ошибка при удалении магазина:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)

def delete_all_stores():
    """Удаляет все магазины (и все связанные записи о наличии товаров)."""
    query = "DELETE FROM stores"
    conn, cur = connect_to_db()
    try:
        cur.execute(query)
        conn.commit()
        print("Все магазины удалены.")
    except Exception as e:
        print("Ошибка при удалении всех магазинов:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)

def delete_product_by_id(product_id):
    """Удаляет товар по product_id (и все связанные записи о наличии)."""
    query = "DELETE FROM products WHERE product_id = %s"
    conn, cur = connect_to_db()
    try:
        cur.execute(query, (product_id,))
        conn.commit()
        print(f"Товар с id={product_id} удалён. Строк удалено: {cur.rowcount}")
    except Exception as e:
        print("Ошибка при удалении товара:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)

def delete_all_products():
    """Удаляет все товары (и все связанные записи о наличии)."""
    query = "DELETE FROM products"
    conn, cur = connect_to_db()
    try:
        cur.execute(query)
        conn.commit()
        print("Все товары удалены.")
    except Exception as e:
        print("Ошибка при удалении всех товаров:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)

def delete_product_in_store_by_id(row_id):
    """Удаляет запись о наличии товара по id."""
    query = "DELETE FROM products_in_stores WHERE id = %s"
    conn, cur = connect_to_db()
    try:
        cur.execute(query, (row_id,))
        conn.commit()
        print(f"Запись с id={row_id} удалена. Строк удалено: {cur.rowcount}")
    except Exception as e:
        print("Ошибка при удалении записи о наличии:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)

def delete_all_products_in_stores():
    """Удаляет все записи о наличии товаров."""
    query = "DELETE FROM products_in_stores"
    conn, cur = connect_to_db()
    try:
        cur.execute(query)
        conn.commit()
        print("Все записи о наличии товаров удалены.")
    except Exception as e:
        print("Ошибка при удалении всех записей о наличии:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)

#--------------------------------------------------------------------------------------------------------------------------
# 6
#--------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------------------
# 
#--------------------------------------------------------------------------------------------------------------------------

def create_tables():
    """Создаёт все таблицы в базе данных."""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS stores (
            store_id SERIAL PRIMARY KEY,
            address VARCHAR(255) NOT NULL,
            phone VARCHAR(20),
            director VARCHAR(100),
            employee_count INTEGER
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            brand VARCHAR(50),
            weight NUMERIC(10, 2),
            price NUMERIC(15, 2)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS products_in_stores (
            id SERIAL PRIMARY KEY,
            store_id INTEGER NOT NULL REFERENCES stores(store_id) ON DELETE CASCADE,
            product_id INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
            quantity INTEGER NOT NULL
        )
        """
    )
    conn, cur = connect_to_db()
    try:
        for command in commands:
            cur.execute(command)
        conn.commit()
        print("Таблицы успешно созданы (или уже существуют).")
    except Exception as e:
        print("Ошибка при создании таблиц:", e)
        conn.rollback()
    finally:
        close_db(conn, cur)


# Тест подключения
if __name__ == "__main__":
    print("=== 1. СОЗДАНИЕ ТАБЛИЦ ===")
    create_tables()

    print("\n=== 2. ДОБАВЛЕНИЕ ДАННЫХ ===")
    store_id_1 = insert_store("ул. Пушкина, 1", "+7-900-000-11-22", "Пушкин А.С.", 7)
    store_id_2 = insert_store("ул. Лермонтова, 3", "+7-900-000-22-33", "Лермонтов М.Ю.", 5)
    insert_many_stores([
        ("пр. Гагарина, 8", "+7-900-123-45-67", "Гагарин Ю.А.", 10)
    ])

    product_id_1 = insert_product("Стиральная машина", "LG", 60.0, 35000)
    product_id_2 = insert_product("Холодильник", "Samsung", 80.5, 42000)
    insert_many_products([
        ("Телевизор", "Sony", 15.0, 28000)
    ])

    insert_product_in_store(store_id_1, product_id_1, 5)
    insert_product_in_store(store_id_2, product_id_1, 2)
    insert_many_products_in_stores([
        (store_id_1, product_id_2, 4),
        (store_id_2, product_id_2, 7)
    ])

    print("\n=== 3. ВЫБОРКИ ===")
    print("Все магазины:")
    select_all_stores()
    print("Магазины по адресу 'ул. Пушкина, 1':")
    select_stores_by_address("ул. Пушкина, 1")

    print("\nВсе товары:")
    select_all_products()
    print("Товары бренда LG:")
    select_products_by_brand("LG")

    print("\nВсе записи о наличии товаров:")
    select_all_products_in_stores()
    print("Товары в магазине 1:")
    select_products_in_store(store_id_1)

    print("\nВсе товары с информацией о магазине (JOIN):")
    select_products_with_store_info(store_id_1)

    print("\n=== 4. ОБНОВЛЕНИЯ ===")
    update_store(store_id_1, address="ул. Новая, 77")
    update_product(product_id_1, price=37000)
    # Найдите id нужной записи о наличии, например 1, если это первая строка
    update_product_in_store(1, quantity=10)

    print("\n=== 5. УДАЛЕНИЕ ДАННЫХ ===")
    delete_product_in_store_by_id(1)
    delete_store_by_id(store_id_2)
    delete_all_products_in_stores()
    delete_all_products()
    delete_all_stores()

    print("\n=== КОНЕЦ ДЕМОНСТРАЦИИ ===")





