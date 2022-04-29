class Series:
    def __init__(self, nombre, url, type):
        self.nombre = nombre
        self.url = url
        self.type = type
    def to_dict(self):
        return dict((key,value) for (key, value) in self.__dict__.items())
