from prettytable import PrettyTable
from claseToken import *
from claseErrorL import *

class AnalizadorLexico:
  def __init__(self):
    self.listaTokens = []
    self.listaErrores = []
    self.PalabrasReservadas = ["RESULTADO","VS","TEMPORADA","JORNADA","GOLES","TABLA","PARTIDOS","ADIOS","TOP"]
    self.condiciones = ["LOCAL","VISITANTE","TOTAL","SUPERIOR","INFERIOR"]
    self.linea = 1 
    self.columna = 0
    self.buffer = ""
    self.estado = 0 # Estado Inicial 
    self.i = 0 #Contador para recorrer la cadena
  

  def agregarToken(self,lexema,linea,columna,token):
      self.listaTokens.append(Token(lexema,linea,columna,token))  
      self.buffer = ""

  def agregarError(self,caracter,linea,columna):
      self.listaErrores.append(ErrorL('Lexema '+caracter+' no reconocido en el lenguaje ',linea,columna))
      self.buffer = ""  

  def s0(self,caracter:str):
    '''Estado S0'''
    if caracter.isalpha():
        self.estado = 1
        self.buffer += caracter
        self.columna += 1
    elif caracter.isdigit():
        self.estado = 2
        self.buffer += caracter
        self.columna += 1
    elif caracter == '"':
        self.estado = 3
        self.buffer += caracter 
        self.columna +=1
    elif caracter == "<":
        self.estado = 4
        self.buffer += caracter 
        self.columna +=1
    elif caracter == ">":
        self.estado = 5
        self.buffer += caracter 
        self.columna +=1
    elif caracter == "-":
        self.estado = 6
        self.buffer += caracter 
        self.columna +=1
         
    elif caracter in ["\t"," "]: #Espacios en blanco y tabulaciones
        self.columna += 1
    elif caracter == '$':
      print('Se terminó el análisis ')
    else:
      self.agregarError(caracter,self.linea,self.columna)
      self.columna += 1
      self.estado = 0
          
  def s1(self,caracter:str):
    '''Estado S1'''  
    if caracter.isalpha():
      self.estado = 1
      self.buffer += caracter
      self.columna += 1
    elif caracter.isdigit():
      self.estado = 1
      self.buffer += caracter
      self.columna += 1  
    elif caracter == '_':
      self.estado = 1
      self.buffer += caracter
      self.columna += 1
    elif self.buffer in self.PalabrasReservadas:
         self.agregarToken(self.buffer,self.linea,self.columna,"pr_{}".format(self.buffer))
         self.estado = 0
         self.i -= 1
    elif self.buffer in self.condiciones: 
         self.agregarToken(self.buffer,self.linea,self.columna,"condicion{}".format(self.buffer))
         self.estado = 0
         self.i -= 1
    else: 
         self.agregarToken(self.buffer,self.linea,self.columna,"identificador")
         self.estado = 0
         self.i -= 1
         
  def s2(self,caracter):
        if caracter.isdigit():
            self.estado = 2
            self.buffer += caracter 
            self.columna += 1
        else:
            self.agregarToken(self.buffer,self.linea,self.columna,"entero")
            self.estado = 0
            self.i -= 1
            
  def s3(self):
      self.agregarToken(self.buffer,self.linea,self.columna,"comilla")
      self.estado = 0
      self.i -= 1
      
  def s4(self):
      self.agregarToken(self.buffer,self.linea,self.columna,"menorQue")
      self.estado = 0
      self.i -= 1  
      
  def s5(self):
      self.agregarToken(self.buffer,self.linea,self.columna,"mayorQue")
      self.estado = 0
      self.i -= 1

  def s6(self,caracter):
      if caracter == "f":
        self.buffer += caracter   
        self.agregarToken(self.buffer,self.linea,self.columna,"flagFile")
        self.estado = 0 
      elif caracter == "n":
        self.buffer += caracter   
        self.agregarToken(self.buffer,self.linea,self.columna,"flagTop")
        self.estado = 0    
      elif caracter == "j":
        self.estado = 7
        self.buffer += caracter 
        self.columna += 1  
      else:
        self.agregarToken(self.buffer,self.linea,self.columna,"guion")
        self.estado = 0
        self.i -= 1   
        
  def s7(self,caracter):
      if caracter == "i":
        self.buffer += caracter 
        self.agregarToken(self.buffer,self.linea,self.columna,"flagApartir")
        self.estado = 0
      elif caracter == "f":
        self.buffer += caracter   
        self.agregarToken(self.buffer,self.linea,self.columna,"flagHasta")
        self.estado = 0
      else:
        self.agregarError(caracter,self.linea,self.columna)
        self.columna += 1
        self.estado = 0  
             
     
  def analizar(self,cadena):
    cadena += '$'
    self.listaErrores = []
    self.listaTokens = []
    self.i = 0

    while self.i < len(cadena):
        if self.estado == 0:
            self.s0(cadena[self.i])
        elif self.estado == 1:
            self.s1(cadena[self.i])
        elif self.estado == 2:
            self.s2(cadena[self.i])
        elif self.estado == 3:
            self.s3()
        elif self.estado == 4:
            self.s4()
        elif self.estado == 5:
            self.s5()
        elif self.estado == 6:
            self.s6(cadena[self.i])   
        elif self.estado == 7:
            self.s7(cadena[self.i])    
                                           
        self.i += 1

  def imprimirTokens(self):
      x = PrettyTable()
      x.field_names = ["lexema","linea","columna","tipo"]
      for token in self.listaTokens:
        x.add_row([token.lexema,token.linea,token.columna,token.tipo])
      print(x)

  def imprimirErrores(self):
      x = PrettyTable()
      x.field_names = ["Descripción","linea","columna"]
      for error in self.listaErrores:
        x.add_row([error.descripcion,error.linea,error.columna])
      print(x)