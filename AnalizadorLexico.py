from prettytable import PrettyTable
from claseToken import *
from claseErrorL import *

class AnalizadorLexico:
  def __init__(self):
    self.listaTokens = []
    self.listaErrores = []
    self.PalabrasReservadas = ["RESULTADO","VS","TEMPORADA","JORNADA","GOLES","TABLA","PARTIDOS","ADIOS"]
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
    elif caracter in ["\t"," "]: #Espacios en blanco y tabulaciones
        self.columna += 1
    elif caracter == '$':
      print('Se terminó el análisis ')
    else:
      self.estado = 99
      self.buffer += caracter 
      self.columna += 1
      #self.agregarError(caracter,self.linea,self.columna)
      #self.columna += 1
      #self.estado = 0
      
  def E(self,caracter:str):
      if caracter != " " and caracter != "$":
          self.estado = 99
          self.buffer += caracter
          self.columna += 1
      else:
          self.agregarError(self.buffer,self.linea,self.columna)
          self.columna += 1
          self.estado = 0
          self.i -= 1 
          
  def s1(self,caracter:str):
    '''Estado S1'''  
    if caracter.isalpha():
      self.estado = 1
      self.buffer += caracter
      self.columna += 1
    elif caracter.isdigit():
      self.estado = 12
      self.buffer += caracter
      self.columna += 1  
    elif caracter == '_':
      self.estado = 12
      self.buffer += caracter
      self.columna += 1
    else:
      if self.buffer in self.PalabrasReservadas:
         self.agregarToken(self.buffer,self.linea,self.columna,"palabra reservada {}".format(self.buffer))
         self.estado = 0
         self.i -= 1
      elif self.buffer in self.condiciones:
         self.agregarToken(self.buffer,self.linea,self.columna,"condicion {}".format(self.buffer))
         self.estado = 0
         self.i -= 1
      elif self.buffer.isalpha():
         self.agregarToken(self.buffer,self.linea,self.columna,"nombre archivo")
         self.estado = 0
         self.i -= 1    
      else:
        self.agregarError(self.buffer,self.linea,self.columna)
        self.columna += 1
        self.estado = 0 
        self.i -= 1    
        
  def s12(self,caracter:str):
        '''Estado S12'''  
        if caracter.isalpha():
            self.estado = 12
            self.buffer += caracter
            self.columna += 1
        elif caracter.isdigit():
            self.estado = 12
            self.buffer += caracter
            self.columna += 1  
        elif caracter == '_':
            self.estado = 12
            self.buffer += caracter
            self.columna += 1   
        elif caracter == " " or caracter == "$":
            self.agregarToken(self.buffer,self.linea,self.columna,"nombre archivo")
            self.estado = 0
            self.i -= 1 
        else:
            self.buffer += caracter
            self.agregarError(self.buffer,self.linea,self.columna)
            self.columna += 1
            self.estado = 0
            self.i -= 1 

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
        elif self.estado == 12:
            self.s12(cadena[self.i])   
        elif self.estado == 99:
            self.E(cadena[self.i])          
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