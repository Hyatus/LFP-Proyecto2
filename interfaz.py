import sys
from PySide2 import QtCore, QtWidgets, QtGui
import easygui
from AnalizadorLexico import *
from AnalizadorSintactico import *
import os
import pandas as pd
from TabladeErrores import *
from TabladeTokens import *
from TabladeErroresS  import *


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.df = pd.read_csv('DOCUMENTACION\LaLigaBot-LFP.csv')
        #print(self.df.head())
        self.listadeTokensT = []
        self.listadeErroresT = []
        self.errores = [] 
        self.button = QtWidgets.QPushButton("ENVIAR")
        self.button2 = QtWidgets.QPushButton("LIMPIAR LOG")
        self.text = QtWidgets.QLabel("PROYECTO 2 LENGUAJES FORMALES DE PROGRAMACION",
                                     alignment=QtCore.Qt.AlignCenter)
        self.plainTextEdit = QtWidgets.QTextEdit()
        self.insertText = QtWidgets.QLineEdit()
        self.comboX = QtWidgets.QComboBox()
        self.comboX.addItem("REPORTES")
        self.comboX.addItem("REPORTE DE TOKENS")
        self.comboX.addItem("REPORTE DE ERRORES")
        self.comboX.addItem("REPORTE DE ERRORES S.")
        self.comboX.addItem("MANUAL DE USUARIO")
        self.comboX.addItem("MANUAL TECNICO")
        self.comboX.activated.connect(self.funcionCombo)
        
        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.plainTextEdit)
        self.layout.addWidget(self.insertText)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.comboX)
        self.setLayout(self.layout)
        self.textoInicial()
        self.button.clicked.connect(self.magic)
        self.button2.clicked.connect(self.limpiarLog)
    
    def funcionCombo(self):
        opcion = self.comboX.currentText()
        if opcion == "REPORTE DE TOKENS":
            generarTablaTokens(self.listadeTokensT)
            os.system("TablaTokens.html")
        if opcion == "REPORTE DE ERRORES":
            generarTablaErrores(self.listadeErroresT)
            os.system("TablaErrores.html")
        if opcion == "MANUAL DE USUARIO":
            os.system("MANUAL_U.pdf")
        if opcion == "MANUAL TECNICO":
            os.system("MANUAL_T.pdf")
        if opcion == "REPORTE DE ERRORES S.":
            generarTablaErroresS(self.errores)
            os.system("TablaErroresS.html")
    
    
    @QtCore.Slot()
    def limpiarLog(self):
        self.listadeErroresT.clear()
        self.listadeTokensT.clear()
        self.errores.clear()
        
    @QtCore.Slot()
    def magic(self):
        
        entrada = self.insertText.text()
        
    
        self.textoDerecha(entrada)
    
        lexico = AnalizadorLexico()
        
        

        lexico.analizar(entrada)
        
        listaTokens = lexico.listaTokens
        listaErrores = lexico.listaErrores
        
        self.listadeTokensT.extend(lexico.listaTokens)
        self.listadeErroresT.extend(lexico.listaErrores)
        
        print(self.listadeTokensT)
        print(self.listadeErroresT)
        
        self.imprimirTokensT()
        self.imprimirErroresT()
        
        
        #print("LISTA TOKENS")
        #lexico.imprimirTokens()
        #print("LISTA ERRORES ")
        #lexico.imprimirErrores()
    
    
        self.AnalizadorSintactico(listaTokens)
        self.analizar()
        print("ERRORES SINTACTICOS")
        self.imprimirErrores()
        
    def imprimirTokensT(self):
      x = PrettyTable()
      x.field_names = ["lexema","linea","columna","tipo"]
      for token in self.listadeTokensT:
        x.add_row([token.lexema,token.linea,token.columna,token.tipo])
      print(x)

    def imprimirErroresT(self):
      x = PrettyTable()
      x.field_names = ["Descripción","linea","columna"]
      for error in self.listadeErroresT:
        x.add_row([error.descripcion,error.linea,error.columna])
      print(x)
      
    def textoInicial(self):
        self.plainTextEdit.insertPlainText("Bienvenido a la Liga Bot.Ingrese un comando")
        self.plainTextEdit.setAlignment(QtCore.Qt.AlignLeft)
    
    def textoDerecha(self,cadena):
        self.plainTextEdit.insertPlainText("\n\n"+cadena)
        self.plainTextEdit.setAlignment(QtCore.Qt.AlignRight)
        
    ################# ANALIZADOR SINTACTICO ##############################    
    def AnalizadorSintactico(self,tokens:list):
        #self.errores = []
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
             self.plainTextEdit.insertPlainText(f"\n\nADIOS")
             self.plainTextEdit.setAlignment(QtCore.Qt.AlignLeft)    
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
                             
                             ##### TOKEN TEMPORADA ########
                             token = self.sacarToken()
                             if token is None:
                                 self.agregarError("pr_TEMPORADA","EOF")
                             elif token.tipo == "pr_TEMPORADA":
                                 ###### MENOR QUE #########
                                 token = self.sacarToken()
                                 if token is None:
                                     self.agregarError("menorQue","EOF")
                                 elif token.tipo == "menorQue":
                                     ######### ENTERO ###########
                            
                                     token = self.sacarToken()
                                     if token is None:
                                         self.agregarError("entero{4}","EOF")
                                     elif token.tipo == "entero" and len(token.lexema) == 4:
                                         fecha += token.lexema
                                         ###### GUION #######
                                         token = self.sacarToken()
                                         if token is None:
                                             self.agregarError("guion","EOF")
                                         elif token.tipo == "guion":
                                             fecha += token.lexema
                                    
                                             ######### ENTERO ###########
                                             token = self.sacarToken()
                                             if token is None:
                                                self.agregarError("entero{4}","EOF")
                                             elif token.tipo == "entero" and len(token.lexema) == 4:
                                                fecha += token.lexema
                                                ######## MAYOR QUE ############
                                                token = self.sacarToken()
                                                if token is None:
                                                    self.agregarError("mayorQue","EOF")
                                                elif token.tipo == "mayorQue":
                                                    ######## EOF ############
                                                    token = self.sacarToken()
                                                    if token is None:
                                                        #print("Fecha->",fecha)
                                                        #print("Equipo1->",equipo1.strip())
                                                        #print("Equipo2->",equipo2.strip())
                                                        df2 = self.df[(self.df['Temporada']==fecha) & (self.df['Equipo1'] == equipo1.strip()) & (self.df['Equipo2'] == equipo2.strip()) ]
                                                        goles2 = df2.iloc[0,6]
                                                        goles1 = df2.iloc[0,5]
                
                                                        print(self.df[(self.df['Temporada']==fecha) & (self.df['Equipo1'] == equipo1.strip()) & (self.df['Equipo2'] == equipo2.strip()) ])
                                                        self.plainTextEdit.insertPlainText(f"\n\nEl Resultado de este partido fue: {equipo1} {goles1} - {equipo2} {goles2}")
                                                        self.plainTextEdit.setAlignment(QtCore.Qt.AlignLeft)
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
                                            self.func_JORNADA(int(numero),fecha)
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
                                                    self.func_JORNADA(int(numero),fecha,nombreArchivo)
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
    
    def func_JORNADA(self,numero,fecha,nombreArchivo = "jornada"):
        self.plainTextEdit.insertPlainText(f"\n\nGenerando archivo de resultados jornada {numero} temporada {fecha}")
        self.plainTextEdit.setAlignment(QtCore.Qt.AlignLeft)
        df2 = self.df[((self.df['Jornada']==numero) & (self.df['Temporada'] == fecha)) ]
        print(df2)
        nombreArchivo += ".html"
        encabezado = f'''
        <!DOCTYPE html>
        <html>
        <head>
	    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
	    <title>Tabla de Errores</title>
        <link rel="stylesheet" type="text/css" href="estilo.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@500&family=Roboto:wght@700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        </head>
        <body>
        <h1> RESULTADOS JORNADA {numero} TEMPORADA {fecha} </h1>
        <br>
        <br>
        <br>
        '''
        
        tabla = '''
            <table class="table table-hover">
            <thead>
            <tr>
            <th scope="col">#</th>
            <th scope="col">FECHA</th>
            <th scope="col">TEMPORADA</th>
            <th scope="col">JORNADA</th>
            <th scope="col">EQUIPO 1</th>
            <th scope="col">EQUIPO 2</th>
            <th scope="col">GOLES 1</th>
            <th scope="col">GOLES 2</th>
            </tr>
            </thead>
            <tbody>
            '''
             
        final = ''' 
           </body>
           </html> 
            '''
    
        file = open(nombreArchivo,"w")
        file.write(encabezado)
        file.write(tabla)
    
        contadorFila = 1
        for i in df2.index:     
            fechaT = df2["Fecha"][i] 
            temporadaT = df2["Temporada"][i]
            jornadaT = df2["Jornada"][i]
            equipo1T = df2["Equipo1"][i]
            equipo2T = df2["Equipo2"][i]
            goles1T = df2["Goles1"][i]
            goles2T = df2["Goles2"][i]
            
            fila = f'''
                   <tr>
                   <th scope="row">{contadorFila}</th>
                   <td>{fechaT}</td>
                   <td>{temporadaT}</td>
                   <td>{jornadaT}</td>
                   <td>{equipo1T}</td>
                   <td>{equipo2T}</td>
                   <td>{goles1T}</td> 
                   <td>{goles2T}</td>
                   </tr>
               '''
            file.write(fila)   
            contadorFila +=1
        
   
        finalTabla = '''
                    </tbody>
                    </table>
                 '''
                 

       
        file.write(finalTabla)      
  
        file.write(final)
        file.close()
        
        os.system(f"{nombreArchivo}")

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
                                                    self.func_GOLES(condicion,equipo.strip(),fecha)
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
    
    def func_GOLES(self,condicion,equipo,fecha):
        if condicion == "LOCAL":
            goles = 0
            df2 = self.df[((self.df['Equipo1']==equipo) & (self.df['Temporada'] == fecha)) ]
            print(df2)
            
            for i in df2.index:
                  goles += int(df2["Goles1"][i])
            
            self.plainTextEdit.insertPlainText(f"\n\nLos goles anotados por el {equipo} en total en la temporada {fecha} fueron {goles}")
            self.plainTextEdit.setAlignment(QtCore.Qt.AlignLeft)
            #print("GOLES",str(goles))
        elif condicion == "VISITANTE":
            goles = 0
            df2 = self.df[((self.df['Equipo2']==equipo) & (self.df['Temporada'] == fecha)) ]
            print(df2)
            
            for i in df2.index:
                  goles += int(df2["Goles2"][i])
           
            self.plainTextEdit.insertPlainText(f"\n\nLos goles anotados por el {equipo} en total en la temporada {fecha} fueron {goles}")
            self.plainTextEdit.setAlignment(QtCore.Qt.AlignLeft)
            
        elif condicion == "TOTAL":
            goles = 0
            df2 = self.df[((self.df['Equipo1']==equipo) & (self.df['Temporada'] == fecha)) ]
            print(df2)
            
            for i in df2.index:
                  goles += int(df2["Goles1"][i])
                  
            df2 = self.df[((self.df['Equipo2']==equipo) & (self.df['Temporada'] == fecha)) ]
            print(df2)
            
            for i in df2.index:
                  goles += int(df2["Goles2"][i])
           
            self.plainTextEdit.insertPlainText(f"\n\nLos goles anotados por el {equipo} en total en la temporada {fecha} fueron {goles}")
            self.plainTextEdit.setAlignment(QtCore.Qt.AlignLeft)
          
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
                                                    self.func_TABLA(fecha)
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
                                                                self.func_TABLA(fecha,nombreArchivo)
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

    def func_TABLA(self,fecha,nombreArchivo="temporada"):   
        nombreArchivo += ".html"
        df2 = self.df[((self.df['Temporada'] == fecha))]
        #print(df2) 
        
        listaEquipos = df2['Equipo1'].unique().tolist()
        print(listaEquipos)
        listaPuntos = []
        
        for equipo in listaEquipos:
            puntos = 0
            for i in df2.index:
                if df2["Equipo1"][i] == equipo:
                    if df2["Goles1"][i] > df2["Goles2"][i]:
                        puntos += 3
                    elif df2["Goles1"][i] == df2["Goles2"][i]:
                        puntos += 1
            
            for i in df2.index:
                if df2["Equipo2"][i] == equipo:
                    if df2["Goles2"][i] > df2["Goles1"][i]:
                        puntos += 3
                    elif df2["Goles2"][i] == df2["Goles1"][i]:
                        puntos += 1            
        
                                      
            listaPuntos.append(puntos)
        
        print(listaPuntos)        
        
        dfTabla = pd.DataFrame(list(zip(listaEquipos,listaPuntos)), columns = ['Equipo','Puntos']) 
        
        dfTabla.sort_values('Puntos',ascending=False,inplace=True)
        
        self.plainTextEdit.insertPlainText(f"\n\nGenerando archivo de clasificación de temporada {fecha}")
        self.plainTextEdit.setAlignment(QtCore.Qt.AlignLeft)
        
        encabezado = f'''
        <!DOCTYPE html>
        <html>
        <head>
	    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
	    <title>Tabla de Errores</title>
        <link rel="stylesheet" type="text/css" href="estilo.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@500&family=Roboto:wght@700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        </head>
        <body>
        <h1> CLASIFICACION DE TEMPORADA {fecha} </h1>
        <br>
        <br>
        <br>
        '''
        
        tabla = '''
            <table class="table table-hover">
            <thead>
            <tr>
            <th scope="col">#</th>
            <th scope="col">EQUIPO</th>
            <th scope="col">PUNTOS</th>
            </tr>
            </thead>
            <tbody>
            '''
             
        final = ''' 
           </body>
           </html> 
            '''
    
        file = open(nombreArchivo,"w")
        file.write(encabezado)
        file.write(tabla)
    
        contadorFila = 1
        
        for i in dfTabla.index:     
            equipoT = dfTabla["Equipo"][i] 
            puntosT = dfTabla["Puntos"][i]
            
            fila = f'''
                   <tr>
                   <th scope="row">{contadorFila}</th>
                   <td>{equipoT}</td>
                   <td>{puntosT}</td>
                   </tr>
               '''
            file.write(fila)   
            contadorFila +=1
        
   
        finalTabla = '''
                    </tbody>
                    </table>
                 '''
                 

       
        file.write(finalTabla)      
  
        file.write(final)
        file.close()
        
        os.system(f"{nombreArchivo}")

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
                                                    self.func_PARTIDOS(equipo.strip(),fecha)
                                            
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
                                                                self.func_PARTIDOS(equipo.strip(),fecha,nombreArchivo)
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
                                                                                    self.func_PARTIDOS(equipo.strip(),fecha,nombreArchivo,int(aPartir),int(hasta))
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
    
    def func_PARTIDOS(self,equipo,fecha,nombreArchivo = "partidos",apartir = 0,hasta = 0):
        
        df2 = None
        nombreArchivo += ".html"
        
        if apartir == 0 and hasta == 0:
            df2 = self.df[(self.df['Temporada']==fecha) & ((self.df['Equipo1'] == equipo) | (self.df['Equipo2'] == equipo) )]
            print(df2)
            
        else:
            df2 = self.df[(self.df['Temporada']==fecha) & ((self.df['Equipo1'] == equipo) | (self.df['Equipo2'] == equipo)) & (self.df['Jornada'] >= int(apartir)) & (self.df['Jornada'] <= int(hasta))  ]
            print(df2)
            
        
        encabezado = f'''
        <!DOCTYPE html>
        <html>
        <head>
	    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
	    <title>Tabla de Errores</title>
        <link rel="stylesheet" type="text/css" href="estilo.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@500&family=Roboto:wght@700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        </head>
        <body>
        <h1> RESULTADOS DE TEMPORADA {fecha} DEL {equipo}</h1>
        <br>
        <br>
        <br>
        '''
        
        tabla = '''
            <table class="table table-hover">
            <thead>
            <tr>
            <th scope="col">#</th>
            <th scope="col">FECHA</th>
            <th scope="col">TEMPORADA</th>
            <th scope="col">JORNADA</th>
            <th scope="col">EQUIPO 1</th>
            <th scope="col">EQUIPO 2</th>
            <th scope="col">GOLES 1</th>
            <th scope="col">GOLES 2</th>
            </tr>
            </thead>
            <tbody>
            '''
             
        final = ''' 
           </body>
           </html> 
            '''
    
        file = open(nombreArchivo,"w")
        file.write(encabezado)
        file.write(tabla)
    
        contadorFila = 1
        for i in df2.index:     
            fechaT = df2["Fecha"][i] 
            temporadaT = df2["Temporada"][i]
            jornadaT = df2["Jornada"][i]
            equipo1T = df2["Equipo1"][i]
            equipo2T = df2["Equipo2"][i]
            goles1T = df2["Goles1"][i]
            goles2T = df2["Goles2"][i]
            
            fila = f'''
                   <tr>
                   <th scope="row">{contadorFila}</th>
                   <td>{fechaT}</td>
                   <td>{temporadaT}</td>
                   <td>{jornadaT}</td>
                   <td>{equipo1T}</td>
                   <td>{equipo2T}</td>
                   <td>{goles1T}</td> 
                   <td>{goles2T}</td>
                   </tr>
               '''
            file.write(fila)   
            contadorFila +=1
        
   
        finalTabla = '''
                    </tbody>
                    </table>
                 '''
                 

       
        file.write(finalTabla)      
  
        file.write(final)
        file.close()
        
        os.system(f"{nombreArchivo}")
    
         
        
                 
        self.plainTextEdit.insertPlainText(f"\n\nGenerando archivo de resultados de temporada {fecha} del {equipo}")
        self.plainTextEdit.setAlignment(QtCore.Qt.AlignLeft)
    
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
                                            
                                            self.func_TOP(fecha,condicion)
                                            
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
                                                    self.func_TOP(fecha,condicion,int(numero))
                                                
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
      
    def func_TOP(self,fecha,condicion,numero=5):
        
        df2 = self.df[((self.df['Temporada'] == fecha))]
        print(df2) 
        
        listaEquipos = df2['Equipo1'].unique().tolist()
        print(listaEquipos)
        listaPuntos = []
        
        for equipo in listaEquipos:
            puntos = 0
            for i in df2.index:
                if df2["Equipo1"][i] == equipo:
                    if df2["Goles1"][i] > df2["Goles2"][i]:
                        puntos += 3
                    elif df2["Goles1"][i] == df2["Goles2"][i]:
                        puntos += 1
            
            for i in df2.index:
                if df2["Equipo2"][i] == equipo:
                    if df2["Goles2"][i] > df2["Goles1"][i]:
                        puntos += 3
                    elif df2["Goles2"][i] == df2["Goles1"][i]:
                        puntos += 1            
        
                                      
            listaPuntos.append(puntos)
        
        print(listaPuntos)        
        
        dfTabla = pd.DataFrame(list(zip(listaEquipos,listaPuntos)), columns = ['Equipo','Puntos']) 
        
        dfTabla.sort_values('Puntos',ascending=False,inplace=True)
        
        dfTabla.index.names = [None]
        dfTabla.reset_index(drop=True,inplace=True)
        
        if condicion == "SUPERIOR":
            self.plainTextEdit.setAlignment(QtCore.Qt.AlignCenter)
            self.plainTextEdit.insertPlainText(f"\n\n{dfTabla.head(numero)}")
        elif condicion == "INFERIOR": 
            self.plainTextEdit.setAlignment(QtCore.Qt.AlignCenter)
            self.plainTextEdit.insertPlainText(f"\n\n{dfTabla.tail(numero)}")   
             
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
        
                   
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(450, 600)
    widget.show()

    sys.exit(app.exec_())
        