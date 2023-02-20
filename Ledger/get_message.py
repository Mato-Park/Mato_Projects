import psycopg2
from imessage_reader import fetch_data
from os.path import expanduser
import sys
import sqlite3

def fetch_db_data(db, query):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(query)

        return cursor.fetchall()
    except Exception as e:
        sys.exit("Error reading the database: %s" %e)

db_path = expanduser("~") + "/Library/Messages/chat.db"
# 2일 전 문자 데이터 수신, 몇일 전 선택할 수 있게끔 해야할 듯
query = """SELECT text, handle.id, datetime((date / 1000000000) + 978307200, 'unixepoch', 'localtime'),
handle.service, message.destination_caller_id, message.is_from_me, date((date/1000000000)+978307200, 'unixepoch', 'localtime')
FROM message JOIN handle ON message.handle_id = handle.ROWID
WHERE handle.id == '+8215447200' and message.is_from_me == 0 and 
date((date/1000000000)+978307200, 'unixepoch', 'localtime') >= date('now', 'localtime', '-5 days')
ORDER BY date asc"""

rval = fetch_db_data(db_path, query)

db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
cursor = db.cursor()

for i in rval:
    try:
        number = i[1]
        text_original = i[0]
        date = i[6]
        time = i[0].split(" ")[3]
        ammounts = int(i[0].split(" ")[4][:-1].replace(',', ''))
        place = i[0].split(" ")[5]
        query = f"""INSERT INTO message.text_message (number, text_original, date, time, ammounts, place) 
                    VALUES('{number}', '{text_original}', '{date}', '{time}', {ammounts}, '{place}')
                    ON CONFLICT (TEXT_ORIGINAL)
                    DO NOTHING;"""
        cursor.execute(query)
        cursor.execute("COMMIT")
        print("Insert Sucess!! ======================")
    except Exception as e:
        print(e)