import sqlite3

#init some base
class DataBase:
    def __init__(self, name_base):
        self.name_base = name_base
        self.conn = sqlite3.connect(name_base)
        self.cur = self.conn.cursor()

    def delete_where_id(self):
        pass

    def create_base(self, table, key):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table} ({key} TEXT PRIMARY KEY)")
        self.conn.commit()
        print("Created")

    def insert_data(self, table, data):
        self.cur.execute(f"INSERT INTO {table} VALUES (?)", (data,))
        self.conn.commit()
        print("Inserted")

    def select_data_all(self, table):
        self.cur.execute(f"SELECT * from {table}")
        self.conn.commit()
        return self.cur.fetchall()