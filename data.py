import sqlite3

class DataBas:
    def __init__(self, dataname):
        self.connect = sqlite3.connect(dataname)
        self.cursor = self.connect.cursor()

    def add_user(self, user_id, first_name, username):
        with self.connect:
            self.cursor.execute("INSERT INTO users(user_id, first_name, username) VALUES(?, ?, ?)", (user_id, first_name, username,))
            self.connect.commit()

    def check_user(self, user_id):
        with self.connect:
            a = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchall()
            return bool(len(a))

    def check_rang(self, user_id):
        with self.connect:
            a = self.cursor.execute("SELECT rang FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
            return a

    def select_all(self, text):
        with self.connect:
            return self.cursor.execute(text).fetchall()
    def select_one(self, text):
        with self.connect:
            return self.cursor.execute(text).fetchone()

    def add_with_bot(self, text):
        with self.connect:
            self.cursor.execute(text)
            self.connect.commit()
