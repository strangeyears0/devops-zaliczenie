import time
import os
import psycopg2
from flask import Flask

app = Flask(__name__)


DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            print("Czekam na baze danych...")
            time.sleep(2)
    return None

def init_db():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS visits (count INT)")
        cur.execute("SELECT count FROM visits")
        if cur.fetchone() is None:
            cur.execute("INSERT INTO visits (count) VALUES (0)")
        conn.commit()
        cur.close()
        conn.close()


if DB_HOST:
    init_db()

@app.route('/')
def hello():
    if not DB_HOST:
        return "Aplikacja dziala (tryb bez bazy)"
        
    conn = get_db_connection()
    if not conn:
        return "Blad polaczenia z baza!"
    
    cur = conn.cursor()
    cur.execute("UPDATE visits SET count = count + 1")
    conn.commit()
    
    cur.execute("SELECT count FROM visits")
    count = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    return f"Hello DevOps World! Odwiedziny: {count}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)