from prettytable import PrettyTable
from pyparsing import ParseExpression

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
        elif temporal.tipo == 'pr_JORNADA':
             self.JORNADA() 
        elif temporal.tipo == 'pr_GOLES':
             self.GOLES()  
        elif temporal.tipo == 'pr_TABLA':
             self.TABLA()
        elif temporal.tipo == 'pr_PARTIDOS':
             self.PARTIDOS()   
        elif temporal.tipo == 'pr_TOP':
             self.TOP()   
        elif temporal.tipo == 'pr_ADIOS':
             return     
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
        fecha = ""
        
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
                   #print("Equipo 1 " + str(equipo1))
                   
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
                             #print("Equipo 2 " + str(equipo2))
                             
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
                                     
                                     ##### GUION ##############
                                     token = self.sacarToken()
                                     if token is None:
                                         self.agregarError("guion","EOF")
                                     elif token.tipo == "guion":
                                         fecha += token.lexema
                                         ######## ENTERO ##########
                                         token = self.sacarToken()
                                         if token is None:
                                             self.agregarError("entero","EOF")
                                             return
                                         elif token.tipo == "entero" and len(token.lexema) == 4:
                                             fecha += token.lexema
                                             #print(f"fecha 2 {fecha}")  
                                             
                                             ###### MAYOR QUE #########
                                             token = self.sacarToken()
                                             
                                             if token is None:
                                                 self.agregarError("mayorQue","EOF")
                                             elif token.tipo == "mayorQue":
                                                 
                                                 ######## EOF ############
                                                 token = self.sacarToken()
                                                 if token is None:
                                                    print(f"Equipo-1: {equipo1}")
                                                    print(f"Equipo-2: {equipo2}")
                                                    print(f"fecha: {fecha}") 
                                                 else:
                                                    self.agregarError("EOF",token.tipo)     
                                             else:
                                                 self.agregarError("mayorQue",token.tipo)
                                                         
                                             
                                         elif token.tipo == "entero":
                                            self.agregarError("entero{4}",f"entero[{len(token.lexema)}]")
                                         else:
                                            self.agregarError("entero{4}",token.tipo)
                                    
                        
                                     else:
                                         self.agregarError("guion",token.tipo)    
                                     
                                     
                                      
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
    
    def JORNADA(self):
        '''
        Muestra en un archivo HTML el resultado de
        todos los partidos disputados en una jornada, se especifican la jornada y la
        temporada
        
        Producción
                JORNADA ::=  pr_JORNADA entero{2} pr_temporada fecha 
                            |pr_JORNADA entero{2} pr_temporada fecha flagF identificador  
        '''
        
        numero = 0
        fecha = ""
        nombreArchivo = None 
        
        token = self.sacarToken()
        if token.tipo == "pr_JORNADA":
            token = self.sacarToken()
            
            ####### ENTERO ###### 
            if token is None:
                self.agregarError("entero","EOF")
                return
            
            elif token.tipo == "entero" and len(token.lexema) == 2:
                
                numero = token.lexema 
                #print(f"Numero -> {numero}")
                
            
                ##### TEMPORADA ######
                token = self.sacarToken()
                if token is None:
                    self.agregarError("pr_TEMPORADA","EOF")
                    return
                elif token.tipo == "pr_TEMPORADA":
                    ####### MENOR QUE ##########
                    token = self.sacarToken()
                    if token is None:
                        self.agregarError("menorQue","EOF")
                        return
                    elif token.tipo == "menorQue":
                        
                        ######## ENTERO ########
                        token = self.sacarToken()
                        if token is None:
                            self.agregarError("entero{4}","EOF")
                            return
                        elif token.tipo == "entero" and len(token.lexema) == 4:
                            fecha += token.lexema 
                            ###### GUION ######
                            token = self.sacarToken()
                            if token is None:
                                self.agregarError("guion","EOF")
                                return
                            elif token.tipo == "guion":
                                fecha += token.lexema
                                ######## ENTERO ########
                                token = self.sacarToken()
                                if token is None:
                                    self.agregarError("entero{4}","EOF")
                                    return
                                elif token.tipo == "entero" and len(token.lexema) == 4:
                                    fecha += token.lexema
                                    ###### MAYOR QUE ########
                                    token = self.sacarToken()
                                    if token is None:
                                        self.agregarError("mayorQue","EOF")
                                        return
                                    elif token.tipo == "mayorQue":
                                        ######## EOF | FLAG ARCHIVO ###### 
                                        token = self.sacarToken()
                                        if token is None:
                                            print(f"Numero: {numero}")
                                            print(f"Fecha {fecha}")
                                        elif token.tipo == "flagFile":
                                            
                                            ######### NOMBRE ARCHIVO ########
                                            token = self.sacarToken()
                                            if token is None:
                                                self.agregarError("identificador","EOF")
                                                return
                                            elif token.tipo == "identificador":
                                                nombreArchivo = token.lexema
                                                ######### EOF ########
                                                token = self.sacarToken()
                                                if token is None:
                                                    print(f"Numero: {numero}")
                                                    print(f"Fecha {fecha}")
                                                    print(f"nombre Archivo {nombreArchivo}")
                                                else:
                                                    self.agregarError("EOF",token.tipo)
                                                    return 
                                                    
                                                
                                            else:
                                                self.agregarError("identificador",token.tipo)
                                                return 
                                            
                                            
                                            
                                            
                                        else:
                                            self.agregarError("flagFile",token.tipo)
                                            return 
                                            
                                                
                                            
                                    else:
                                        self.agregarError("mayorQue",token.tipo)
                                        return 
                                        
                                elif token.tipo == "entero":
                                    self.agregarError("entero{4}",f"entero[{len(token.lexema)}]")
                                    return
                                else:
                                    self.agregarError("entero",token.tipo)
                                    return    
                                    
                                
                            
                            else:
                                self.agregarError("guion",token.tipo)
                                return
                            
                        elif token.tipo == "entero":
                            self.agregarError("entero{4}",f"entero[{len(token.lexema)}]")
                            return
                        else:
                            self.agregarError("entero",token.tipo)
                            return
                        
                        
                    else:
                        self.agregarError("menorQue",token.tipo)
                        return
                    
                    
                else:
                    self.agregarError("pr_TEMPORADA",token.tipo)
                    return
                    
                    
            elif token.tipo == "entero":
                self.agregarError("entero{2}",f"entero[{len(token.lexema)}]")
                return
            
            else:
                self.agregarError("entero{2}",token.tipo)
                return
        
            
        else:
            self.agregarError("pr_JORNADA","EOF")    
    
    def GOLES(self):
        '''
        Muestra el total de goles anotados por un
        equipo, se especifica la condición de los goles, el equipo y la temporada

        
        GOLES	::=	pr_goles condicion equipo pr_temporada fecha				
  
        '''
        condicion = None
        equipo = None
        fecha = "" 
        
        token = self.sacarToken()
        if token.tipo == "pr_GOLES":
            token = self.sacarToken()
            #### CONDICION 
            if token is None: 
                self.agregarError("condicionLOCAL | condicionVISITANTE | condicionTOTAL","EOF")
            elif token.tipo == "condicionLOCAL" or token.tipo == "condicionVISITANTE" or token.tipo == "condicionTOTAL":
                condicion = token.lexema
                #print("->",condicion)
                
                ###### COMILLA #########
                token = self.sacarToken()
                if token is None:
                    self.agregarError("comilla","EOF")
                elif token.tipo == "comilla":
                    equipo = self.armarCadena()
    
                    if equipo != "EOF":
                       #print("Equipo->",equipo)
                       ####### TEMPORADA ####### 
                       token = self.sacarToken()
                       if token is None:
                           self.agregarError("pr_TEMPORADA","EOF")
                       elif token.tipo == "pr_TEMPORADA":
                           ###### MENOR QUE ########
                           token = self.sacarToken()
                           if token is None:
                               self.agregarError("menorQue","EOF")
                           elif token.tipo == "menorQue":
                                ###### ENTERO #########
                                token = self.sacarToken()
                                if token is None:
                                    self.agregarError("entero{4}","EOF")
                                elif token.tipo == "entero" and len(token.lexema) == 4:
                                    fecha += token.lexema
                                    ##### GUION #####
                                    token = self.sacarToken()
                                    if token is None:
                                       self.agregarError("guion","EOF")
                                    elif token.tipo == "guion":
                                        fecha += token.lexema
                                        ###### ENTERO #########
                                        token = self.sacarToken()
                                        if token is None:
                                            self.agregarError("entero{4}","EOF")
                                        elif token.tipo == "entero" and len(token.lexema) == 4:
                                            fecha += token.lexema
                                            ##### MAYOR QUE ##### 
                                            token = self.sacarToken()
                                            if token is None:
                                                self.agregarError("mayorQue","EOF")
                                            elif token.tipo == "mayorQue":
                                                ######## EOF #######
                                                token = self.sacarToken()
                                                if token is None:
                                                    print("Condicion -> ",condicion)
                                                    print("Equipo->",equipo)
                                                    print("Fecha->",fecha)
                                                else:
                                                    self.agregarError("EOF",token.tipo)   
                                                    
                                            else:
                                                self.agregarError("mayorQue",token.tipo)
                                        
                                        elif token.tipo == "entero":
                                            self.agregarError("entero{4}",f"entero[{len(token.lexema)}]")
                                        else:
                                            self.agregarError("entero{4}",token.tipo)
                                            
                                    else:
                                        self.agregarError("guion",token.tipo)       
                                    
                                elif token.tipo == "entero":
                                    self.agregarError("entero{4}",f"entero[{len(token.lexema)}]")
                                else:
                                    self.agregarError("entero{4}",token.tipo)
                                    
                                    
                                
                           else:
                               self.agregarError("menorQue",token.tipo)
                           
                       else:
                           self.agregarError("pr_TEMPORADA",token.tipo)
                    else:
                        self.agregarError("comilla","EOF")
                        
                        
                else:
                
                    self.agregarError("comilla",token.tipo)
                
                
            else:
                self.agregarError("condicionLOCAL | condicionVISITANTE | condicionTOTAL",token.tipo)
            
        else:
            self.agregarError("pr_GOLES","EOF") 
    
    def TABLA(self):
        '''
       Muestra la clasificación de La Liga (ordenamiento respecto a puntos), se especifica la temporada:

        
        TABLA	::=	 pr_tabla pr_temporada fecha 					
	            |	 pr_tabla pr_temporada fecha  flagF identificador					
				
        '''
        fecha = ""
        nombreArchivo = ""
        token = self.sacarToken()
        if token.tipo == "pr_TABLA":
            ########## TEMPORADA ###########
            token = self.sacarToken()
            if token is None:
                self.agregarError("pr_TEMPORADA","EOF")
            elif token.tipo == "pr_TEMPORADA":
                ###### MENOR QUE ########
                           token = self.sacarToken()
                           if token is None:
                               self.agregarError("menorQue","EOF")
                           elif token.tipo == "menorQue":
                                ###### ENTERO #########
                                token = self.sacarToken()
                                if token is None:
                                    self.agregarError("entero{4}","EOF")
                                elif token.tipo == "entero" and len(token.lexema) == 4:
                                    fecha += token.lexema
                                    ##### GUION #####
                                    token = self.sacarToken()
                                    if token is None:
                                       self.agregarError("guion","EOF")
                                    elif token.tipo == "guion":
                                        fecha += token.lexema
                                        ###### ENTERO #########
                                        token = self.sacarToken()
                                        if token is None:
                                            self.agregarError("entero{4}","EOF")
                                        elif token.tipo == "entero" and len(token.lexema) == 4:
                                            fecha += token.lexema
                                            ##### MAYOR QUE ##### 
                                            token = self.sacarToken()
                                            if token is None:
                                                self.agregarError("mayorQue","EOF")
                                            elif token.tipo == "mayorQue":
                                                ######## EOF | ARCHIVO #######
                                                token = self.sacarToken()
                                                if token is None:
                                                    print("Fecha->",fecha)
                                                elif token.tipo == "flagFile":
                                                        ##### IDENTIFICADOR ######
                                                        token = self.sacarToken()
                                                        if token is None:
                                                            self.agregarError("identificador","EOF")
                                                        elif token.tipo == "identificador":
                                                            nombreArchivo = token.lexema
                                                            ######## EOF #######
                                                            token = self.sacarToken()
                                                            if token is None:
                                                                print("Fecha->",fecha)
                                                                print("Nombre Archivo->",nombreArchivo)
                                                            else:
                                                                self.agregarError("EOF",token.tipo)
                                                        else:
                                                            self.agregarError("identificador",token.tipo)
                                                        
                                                else:
                                                    self.agregarError("flagFile",token.tipo)    
                                                    
                                            else:
                                                self.agregarError("mayorQue",token.tipo)
                                        
                                        elif token.tipo == "entero":
                                            self.agregarError("entero{4}",f"entero[{len(token.lexema)}]")
                                        else:
                                            self.agregarError("entero{4}",token.tipo)
                                            
                                    else:
                                        self.agregarError("guion",token.tipo)       
                                    
                                elif token.tipo == "entero":
                                    self.agregarError("entero{4}",f"entero[{len(token.lexema)}]")
                                else:
                                    self.agregarError("entero{4}",token.tipo)      
                                
                           else:
                               self.agregarError("menorQue",token.tipo)
                           
                
            else:
                self.agregarError("pr_TEMPORADA",token.tipo)
        else:
            self.agregarError("pr_TABLA","EOF")
            
    def PARTIDOS(self):
        '''
        PARTIDOS	::=	pr_partidos equipo pr_temporada fecha flagF identificador	 																	
	                |	pr_partidos equipo pr_temporada fecha flagF identificador flagApartir numero flagHasta entero{2}									
        '''
        equipo = None
        fecha = ""
        nombreArchivo = None
        aPartir = 0
        hasta = 0
        
        token = self.sacarToken()
        if token.tipo == "pr_PARTIDOS":
            token = self.sacarToken()
            ####### COMILLA ########
            if token is None:
                self.agregarError("comilla","EOF")
            elif token.tipo == "comilla":
                equipo = self.armarCadena()
                
                if equipo != "EOF":
                    print("Equipo->",equipo)
                    ######## TEMPORADA #########
                    token = self.sacarToken()
                    if token is None:
                        self.agregarError("pr_TEMPORADA","EOF")
                    elif token.tipo == "pr_TEMPORADA":
                        ###### MENOR QUE ########
                           token = self.sacarToken()
                           if token is None:
                               self.agregarError("menorQue","EOF")
                           elif token.tipo == "menorQue":
                                ###### ENTERO #########
                                token = self.sacarToken()
                                if token is None:
                                    self.agregarError("entero{4}","EOF")
                                elif token.tipo == "entero" and len(token.lexema) == 4:
                                    fecha += token.lexema
                                    ##### GUION #####
                                    token = self.sacarToken()
                                    if token is None:
                                       self.agregarError("guion","EOF")
                                    elif token.tipo == "guion":
                                        fecha += token.lexema
                                        ###### ENTERO #########
                                        token = self.sacarToken()
                                        if token is None:
                                            self.agregarError("entero{4}","EOF")
                                        elif token.tipo == "entero" and len(token.lexema) == 4:
                                            fecha += token.lexema
                                            ##### MAYOR QUE ##### 
                                            token = self.sacarToken()
                                            if token is None:
                                                self.agregarError("mayorQue","EOF")
                                            elif token.tipo == "mayorQue":
                                               ######## EOF | ARCHIVO #######
                                                token = self.sacarToken()
                                                if token is None:
                                                    print("Equipo->",equipo)
                                                    print("Fecha->",fecha)
                                            
                                                elif token.tipo == "flagFile":
                                                        ##### IDENTIFICADOR ######
                                                        token = self.sacarToken()
                                                        if token is None:
                                                            self.agregarError("identificador","EOF")
                                                        elif token.tipo == "identificador":
                                                            nombreArchivo = token.lexema
                                                            ######## EOF #######
                                                            token = self.sacarToken()
                                                            if token is None:
                                                                print("Equipo->",equipo)
                                                                print("Fecha->",fecha)
                                                                print("Nombre Archivo->",nombreArchivo)
                                                                ######### FLAG A PARTIR ########
                                                            elif token.tipo == "flagApartir":
            
                                                                    ######## ENTERO ######### 
                                                                    token = self.sacarToken()
                                                                    if token is None:
                                                                        self.agregar("entero","EOF")
                                                                    elif token.tipo == "entero" and len(token.lexema) == 2:
                                                                        aPartir = token.lexema 
                                                                        
                                                                        ######### FLAG HASTA ########
                                                                        token = self.sacarToken()
                                                                        if token is None:
                                                                            self.agregarError("flagHasta","EOF")
                                                                        elif token.tipo == "flagHasta":
                                                                    
                                                                            ######## ENTERO ######### 
                                                                            token = self.sacarToken()
                                                                            if token is None:
                                                                                self.agregar("entero","EOF")
                                                                            elif token.tipo == "entero" and len(token.lexema) == 2:
                                                                                hasta = token.lexema 
                                                                                ####### EOF #########
                                                                                token = self.sacarToken()
                                                                                if token is None:
                                                                                    print("Equipo->",equipo)
                                                                                    print("Fecha->",fecha)
                                                                                    print("A partir->",aPartir)
                                                                                    print("Hasta->",hasta)
                                                                                else:
                                                                                    self.agregarError("EOF",token.tipo)    
                                                                                
                                                                        
                                                                            elif token.tipo == "entero":
                                                                                self.agregarError("entero{2}",f"entero[{len(token.lexema)}]")
                                                                            else:
                                                                                self.agregarError("entero{2}",token.tipo)
                                                                        
        
                                                                        else:
                                                                            self.agregarError("flagHasta",token.tipo)
                                                                        
                                                                    elif token.tipo == "entero":
                                                                        self.agregarError("entero{2}",f"entero[{len(token.lexema)}]")
                                                                    else:
                                                                        self.agregarError("entero{2}",token.tipo)
                                                                        
        
                                                            else:
                                                                self.agregarError("flagApartir",token.tipo)
                                                                
                                                                
                                                                
                                                        else:
                                                            self.agregarError("identificador",token.tipo)
                                                        
                                                else:
                                                    self.agregarError("flagFile",token.tipo)    
                                                  
                                                    
                                            else:
                                                self.agregarError("mayorQue",token.tipo)
                                        
                                        elif token.tipo == "entero":
                                            self.agregarError("entero{4}",f"entero[{len(token.lexema)}]")
                                        else:
                                            self.agregarError("entero{4}",token.tipo)
                                            
                                    else:
                                        self.agregarError("guion",token.tipo)       
                                    
                                elif token.tipo == "entero":
                                    self.agregarError("entero{4}",f"entero[{len(token.lexema)}]")
                                else:
                                    self.agregarError("entero{4}",token.tipo)
                                    
                                    
                                
                           else:
                               self.agregarError("menorQue",token.tipo)
                           
                    else:
                        self.agregarError("pr_TEMPORADA",token.tipo)    
                else:
                    self.agregarError("comilla","EOF")    
            
        else:
            self.agregarError("pr_PARTIDOS","EOF")

    def TOP(self):
        '''
         Muestra el top (superior o inferior) de los equipos clasificados
            según los puntos conseguidos.
        
        Producción
                TOP	::=	pr_top con_superior pr_temporada fecha flagTop entero{2} 					
	                |	pr_top con_inferior pr_temporada fecha  flagTop entero{2}					
	                |	pr_top con_superior pr_temporada fecha 					
	                |	pr_top con_inferior pr_temporada fecha					

        '''
        token = self.sacarToken()
        condicion = None
        fecha = ""
        numero = 0
        
        if token.tipo == "pr_TOP":
            token = self.sacarToken()
            ######## CONDICION ##############
            
            if token is None:
                self.agregarError("condicionSUPERIOR | condicionINFERIOR","EOF")
            elif token.tipo == "condicionSUPERIOR" or token.tipo == "condicionINFERIOR":
                 condicion = token.lexema
                 ##### TEMPORADA ########
                 token = self.sacarToken()
                 if token is None:
                     self.agregarError("pr_TEMPORADA","EOF")
                 elif token.tipo == "pr_TEMPORADA":
                     ####### MENOR QUE ##########
                    token = self.sacarToken()
                    if token is None:
                        self.agregarError("menorQue","EOF")
                        return
                    elif token.tipo == "menorQue":
                        
                        ######## ENTERO ########
                        token = self.sacarToken()
                        if token is None:
                            self.agregarError("entero{4}","EOF")
                            return
                        elif token.tipo == "entero" and len(token.lexema) == 4:
                            fecha += token.lexema 
                            ###### GUION ######
                            token = self.sacarToken()
                            if token is None:
                                self.agregarError("guion","EOF")
                                return
                            elif token.tipo == "guion":
                                fecha += token.lexema
                                ######## ENTERO ########
                                token = self.sacarToken()
                                if token is None:
                                    self.agregarError("entero{4}","EOF")
                                    return
                                elif token.tipo == "entero" and len(token.lexema) == 4:
                                    fecha += token.lexema
                                    ###### MAYOR QUE ########
                                    token = self.sacarToken()
                                    if token is None:
                                        self.agregarError("mayorQue","EOF")
                                        return
                                    elif token.tipo == "mayorQue":
                                        
                                        ######## EOF | FLAG ARCHIVO ###### 
                                        token = self.sacarToken()
                                        if token is None:
                                            
                                            print(f"Fecha {fecha}")
                                        elif token.tipo == "flagTop":
                                            
                                            ######### ENTERO ########
                                            token = self.sacarToken()
                                            if token is None:
                                                self.agregarError("entero{2}","EOF")
                                                return
                                            elif token.tipo == "entero" and len(token.lexema) == 2:
                                                numero = token.lexema
                                                ######### EOF ########
                                                token = self.sacarToken()
                                                if token is None:
                                                    print(f"Numero: {numero}")
                                                    print(f"Fecha {fecha}")
                                                
                                                else:
                                                    self.agregarError("EOF",token.tipo)
                                                    return 
                                                    
                                                
                                            elif token.tipo == "entero":
                                                self.agregarError("entero{2}",f"entero[{len(token.lexema)}]")
                                                return 
                                            else:
                                                self.agregarError("entero{2}",token.tipo)
                                                return
                                            
                                            
                                            
                                            
                                        else:
                                            self.agregarError("flagTop",token.tipo)
                                            return 
                                            
                                                
                                            
                                    else:
                                        self.agregarError("mayorQue",token.tipo)
                                        return 
                                        
                                elif token.tipo == "entero":
                                    self.agregarError("entero{4}",f"entero[{len(token.lexema)}]")
                                    return
                                else:
                                    self.agregarError("entero",token.tipo)
                                    return    
                                    
                                
                            
                            else:
                                self.agregarError("guion",token.tipo)
                                return
                            
                        elif token.tipo == "entero":
                            self.agregarError("entero{4}",f"entero[{len(token.lexema)}]")
                            return
                        else:
                            self.agregarError("entero",token.tipo)
                            return
                        
                        
                    else:
                        self.agregarError("menorQue",token.tipo)
                        return
                     
                 else:
                     self.agregarError("pr_TEMPORADA",token.tipo)    
            else:
                self.agregarError("condicionSUPERIOR | condicionINFERIOR","EOF")   
            
        else:
            self.agregarError("pr_TOP","EOF")    
                  
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
        
            
            
        
        
                
            
        
                 
    