from http.server import HTTPServer, BaseHTTPRequestHandler
import psycopg2  # Библиотека для связи с базой PostgreSQL
import time

# Функция для подключения к базе данных
def get_db_connection():
    # Мы указываем host="db" — это имя нашего контейнера с базой. 
    # Docker сам поймет, что "db" — это соседний контейнер в сети.
    conn = psycopg2.connect(
        host="db",
        database="mydb",
        user="postgres",
        password="mysecretpassword"
    )
    return conn

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Подключаемся к базе и создаем таблицу (если ее еще нет)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, time VARCHAR(50));")
        
        # 2. Записываем текущее время визита в базу
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO visits (time) VALUES (%s);", (now,))
        conn.commit()
        
        # 3. Считаем, сколько всего визитов было
        cur.execute("SELECT COUNT(*) FROM visits;")
        count = cur.fetchone()[0]
        
        # 4. Отправляем ответ в браузер
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        text = f"<h1>Privet! Vizitov vsego: {count}</h1><p>Posledniy raz: {now}</p>"
        self.wfile.write(text.encode('utf-8'))
        
        # Закрываем соединение
        cur.close()
        conn.close()

server = HTTPServer(('0.0.0.0', 8000), Handler)
print("Server started on port 8000")
server.serve_forever()
