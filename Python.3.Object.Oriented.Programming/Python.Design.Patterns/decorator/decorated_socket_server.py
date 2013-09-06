import socket
import gzip
from io import BytesIO

def respond(client):
    response = input("Enter a value:")
    client.send(bytes(response, "utf8"))
    client.close()

class LogSocket:
    def __init__(self, socket_):
        self.socket_ = socket_
    def send(self, data):
        print("Sending {0} to {1}".format(
            data, self.socket_.getpeername()[0]))
        self.socket_.send(data)

    def close(self):
        self.socket_.close()

class GzipSocket:
    def __init__(self, socket_):
        self.socket_ = socket_

    def send(self, data):
        buf = BytesIO()
        zipfile = gzip.GzipFile(fileobj=buf, mode="w")
        zipfile.write(data)
        zipfile.close()
        self.socket_.send(buf.getvalue())

    def getpeername(self):
        return self.socket_.getpeername()

    def close(self):
        self.socket_.close()

if __name__ == "__main__":
    gzip_enabled = True
    log_enabled = True
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 2401))
    server.listen(1)
    try:
        while True:
            client, addr = server.accept()
            # Mind the order of decorators here
            if gzip_enabled:
                client = GzipSocket(client)
            if log_enabled:
                client = LogSocket(client)
            respond(client)
    finally:
        server.close()

# ---- Reference Socket Client Code ---- #
# import socket
# import gzip
# from io import BytesIO
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(("localhost", 2401))
# data = client.recv(1024)
# zipfile= gzip.GzipFile(fileobj=BytesIO(data), mode="r")
# print("Received: {0}".format(unzipped_file.read()))
# zipfile.close()
# client.close()
