
from flask import Flask, make_response, request
from database import BookBase
from datetime import datetime

bookBase = BookBase()
app = Flask(__name__)

prefix = lambda r: f"/api/v1{r}"

def createResponse(data: dict, route: str, code:int=200, **kwargs):
    if not isinstance(data, list):
        data = [data]
    return make_response({
        "time": datetime.now(),
        "route": route,
        "size": len(data),
        "data": data,
        **kwargs
    }, code, {"Content-Type": "application/json"})

@app.route(prefix("/"))
def default():
    return createResponse(["This is a sample API for books."], route=request.path)

@app.route(prefix("/books"), methods=["GET"])
def books():
    listParse = lambda l: ";".join(l) if isinstance(l, list) else l
    books = bookBase.data()
    args = request.args
    if any(k in args.keys() for k in ["authors", "categories", "title"]):
        for a in args:
            books = [book for book in books if args.get(a).lower() in listParse(book.get(a)).lower()]
    return createResponse(books, route=request.path, filter={a:args.get(a) for a in args})

@app.route(prefix("/books/<isbn>"), methods=["GET", "PUT", "DELETE"])
def getBook(isbn):
    books = bookBase.data()
    if request.method == "GET":
        book = next((book for book in books if book.get("isbn", None)==isbn), {})
        return createResponse([book], route=request.path)
    elif request.method == "PUT":
        book = request.get_json()
        if book["isbn"]!=isbn:
            return createResponse([], route=request.path, code=400, error="ISBN not matching")
        if not any(b.get("isbn", None)==book["isbn"] for b in books):
            try:
                bookBase.inject(book)
                return createResponse(book, route=request.path, code=201)
            except TypeError:
                print("this is where i want to go")
                return createResponse([], route=request.path, code=400, error="You are missing some datapoints")
    else:
        if isbn in [b.get("isbn", None) for b in books]:
            book = bookBase.remove(isbn=isbn)
            return createResponse(book, route=request.path)
        else:
            return createResponse([], route=request.path, code=400, error="ISBN not present")

@app.route(prefix("/books/data/structure"))
def getColumns():
    books = bookBase.data()
    data = {key for book in books for key in book.keys()}
    return createResponse(data, route=request.path)

@app.route(prefix("/resources"))
def getResources():
    data = [{"resource": url.rule, "methods": list(url.methods)} for url in app.url_map.iter_rules()]
    return createResponse(data, route=request.path)
        

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)
