import operator
import csv
import string
class Validacion():


    def ValidarArchivo(archivo):
        try:
            with open(archivo) as archivo_csv:
                return True

        except FileNotFoundError:
            return False

    def ValidarCampos(lista):
        try:
            for i in lista:
                if len(i) == 5:
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
            leer_archivo = csv.reader(csv_file)
            campos = []
            for campo_lista in leer_archivo:
                campos.append(campo_lista)
            return campos
    def DicCampos(campos):
        cliente = []
        codigo = []
        producto = []
        cantidad = []
        precio = []
        for lista in campos:
            codigo.append(lista[0])
            producto.append(lista[1])
            cliente.append(lista[2])
            cantidad.append(lista[3])
            precio.append(lista[4])
        dic_campos = {}
        dic_campos['cliente']= cliente
        dic_campos['codigo']= codigo
        dic_campos['producto']= producto
        dic_campos['cantidad']= cantidad
        dic_campos['precio']= precio
        return  dic_campos

class Utilidad():

    def CombinarNombre(nombre,apellido): # combina nombre y apellido capitalizados
        try:
            nombre_completo = nombre.strip().capitalize() +' '+ apellido.strip().capitalize()
            return nombre_completo
        except:
            return False

    def OrdenarDiccionario(diccionario):
        try:
            diccionario = sorted(diccionario.items(),key=operator.itemgetter(1))
            return diccionario

        except:
            return False

    def CompradoPorCliente(nombre,cliente,codigo,producto):
        try:
            indice= []
            for contador, consulta in enumerate(cliente):
                if consulta == nombre:
                    indice.append(contador)
            cod = []
            pro = []
            for i in indice:
                cod.append(codigo[i])
                pro.append(producto[i])
            productos_comprados_por_cliente = {}
            productos_comprados_por_cliente['producto'] = pro
            productos_comprados_por_cliente['codigo']= cod
            return productos_comprados_por_cliente

        except:
            return False

    def ClientesPorProducto(num_cod,codigo,cliente,producto):
        try:
            indice= []
            for contador, consulta in enumerate(codigo):
                if consulta == num_cod:
                    indice.append(contador)
            nombre_producto = producto[indice[0]]
            nombres = []
            for i in indice:
                nombres.append(cliente[i])
            producto_con_lista_clientes = {}
            producto_con_lista_clientes['clientes']= nombres
            producto_con_lista_clientes['producto']= nombre_producto
            return producto_con_lista_clientes
        except:
            return False

    def TopClientes(cliente,archivo_csv):
        try:
            list_nombre = []
            list_gasto = []
            for nombre in cliente: # para nombre el nombre de la lista cliente
                if nombre in list_nombre:
                    continue
                for i in archivo_csv[1:]: # para i la lista de campos

                    if nombre in i: # si nombre esta en i(la lista de campos)
                        if nombre in list_nombre: # si nombre(uno de la lista de clientes) esta en list_nombre
                            indice = list_nombre.index(nombre) # indice guarda el numero de posicion
                            list_gasto[indice] = list_gasto[indice] + float(i[3]) * float(i[4]) # cambia el valor que ya tenia list_gasto

                        else: # si no esta nombre en i (la lista de campos)
                            list_nombre.append(nombre) # se debe agregar nombre a list_nombre
                            list_gasto.append(float(i[3]) * float(i[4])) # se debe agregar los gastos a list_gasto
            cliente_gasto = [list_nombre,list_gasto]
            return cliente_gasto
        except:
            return False

    def TopProductos(prducto,archivo_csv):
        try:
            list_producto = []
            list_cantidad = []
            for nombre in prducto: # para nombre el nombre de la lista cliente
                if nombre in list_producto:
                    continue
                for i in archivo_csv[1:]: # para i la lista de campos
                    if nombre in i: # si nombre esta en i(la lista de campos)
                        if nombre in list_producto: # si nombre(uno de la lista de clientes) esta en list_producto
                            indice = list_producto.index(nombre) # indice guarda el numero de posicion
                            list_cantidad[indice] = list_cantidad[indice] + int(i[3]) # cambia el valor que ya tenia list_cantidad
                        else: # si no esta nombre en i (la lista de campos)
                            list_producto.append(nombre) # se debe agregar nombre a list_producto
                            list_cantidad.append(int(i[3])) # se debe agregar los gastos a list_cantidad
            producto_cantidad = [list_producto,list_cantidad]
            return producto_cantidad
        except:
            return False

    def OrdenarListasProductosCantidad(producto,cantidad):
        try:
            for i in range(len(cantidad)):
                for x in range(len(cantidad)-1):
                    if int(cantidad[x]) < int(cantidad[x+1]):
                        aux1= int(cantidad[x])
                        cantidad[x] = int(cantidad[x+1])
                        cantidad[x+1]= aux1
                        aux2=producto[x]
                        producto[x]=producto[x+1]
                        producto[x+1]=aux2
            dic = {}
            dic['producto'] = producto
            dic['cantidad'] = cantidad
            return dic
        except:
            return False

    def OrdenarListasClienteGastos(cliente,gastos):
        try:
            for i in range(len(cliente)):
                for x in range(len(cliente)-1):
                    if float(gastos[x]) < float(gastos[x+1]):
                        aux1= float(gastos[x])
                        gastos[x] = float(gastos[x+1])
                        gastos[x+1]= aux1
                        aux2=cliente[x]
                        cliente[x]=cliente[x+1]
                        cliente[x+1]=aux2
            dic = {}
            dic['cliente'] = cliente
            dic['gasto'] = gastos
            return dic
        except:
            return False
