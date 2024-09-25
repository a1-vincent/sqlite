import sqlite3

#connect to or create sqlite database
conn = sqlite3.connect('members.db')
cur = conn.cursor()

#display data
member_data = cur.execute("SELECT * members ORDER BY ln")
for row in member_data:
    print(row)

#Closing time
cur.close()
conn.close()
