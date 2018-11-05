import operator
import csv
class Validacion():
    

    def ValidarArchivo(archivo):
        try:
            with open(archivo) as archivo_csv:
                return True

        except FileNotFoundError:
            return False

    def ValidarCampos(lista):
        try:
            for i in range(len(lista)-1):
                if len(lista[i]) == 6:
                    condicion = True
                else:
                    condicion = False
                    if condicion == False:
                        break
            return condicion
        except:
            return False
        
    
    def ValidarCampoCodigo(lista):
        try:
            for valor in lista: 
                if valor[0:3].isupper() and valor[0:3].isalpha() and valor.isalnum() and valor[3:6].isdigit() and len(valor) == 6:
                    condicion = True            
                else:
                    condicion = False
                    if condicion == False:
                        break
            return condicion 
        except:
            return False

    def ValidarCampoCantidad(lista):
            try:
                for valor in lista:
                    if type(valor) == str:
                        numero = eval(valor)
                        if numero % 1 == 0:
                            condicion = True            
                        else:
                            condicion = False
                            if condicion == False:
                                break
                    elif valor % 1 == 0:
                        condicion = True
                    else:                
                        condicion = False
                        if condicion == False:
                            break   
                return condicion 
            except:
                return False

    def ValidarCampoPrecio(lista):
        try:
            for valor in lista:
                if float(valor) % 1 != 0:
                    condicion = True            
                else:
                    condicion = False
                    if condicion == False:
                        break
            return condicion 
        except:
            return False

class Archivo():

    def AbrirComoLista(archivo):
        with open(archivo) as csv_file:
            leer_archivo = csv.reader(csv_file, delimiter = ';')
            campos = []
            for campo_lista in leer_archivo:
                campos.append(campo_lista)
            return campos

class Utilidad():
    def CombinarNombre(nombre,apellido): # combina nombre y apellido capitalizados
        try:
            nombre_completo = nombre.capitalize() +' '+ apellido.capitalize()
            return nombre_completo
        except:
            return False
  
    def CapturarIndices(nombre,lista): # guarda los indices en una lista en los que aparece nombre
        try:
            consulta = nombre
            indice= []
            for contador, nombre in enumerate(lista):
                if consulta == nombre:
                    indice.append(contador)        
            return indice
        except:
            return False
    
    def IndicesPorCampos(indice,campo): # guarda en una lista los valores indicados por indice
        try:                            # del campo ingresado               
            lista = []
            for index in indice:
                lista.append(campo[index])
            return lista
        except:
            False   

    def ClienteCompras(nombre,indice,producto):
        try:
            cliente = {}
            compra = []
            for i in indice:
                compra.append(producto[i])
            cliente[nombre] = compra
            return cliente
        except:
            return False
    def ProductoClientes(codigo,indice,cliente):
        try:
            producto = {}
            compra = []
            for i in indice:
                compra.append(cliente[i])
            producto[codigo] = compra
            return producto
        except:
            return False

    def SumarCantidad(lista): # suma la cantidad de una lista producto determinado

            try:
                num = 0
                for valor in lista:
                    num = num + int(valor)
                return num
            except:
                return False
    def SumarPrecios(lista): # suma los precios de un cliente determinado
            try:
                num = 0.0
                for valor in lista:
                    num = num + float(valor)
                return num
            except:
                return False
    def CrearDiccionario(campo1,campo2):
        try:
            dicc = {}
            for i in range(len(campo1)):
                dicc[campo1[i]] = campo2[i] 
            return dicc
        except:
            return False

    def OrdenarDiccionario(diccionario):
        try:
            diccionario = sorted(diccionario.items(),key=operator.itemgetter(1))
            return diccionario
            
        except:
            return False
    def GastoCliente(cantidad,precio):
        try:
            gasto = []
            for i in range(1,len(cantidad)):
                gasto.append(float(cantidad[i]) * float(precio[i]))
            return gasto
        except:
            return False

# verificar que un elemento de la lista CLIENTE este en la lista y conseguir los indices
# mostrar todos los PRODUCTO con los mismos indices

# verificar que un elemento de la lista CODIGO este en la lista y conseguir los indices
# veridicar los indices con los de clientes y mostrarlos




