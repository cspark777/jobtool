import sqlite3

connection = sqlite3.connect('DB.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO extract_job (WEB_CLASS_NUM, ATTR_NM) VALUES (?, ?)",
            (110001, 'Ink Color')
            )

cur.execute("INSERT INTO extract_job (WEB_CLASS_NUM, ATTR_NM) VALUES (?, ?)",
            (110001, 'Pen Type')
            )

connection.commit()
connection.close()