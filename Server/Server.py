import http.server
import datetime
import ssl
import threading
import http.client
import http.server
import Server.HandlerOwn as Handler


Hostname = "localhost"
Port = 8080
Conn = http.client.HTTPConnection(host=Hostname, port=Port)
logfile = "logs/Commands/" + datetime.datetime.now().strftime("%d.%m.%Y") + ".log"
log = open(logfile, "a")
ServerLogname = "logs/Server/" + datetime.datetime.now().strftime("%d.%m.%Y") + ".log"
ServerLogfile = open(ServerLogname, "w")
HandlerV = http.server.SimpleHTTPRequestHandler

def start():
    log.write(datetime.datetime.now().strftime("%H:%M:%S") + ": Starting HTTP Server on port: " + str(Port) + "..." + "\n")
    thread = http.server.HTTPServer((Hostname, Port), Handler.Handler)
    context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="Server/Certificate/cert.pem")
    thread.socket = context.wrap_socket(thread.socket, server_side=True)
    try:
        threading.Thread(target=thread.serve_forever()).start()
        print("HTTP Server started on port: " + str(Port))
    except KeyboardInterrupt:
        thread.socket.close()