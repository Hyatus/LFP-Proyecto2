from AnalizadorLexico import *


while True:
    lexico = AnalizadorLexico()
    
    cadena = input("Ingrese comando -> ")
    
    lexico.analizar(cadena)
    
    listaTokens = lexico.listaTokens
    listaErrores = lexico.listaErrores
    
    
    print("LISTA TOKENS")
    lexico.imprimirTokens()
    print("LISTA ERRORES ")
    lexico.imprimirErrores()
   