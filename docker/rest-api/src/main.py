
from typing import Any
from venv import create
from flask import Flask, make_response, request
from database import BookBase
from datetime import datetime

bookBase = BookBase()
app = Flask(__name__)

prefix = lambda r: f"/api/v1{r}"

def createResponse(data: Any, route: str, code:int=200, **kwargs):
    pass

@app.route(prefix("/"))
def default():
    return createResponse(["This is a sample API for books."])
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)