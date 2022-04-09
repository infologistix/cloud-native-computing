from email.generator import Generator
import json


class BookBase():
    def __init__(self) -> None:
        self.__data = []
        with open("./data/books.json", "r") as f:
            self.__data = json.load(f)
        self.__keys = {key for book in self.__data for key in book.keys()}
        
    def data(self):
        return self.__data
    
    def inject(self, data:dict):
        if any(k not in data.keys() for k in self.__keys):
            raise TypeError("Dataset can not be injected")
        self.__data.append(data)
        return data
    
    def remove(self, isbn:str):
        for index, book in enumerate(self.__data):
            if book.get("isbn", None)==isbn:
                del self.__data[index]
                return book