import hashlib
import http.server
import datetime
import secrets
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
                return True
            else:
                return False

    def CreateSession(self):
        SessionKey = secrets.token_urlsafe(32)
        Expiration = datetime.datetime.now() + datetime.timedelta(minutes=SessionTimeout)
        Sessions[SessionKey] = Expiration
        print(Sessions)
        return SessionKey

    def CheckSession(self):
        Cookies = self.headers.get("Cookie")
        print(Cookies)
        if not Cookies:
            return False
        for item in Cookies.split(";"):
            if "session=" not in item:
                pass
            else:
                SessionKey = item.split('=')[1].strip()
                if SessionKey not in Sessions:
                    return False
                else:
                    if Sessions[SessionKey] < datetime.datetime.now():
                        del Sessions[SessionKey]
                        return False
                    else:
                        return True
        return False

    def do_GET(self):
        if self.path == "/":
            self.send_HTML("index.html")
        elif self.path.startswith("/Dashboard"):
            if self.CheckSession():
                self.send_HTML(self.path[1:])
            else:
                self.send_response(303)
                self.send_header("Location", "/")
                self.end_headers()
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
                self.send_response(303)
                session = str(self.CreateSession())
                self.send_header("Set-Cookie",f"session={session}; Path=/; HttpOnly; Max-Age={SessionTimeout * 60}; Secure")
                self.send_header("Location", "/Dashboard/dashboard.html")
                self.end_headers()
            else :
                self.send_response(303)
                self.send_header("Location", "/index.html")
                self.end_headers()