import argparse
import mysql.connector
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

def get_customer_names():
    with open("/tmp/secret", "r") as creds:
        data = json.load(creds)
    mydb = mysql.connector.connect (
      host=os.environ['MYSQL_HOST'],
      user=data['username'],
      password=data['password'],
      database=os.environ['MYSQL_DATABASE']
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT name FROM customers")
    myresult = mycursor.fetchall()
    cus_names = "\n"
    for x in myresult:
        cus_names += "{}\n".format(x[0])
    mycursor.close()
    mydb.close()
    return cus_names

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html(get_customer_names()))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(self._html("POST!"))


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="0.0.0.0",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
