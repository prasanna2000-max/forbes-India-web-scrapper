#creating a table to save the details
#blob datatype is for the image
import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
sql = """
DROP TABLE IF EXISTS table1;
CREATE TABLE table1 (
          
           rank number,
           name text,
           earnings text,
           about text,
           img BLOB

);"""

c.executescript(sql)
conn.commit()
conn.close()