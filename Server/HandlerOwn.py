import hashlib
import http.server
import datetime
from urllib.parse import parse_qs
import httpx

ServerLogname = "logs/Server/" + datetime.datetime.now().strftime("%d.%m.%Y") + ".log"
ServerLogfile = open(ServerLogname, "w")

Username = "Langebe"
PasswordHash = "e5d7234d85b9b847d5cbcc7974bca2a82a0cf2bda7dc728d899370ba423275fcd3d7e47e83b87f1122968c3f7c823c6d6798ce91ef171baac51c41ce3739749d"
Sessions = {}
SessionTimeout = 30

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        ServerLogfile.write(datetime.datetime.now().strftime("%H:%M:%S: ") + format % args + "\n")
        ServerLogfile.flush()

    def send_HTML(self, file, **kwargs):
        with open("Server/Website/"+file, 'r', encoding='utf-8') as f:
            html = f.read()
        for key, value in kwargs.items():
            html = html.replace("{{"+key+"}}", value)
        if file.endswith(".html"):
            ContentType = "text/html"
        elif file.endswith(".css"):
            ContentType = "text/css"
        elif file.endswith(".js"):
            ContentType = "text/javascript"
        elif file.endswith(".jpeg"):
            ContentType = "image/jpeg"
        elif file.endswith(".png"):
            ContentType = "image/png"
        self.send_response(200)
        self.send_header("Content-type", ContentType)
        self.end_headers()
        self.wfile.write(html.encode())

    def CredentialsCheck(self, username, password):
        if username != Username:
            return False
        else:
            passwordHash = hashlib.sha512(bytes(password, "utf-8")).hexdigest()
            if passwordHash == PasswordHash:
                httpx.Cookies().clear()
                SessionKey = hashlib.sha512(bytes(username + datetime.datetime.now(), "utf-8")).hexdigest()
                print("Session Key: " + SessionKey)
                NewSession = SessionKey + "," + datetime.datetime.now().strftime("%d.%m.%Y")
                Sessions = NewSession
                httpx.Cookies().set(name="SessionKey", value=SessionKey)
                return True
            else:
                return False

    def do_GET(self):
        if self.path == "/":
            self.send_HTML("index.html")
        elif self.path.startswith("/Dashboard/"):
            self.wfile.write(bytes("This Resource is not available", "utf-8"))
        else:
            try:
                self.send_HTML(self.path)
            except:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("<html><head></head><body>Request URL:" + self.path + "</body></html>", "utf-8"))

    def do_POST(self):
        if self.path == "/api/login":
            data = parse_qs(self.rfile.read(int(self.headers['content-length'])).decode("utf-8"))
            username = data.get("username")[0]
            password = data.get("password")[0]
            if self.CredentialsCheck(username, password):
                self.send_HTML("Dashboard/dashboard.html")
            else :
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.send_HTML("index.html", Error="Wrong username or password")