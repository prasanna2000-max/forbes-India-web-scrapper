import sqlite3
conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute("select * from table1") 
  
  
print(cur.fetchall() )
conn.commit()
conn.close()