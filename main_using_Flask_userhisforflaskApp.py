from flask import Flask, request, Response
from json import dump, load
from urllib.parse import parse_qs
import time

app = Flask(__name__)


def file_opener(name: str) -> list:
    x = []
    with open(name, "r", encoding="utf-8") as f:
        try:
            x = load(f)
        except Exception as e:
            print("error in json file: ", e)
    return x


def big_save(datadb: dict):
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


def get_full_path() -> str:
    """
    Recreates BaseHTTPRequestHandler.self.path, which is the raw
    path + query string of the request line (e.g. '/help/api?a=1').
    """
    qs = request.query_string.decode()
    if qs:
        return request.path + "?" + qs
    return request.path


def gogo(path: str, files: str, cont_type: str, replaced, bin: bool = True) -> Response:
    if bin:
        with open(files, "rb") as s:
            data = s.read()
        resp = Response(data)
        resp.headers["Content-Type"] = cont_type
        resp.headers["Server"] = "Guu/13.0"
        return resp
    else:
        if cont_type == "text/html":
            with open(files, "r", encoding="utf-8") as f:
                kj = f.read().replace("{%%}", replaced)
                kj = kj.replace("{{}}", f"Q - {path[1:]}")
            resp = Response(kj)
            resp.headers["Content-Type"] = cont_type
            resp.headers["Server"] = "Guu/13.0"
            return resp
        else:
            with open(files, "r", encoding="utf-8") as f:
                kj = f.read().replace("{%%}", replaced)
            resp = Response(kj)
            resp.headers["Content-Type"] = cont_type
            resp.headers["Server"] = "Guu/13.0"
            return resp


@app.route("/", defaults={"u_path": ""}, methods=["GET"])
@app.route("/<path:u_path>", methods=["GET"])
def catch_all_get(u_path):
    full_path = get_full_path()

    if full_path == "/":
        return gogo(full_path, "index.html", "text/html", "{null} - give a query", False)

    if full_path.startswith("/secret+1234"):
        print("Single line data saved.")
        savef({"timestamp": str(int(time.time())), "message": full_path[12:]})
        return gogo(full_path, "temp.html", "text/html", "saved sucessfully!", False)

    elif full_path == "/help":
        return gogo(full_path, "page.html", "text/html", "0", False)

    elif full_path.endswith("/style.css"):
        return gogo(full_path, "style.css", "text/css", "123", False)

    elif full_path.endswith("/MontenegrinGothicOne-Regular.ttf"):
        return gogo(full_path, "MontenegrinGothicOne-Regular.ttf", "font/ttf", "ad", True)

    elif full_path.endswith("/Unbounded-VariableFont_wght.ttf"):
        return gogo(full_path, "Unbounded-VariableFont_wght.ttf", "font/ttf", "ad", True)

    elif full_path.endswith("/favicon.ico"):
        return gogo(full_path, "favicon.ico", "image/x-icon", None, True)

    elif "." not in full_path:
        return gogo(full_path, "index.html", "text/html", full_path[1:], False)

    else:
        return gogo(full_path, "index.html", "text/html", "{error} - try removing the [dot]", False)


@app.route("/", defaults={"u_path": ""}, methods=["POST"])
@app.route("/<path:u_path>", methods=["POST"])
def catch_all_post(u_path):
    full_path = get_full_path()

    if full_path == "/help/api":
        ddd = request.get_data().decode()
        resp = gogo(full_path, "default.html", "text/html", "ok", False)
        big_save(parse_qs(ddd))
        print("multiline data saved.")
        return resp

    else:
        resp = Response(status=301)
        resp.headers["Server"] = "Guu/13.0"
        resp.headers["Location"] = "/"
        return resp


def mains():
    try:
        print("Listnning the server at port 8080")
        app.run(host="0.0.0.0", port=8080)
    except KeyboardInterrupt:
        print("quit.")
        quit()


if __name__ == "__main__":
    mains()
