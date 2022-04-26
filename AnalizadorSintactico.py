from prettytable import PrettyTable

class AnalizadorSintactico:
    
    def __init__(self,tokens:list) -> None:
        self.errores = []
        self.tokens = tokens 
        
    def agregarError(self,esperado,obtenido):
        self.errores.append(
            '''ERROR SINTÁCTICO: se obtuvo {} se esperaba {}'''.format(obtenido,esperado)
        )
        
    def sacarToken(self):
        '''Saca el primer token y lo quita de la lista '''
        try:
            return self.tokens.pop(0)
        except:
            return None 
        
    def observarToken(self):
        '''Saca el primer token y lo mete de nuevo en la lista'''
        try:
            return self.tokens[0]
        except:
            return None
        
    def analizar(self):
        self.S()
    
    
    def S(self):
        self.INICIO()
        
    def INICIO(self):
        #Observar el primer elemento para decidir a dónde ir 
        
        temporal = self.observarToken()
        
        if temporal is None:
            self.agregarError("pr_RESULTADO | pr_JORNADA | pr_GOLES | pr_TABLA | pr_PARTIDOS | pr_TOP | pr_ADIOS ","EOF")
        elif temporal.tipo == 'pr_RESULTADO':
             self.RESULTADO()
        else:
            self.agregarError("pr_RESULTADO | pr_JORNADA | pr_GOLES | pr_TABLA | pr_PARTIDOS | pr_TOP | pr_ADIOS ",temporal.tipo)
            
    
    def RESULTADO(self):
        '''
        Muestra el resultado de un partido, especifican los equipos y la temporada
        
        Producción
                RESULTADO ::= pr_RESULTADO equipo pr_VS equipo fecha 
        '''
        
        equipo1 = None
        equipo2 = None 
        fecha = None
        token = self.sacarToken()
        if token.tipo == "pr_RESULTADO":
            token = self.sacarToken()
            
            
            #############TOKEN COMILLA #####################
            if token is None:
                self.agregarError("comilla","EOF")
                return
            elif token.tipo == "comilla":
                equipo1 = self.armarCadena()
    
                if equipo1 != "EOF":
                   print("Equipo 1 " + str(equipo1))
                   
                   ########### TOKEN VS ###################
                   token = self.sacarToken()
                    
                   if token is None:
                    self.agregarError("pr_VS","EOF")
                    return
                   elif token.tipo == "pr_VS":
                      ####### TOKEN COMILLA ################
                      token = self.sacarToken()
                      if token is None:
                        self.agregarError("pr_VS","EOF")
                        return
                      elif token.tipo == "comilla":
                          equipo2 = self.armarCadena()
                          if equipo2 != "EOF":
                             print("Equipo 2 " + str(equipo2))
                             
                             ###### TOKEN FECHA ########
                             ###### MENOR QUE #######
                             token = self.sacarToken()
                    
                             if token is None:
                                self.agregarError("menorQue","EOF")
                                return
                             elif token.tipo == "menorQue":
                                 ###### ENTERO #########
                                 token = self.sacarToken()
                                 if token is None:
                                    self.agregarError("entero","EOF")
                                    return
                                 elif token.tipo == "entero" and len(token.lexema) == 4:
                                     fecha += token.lexema
                                     
                                      
                                 elif token.tipo == "entero":
                                     self.agregarError("entero{4}",f"entero[{len(token.lexema)}]")
                                 else:
                                     self.agregarError("entero{4}",token.tipo)
                                 
                             else:
                                 self.agregarError("menorQue",token.tipo)
                                 
                             
                             
                          else:
                              self.agregarError("comilla","EOF")
                          
                      
                   else:
                     self.agregarError("pr_VS",token.tipo)
                   
                else:
                    self.agregarError("comilla","EOF")
            
            else:
                self.agregarError("comilla",token.tipo)
        else:
            self.agregarError("pr_RESULTADO","EOF")
            
        
            
    def armarCadena(self):
        #print("Empieza a armar cadena")
        token = self.sacarToken()
        #print("Lexema al principio " + token.lexema)
        i = 0
        cadena = ""
        while True:
          if token != None:  
            #print(f"Lexema {token.lexema} en iteracion {i} ")
            if token.tipo == "comilla":
                return cadena
            else:
                #print("Es de tipo identificador")
                cadena += token.lexema + " "
                #print(f"La cadena hasta ahora es {cadena}")
                
            token = self.sacarToken()
            i += 1
            
          else: 
              return "EOF"
            
    
    
    def imprimirErrores(self):
        '''Imprime una tabla con los errores'''
        x = PrettyTable()
        x.field_names = ["Descripcion"]
        for error_ in self.errores:
            x.add_row([error_])
        print(x)                
        
            
            
        
        
                
            
        
                 
    