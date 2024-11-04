import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

for i in range(1,11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)",
                   (f'User{i}', f'example{i}@gmail.com', f'{i*10}','1000'))

cursor.execute("UPDATE Users SET balance = ? WHERE (id%2)", (500,) )

for i in range(1,11,3):
    cursor.execute("DELETE FROM Users WHERE id = ?", (f'{i}',))

cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))
users = cursor.fetchall()

for i in range(len(users)):
    print(f' Имя: {users[i][0]} | Почта: {users[i][1]} | Возраст: {users[i][2]} | Баланс: {users[i][3]}')



connection.commit()
connection.close()
