import pyodbc


def get_connection():
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=F;"      # если нужно — поменяй имя сервера
        "DATABASE=STO_DB;"          # имя твоей БД
        "Trusted_Connection=yes;"
    )
    return conn


def init_tables():   # ← вот здесь обязательно двоеточие
    try:
        conn = get_connection()
        conn.close()
        print("Подключение к БД успешно")
    except Exception as e:
        print("Ошибка подключения:", e)
