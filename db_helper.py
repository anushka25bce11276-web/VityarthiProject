import sqlite3

class RetailDB:
    def __init__(self):
        self.conn = sqlite3.connect("store_data.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT,
                category TEXT,
                price REAL,
                quantity INTEGER,
                date_added TEXT
            )
        """)
        self.conn.commit()

    def add_item(self, name, category, price, qty, date):
        try:
            self.cursor.execute("INSERT INTO inventory (item_name, category, price, quantity, date_added) VALUES (?, ?, ?, ?, ?)", 
                                (name, category, price, qty, date))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error adding item:", e)
            return False

    def get_all_items(self):
        self.cursor.execute("SELECT * FROM inventory ORDER BY id DESC")
        rows = self.cursor.fetchall()
        return rows

    def delete_item(self, item_id):
        self.cursor.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        self.conn.commit()

    def get_total_stock_value(self):
        self.cursor.execute("SELECT sum(price * quantity) FROM inventory")
        result = self.cursor.fetchone()
        if result[0] is None:
            return 0
        return result[0]

    def close(self):
        self.conn.close()