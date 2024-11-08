import sqlite3
import products




def initate_db():
    connection = sqlite3.connect('database_utb.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    prods = products.products

    cursor.execute("SELECT SUM(id) FROM Products")
    total = cursor.fetchone()[0]
    if total is None:
        for i in range (1,5):
            cursor.execute("INSERT INTO Products (title, description, price) VALUES (?,?,?)",
                           (f'{prods[i][0]}',f'{prods[i][1]}', f'{i*100} руб.' ))
        connection.commit()
    else:
        pass

    connection.commit()
    connection.close()
####################USERS##########################
    connection = sqlite3.connect('users_utb.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
        ''')

    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('database_utb.db')
    cursor = connection.cursor()
    a = initate_db()
    cursor.execute("SELECT * FROM Products")
    base = cursor.fetchall()
    connection.commit()
    connection.close()
    return base

def add(username, email, age):
    connection = sqlite3.connect('users_utb.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",
                   (f'{username}', f'{email}', f'{age}', f'1000'))
    connection.commit()
    connection.close()

def is_icluded(username):
    connection = sqlite3.connect('users_utb.db')
    cursor = connection.cursor()
    check_user = cursor.execute('SELECT * FROM Users WHERE username=?', (username,))
    if check_user.fetchone() is None:
        connection.close()
        return False
    else:
        connection.close()
        return True


a = initate_db()
#print(is_icluded('Anna'))
b=add('test', 'ex@gmail.com', 20)
a=add('Anna', 'a@ya.ru', 20)
b=add('Bob', 'b@ya.ru', 21)








#print(get_all_products())
