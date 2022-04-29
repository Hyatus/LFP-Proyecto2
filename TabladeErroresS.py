import os

def generarTablaErroresS(listadeErroresS):
    
    encabezado = '''
        <!DOCTYPE html>
        <html>
        <head>
	    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
	    <title>Tabla de Tokens</title>
        <link rel="stylesheet" type="text/css" href="estilo.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@500&family=Roboto:wght@700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        </head>
        <body>
        <h1> ERRORES SINTACTICOS </h1>
        <h3>Nombre: Cristian Alexander Mejia Cahuec Carnet: 201807085</h3><br>
        <br>
        <br>
        <br>
        '''
        
    
        
        
    tabla = '''
            <table class="table table-hover">
            <thead>
            <tr>
            <th scope="col">#</th>
            <th scope="col">Descripcion</th>
            </tr>
            </thead>
            <tbody>
            '''
             
    final = ''' 
           </body>
           </html> 
            '''
    
    file = open('TablaErroresS.html',"w")
    file.write(encabezado)
    file.write(tabla)
    
    contadorFila = 1
    for error in listadeErroresS:      
        fila = f'''
                   <tr>
                   <th scope="row">{contadorFila}</th>
                   <td>{error}</td>
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
    

