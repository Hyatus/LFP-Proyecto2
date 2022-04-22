class Token:
    def __init__(self,lexema: str, linea: str, columna: int, tipo: str):
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
        self.tipo = tipo
        
        