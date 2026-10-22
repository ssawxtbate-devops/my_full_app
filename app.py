from http.server import HTTPServer, BaseHTTPRequestHandler
import psycopg2
import time

def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="mydb",
        user="postgres",
        password="mysecretpassword"
    )
    return conn

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, time VARCHAR(50));")
        
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO visits (time) VALUES (%s);", (now,))
        conn.commit()
        
        cur.execute("SELECT COUNT(*) FROM visits;")
        count = cur.fetchone()[0]
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        text = f"<h1>Privet! Vizitov vsego: {count}</h1><p>Posledniy raz: {now}</p>"
        self.wfile.write(text.encode('utf-8'))
        
        cur.close()
        conn.close()

server = HTTPServer(('0.0.0.0', 8000), Handler)
print("Server started on port 8000")
server.serve_forever()
