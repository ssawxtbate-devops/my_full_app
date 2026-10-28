from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        text = "<h1>Privet iz Kubernetes! Eto moy pervyy pod!</h1>"
        self.wfile.write(text.encode('utf-8'))

server = HTTPServer(('0.0.0.0', 8000), Handler)
print("Server started on port 8000")
server.serve_forever()
