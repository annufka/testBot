import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            telegram_id int NOT NULL,
            name text NOT NULL,
            age int NOT NULL,
            sex text NOT NULL,
            PRIMARY KEY (telegram_id)
            );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, telegram_id: int, name: str, age: int, sex: str):
        sql = """
        INSERT INTO Users(telegram_id, name, age, sex) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(int(telegram_id), name, int(age), sex), commit=True)

    def select_user(self, telegram_id: int):
        sql = "SELECT * FROM Users WHERE telegram_id=?"
        return self.execute(sql, parameters=(int(telegram_id),), fetchone=True)

    def edit_param(self, telegram_id: int, param: str, value: str):
        if param == "name":
            sql = """
            UPDATE Users SET name=? WHERE telegram_id=?
            """
        elif param == "age":
            sql = """
                UPDATE Users SET age=? WHERE telegram_id=?
                """
        elif param == "sex":
            sql = """
                UPDATE Users SET sex=? WHERE telegram_id=?
                """
        self.execute(sql, parameters=(int(value) if param == "age" else value, int(telegram_id)), commit=True)


def logger(statement):
    print(f"""
    _____________________________________________________        
    Executing: 
    {statement}
    _____________________________________________________
    """)
