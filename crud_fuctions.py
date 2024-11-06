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

def get_all_products():
    connection = sqlite3.connect('database_utb.db')
    cursor = connection.cursor()
    a = initate_db()
    cursor.execute("SELECT * FROM Products")
    base = cursor.fetchall()
    connection.commit()
    connection.close()
    return base






#print(get_all_products())
