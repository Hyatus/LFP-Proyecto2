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
    self.contadorFecha = 0
    self.contadorNumero = 0

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
    elif caracter == '"':
        self.estado = 2 
        self.buffer += caracter
        self.columna += 1   
    elif caracter == "<":
        self.estado = 3
        self.buffer += caracter 
        self.columna += 1
    elif caracter.isdigit():
        self.estado = 5
        self.buffer += caracter
        self.columna +=1   
        self.contadorNumero += 1 
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
    elif self.buffer in self.PalabrasReservadas:
         self.agregarToken(self.buffer,self.linea,self.columna,"palabra reservada {}".format(self.buffer))
         self.estado = 0
         self.i -= 1
    elif self.buffer in self.condiciones: 
         self.agregarToken(self.buffer,self.linea,self.columna,"condicion {}".format(self.buffer))
         self.estado = 0
         self.i -= 1
    else:
      if caracter == " " or caracter == "$":
         if self.buffer.isalpha():
         #self.estado = 12
         #self.buffer += caracter
         #self.columna += 1   
          self.agregarToken(self.buffer,self.linea,self.columna,"identificador")
          self.estado = 0
          self.i -= 1    
      else:
         self.estado = 99
         self.buffer += caracter 
         self.columna += 1  
        #self.agregarError(self.buffer,self.linea,self.columna)
        #self.columna += 1
        #self.estado = 0 
        #self.i -= 1    
        
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
            self.agregarToken(self.buffer,self.linea,self.columna,"identificador")
            self.estado = 0
            self.i -= 1 
        else:
            self.estado = 99
            self.buffer += caracter 
            self.columna += 1
            #self.buffer += caracter
            #self.agregarError(self.buffer,self.linea,self.columna)
            #self.columna += 1
            #self.estado = 0
            #self.i -= 1 
            
  def s2(self,caracter):
      if caracter.isalpha():
          self.estado = 2
          self.buffer += caracter
          self.columna += 1     
      elif caracter == " ":
          self.estado = 2
          self.buffer += caracter
          self.columna += 1 
      else:
          self.estado = 21
          self.buffer += caracter
          self.columna += 1 
    
  def s21(self,caracter):
      if caracter == '"':
            self.estado = 21
            self.buffer += caracter
            self.columna += 1
      elif caracter == " " or caracter == "$":
            self.agregarToken(self.buffer,self.linea,self.columna,"equipo")
            self.estado = 0
            self.i -= 1 
      else:
            self.estado = 99
            self.buffer += caracter 
            self.columna += 1  
        
        
            
  def s3(self,caracter):
      if caracter.isdigit() and self.contadorFecha <= 4:
          self.estado = 3
          self.buffer += caracter
          self.columna += 1  
          self.contadorFecha += 1
          #print(f"1Agrego un numero {caracter}")   
      else:
          if self.contadorFecha == 4:
            #print(f"1Llegué a 4 dígitos ahora me paso a 31 {caracter}")
            self.estado = 31
            #self.buffer += caracter
            self.columna += 1  
            self.contadorFecha = 0
            self.i -=1
          else:
            self.estado = 99
            self.buffer += caracter 
            self.columna += 1    
              
  def s31(self,caracter):
      #print(f"llegue a 31 {caracter}")
      if caracter == "-":
         self.estado = 32
         self.buffer += caracter 
         self.columna += 1
         #print(f"Ahora me paso a 32 {caracter}")
      else:
          self.estado = 99
          self.buffer += caracter 
          self.columna += 1      
               
  def s32(self,caracter):
    #print(f"Llegué a 32 {caracter}")
    if caracter.isdigit() and self.contadorFecha <= 4:
        self.estado = 32
        self.buffer += caracter
        self.columna += 1  
        self.contadorFecha += 1
    else:
      if self.contadorFecha == 4:
            #print(f"1Llegué a 4 dígitos ahora me paso a 33 {caracter}")
            self.estado = 33
            #self.buffer += caracter
            self.columna += 1  
            self.contadorFecha = 0
            self.i -=1
      else:
            self.estado = 99
            self.buffer += caracter 
            self.columna += 1    
  
  def s33(self,caracter):
      #print(f"Llegué a 33 {caracter}")  
      if caracter == ">":
         self.estado = 33
         self.buffer += caracter
         self.columna += 1   
      elif caracter == " " or caracter == "$":
          self.agregarToken(self.buffer,self.linea,self.columna,"intervalo fecha")
          self.estado = 0
          self.i -= 1     
      else:
          self.estado = 99
          self.buffer += caracter 
          self.columna += 1  

  def s5(self,caracter):
      #print(f"llegue a s5 {caracter} * {self.contadorNumero}")
      if caracter.isdigit() and self.contadorNumero < 2:
         self.estado = 5
         self.buffer += caracter
         self.columna += 1  
         self.contadorNumero += 1
      elif (self.contadorNumero == 2 and (caracter == " " or caracter == "$")):
           self.agregarToken(self.buffer,self.linea,self.columna,"numero")
           self.estado = 0
           self.i -= 1
           self.contadorNumero = 0
      else:
           if caracter == " " and self.contadorNumero == 1:
                 self.agregarError(self.buffer,self.linea,self.columna)
                 self.columna += 1
                 self.estado = 0 
                 self.i -= 1 
           else:     
                self.estado = 99
                self.buffer += caracter 
                self.columna += 1    
      
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
        elif self.estado == 2:
            self.s2(cadena[self.i])           
        elif self.estado == 3:
            self.s3(cadena[self.i])
        elif self.estado == 31:
            self.s31(cadena[self.i])  
        elif self.estado == 32:
            self.s32(cadena[self.i])
        elif self.estado == 33:
            self.s33(cadena[self.i])
        elif self.estado == 5:
            self.s5(cadena[self.i])
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