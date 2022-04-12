from http.server import *
import urllib.request
import sys


def get_content(server_name, port, path):
    try:
        url = "http://" + server_name + ":" + str(port) + path
        req = urllib.request.Request(url)

        with urllib.request.urlopen(req) as response:
            return b'200', response.read()
    except:
        return b'404', b''



class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/grading/beacon":
            self.send_response(204)
            return
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()

        self.wfile.write("Hello Conor".encode())


def main():
    port = int(sys.argv[2])
    origin = sys.argv[4]
    server = HTTPServer(('0.0.0.0', port), RequestHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        return


    # code, content = get_content('cs5700cdnorigin.ccs.neu.edu', 8080, '/')
    # print(content)
    # print(code)


main()
