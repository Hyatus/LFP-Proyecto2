class ErrorL:
    def __init__(self,descripcion: str, linea: int, columna: int):
        self.descripcion = descripcion
        self.linea = linea
        self.columna = columna