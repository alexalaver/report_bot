import sqlite3

class DataBas:
    def __int__(self, dataname):
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
