from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dump, load
from urllib.parse import parse_qs
import time

def file_opener(name: str) -> list:
    x = []
    with open(name, "r", encoding="utf-8") as f:
        try:
            x = load(f)
        except Exception as e:
            print("error in json file: ", e)
    return x


def big_save(datadb : dict):
    sexx = file_opener("big_data.json")
    sexx.append(datadb)
    km = open("big_data.json", "w", encoding="utf-8")
    dump(sexx, km, ensure_ascii=False, indent=4)
    km.close()


def savef(data: dict):
    var = file_opener("data.json")
    var.append(data)
    d = open("data.json", "w", encoding="utf-8")
    try:
        dump(var, d, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Error in json file or this function: ", e)
    d.close()


def gogo(obj, files, cont_type, replaced, bin=True):
    if bin:
        with open(files, 'rb') as s:
            obj.send_response(200)
            obj.send_header("Content-Type", cont_type)
            obj.send_header("Server", "Guu/13.0")
            obj.end_headers()
            obj.wfile.write(s.read())
    else:
        if cont_type == "text/html":
            with open(files, 'r', encoding="utf-8") as f:
                kj = f.read().replace("{%%}", replaced)
                kj = kj.replace("{{}}", f"Q - {obj.path[1:]}")
                obj.send_response(200)
                obj.send_header("Content-Type", cont_type)
                obj.send_header("Server", "Guu/13.0")
                obj.end_headers()
                obj.wfile.write(kj.encode())
        else:   
            with open(files, 'r', encoding="utf-8") as f:
                kj = f.read().replace("{%%}", replaced)
                obj.send_response(200)
                obj.send_header("Content-Type", cont_type)
                obj.send_header("Server", "Guu/13.0")
                obj.end_headers()
                obj.wfile.write(kj.encode())



class Sex(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":
            gogo(self, 'index.html', "text/html", "{null} - give a query", False)
            return

        if self.path.startswith("/secret+1234"):
            print('Single line data saved.')
            savef({"timestamp": str(int(time.time())), "message": self.path[12:]})
            gogo(self, "temp.html", "text/html", "saved sucessfully!", False)
            return
        
        elif self.path == "/help":
            gogo(self, "page.html", "text/html", '0', False)
            return

        elif self.path.endswith("/style.css"):
            gogo(self, "style.css", "text/css", '123', False)
            return

        elif self.path.endswith("/MontenegrinGothicOne-Regular.ttf"):
            gogo(self, "MontenegrinGothicOne-Regular.ttf", "font/ttf", "ad", True)
            return

        elif self.path.endswith("/Unbounded-VariableFont_wght.ttf"):
            gogo(self, "Unbounded-VariableFont_wght.ttf", "font/ttf", "ad", True)
            return

        elif self.path.endswith('/favicon.ico'):
            gogo(self, "favicon.ico", "image/x-icon", None, True)
            return

        elif "." not in self.path:
            gogo(self, "index.html", "text/html", self.path[1:], False)
            return
        

        else:
            gogo(self, "index.html", "text/html", "{error} - try removing the [dot]", False)


    def do_POST(self):
        if self.path == "/help/api":
            ddd = self.rfile.read(int(self.headers.get("Content-Length", 0))).decode()
            gogo(self, "default.html", "text/html", "ok", False)
            big_save(parse_qs(ddd))
            print("multiline data saved.")
            return

        else:
            self.send_response(301)
            self.send_header("Server", "Guu/13.0")
            self.send_header("Location", "/")
            self.end_headers()
            return




def mains():
    o = HTTPServer(('', 8080), Sex)
    try:
         print("Listnning the server at port 8080")
         o.serve_forever()
    except KeyboardInterrupt:
        print("quit.")
        quit()

        
if __name__ == "__main__":
    mains()
