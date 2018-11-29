#!/usr/bin/env python
import operator
import csv
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_bootstrap import Bootstrap
# from flask_moment import Moment
from flask_script import Manager
from forms import LoginForm, SaludarForm, RegistrarForm
from mis_clases import Validacion, Archivo, Utilidad

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
# moment = Moment(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'


@app.route('/')
def index():
    return render_template('index.html',nombre='Inicio', fecha_actual=datetime.utcnow())


@app.route('/saludar', methods=['GET', 'POST'])
def saludar():
    formulario = SaludarForm()
    if formulario.validate_on_submit():
        print(formulario.usuario.name)
        return redirect(url_for('saludar_persona', usuario=formulario.usuario.data))
    return render_template('saludar.html', form=formulario)


@app.route('/saludar/<usuario>')
def saludar_persona(usuario):
    return render_template('usuarios.html', nombre=usuario)


@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            usuarios_csv = csv.reader(archivo)
            registro = next(usuarios_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido')
                    session['username'] = formulario.usuario.data
                # Ingreso de usuario

                # Ingresar a TABLA DE VENTAS
                    if Validacion.ValidarArchivo('tabla.csv'):
                        archivo_csv = Archivo.AbrirComoLista('tabla.csv')
                        cliente = []
                        codigo = []
                        producto = []
                        cantidad = []
                        precio = []
                        for lista in archivo_csv:
                            codigo.append(lista[0])
                            producto.append(lista[1])
                            cliente.append(lista[2])
                            cantidad.append(lista[3])
                            precio.append(lista[4])
                        rango = len(codigo)
                        # Validacion de campos
                        if Validacion.ValidarCampoCodigo(codigo[1:]) == False:
                            return render_template('no_valido.html' , mensaje = 'El campo CODIGO debe estar compuesto por 3 letras máyusculas seguidas de 3 caracteres númericos')
                        elif Validacion.ValidarCampoCantidad(cantidad[1:]) == False:
                            return render_template('no_valido.html' , mensaje = 'El campo CANTIDAD solo permite números enteros')
                        elif Validacion.ValidarCampoPrecio(precio[1:]) == False:
                            return render_template('no_valido.html' , mensaje = 'El campo PRECIO solo premite números decimales')
                        elif Validacion.ValidarCampos(archivo_csv) == False:
                            return render_template('no_valido.html' , mensaje= 'Verifique la cantidad de CAMPOS ingresados  en su archivo CSV')
                        else:
                            return render_template('tabla.html',nombre= 'Tabla de Ventas',nameParametro = 'TABLA', campo1 = codigo, campo2 = producto,campo3 = cliente,
                            campo4 = cantidad, campo5 = precio, rango= rango)
                    else:
                        return render_template('no_valido.html', mensaje= 'El csv archivo inexistente')
                registro = next(usuarios_csv, None)
            else:
                flash('Revisá nombre de usuario y contraseña')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)

@app.route('/compra_cliente', methods=["GET", 'POST'])
def compra_cliente():
    if request.method == 'POST':
        nombre_cliente = request.form['nombre']
        apellido_cliente = request.form['apellido']
        nombre_completo = Utilidad.CombinarNombre(nombre_cliente,apellido_cliente)
        if nombre_completo == False:
            return render_template('no_valido.html', mensaje= 'Error al ingresar los datos del cliente')
        archivo_csv = Archivo.AbrirComoLista('tabla.csv')
# crea un diccionario que contiene en listas el contenido de los 5 campos
        dic_campos = Archivo.DicCampos(archivo_csv)
        if nombre_completo in dic_campos['cliente']:
# se crea un diccionario con 2 que contiene 2 listas una con los nombres de los productos y otra con los codigos
            cliente_1 = Utilidad.CompradoPorCliente(nombre_completo,dic_campos['cliente'],dic_campos['codigo'],dic_campos['producto'])
            return render_template('compra_cliente.html', nombre_completo = nombre_completo ,codigo = cliente_1['codigo']
            ,producto = cliente_1['producto'] ,rango = len(cliente_1['codigo']))
        else:
            return render_template('no_valido.html', mensaje='No se registran clientes con el nombre {}'.format(nombre_completo))
    return render_template('sin_permiso.html')

@app.route('/clientes_por_producto', methods=["GET", 'POST'])
def clientes_por_producto():
    if request.method == 'POST':
        codigo_producto = request.form['codigo']
        codigo_producto = codigo_producto.upper()
        if codigo_producto == False:
            return render_template('no_valido.html', mensaje= 'Error en el código del producto')
        archivo_csv = Archivo.AbrirComoLista('tabla.csv')
# crea un diccionario que contiene en listas el contenido de los 5 campos
        dic_campos = Archivo.DicCampos(archivo_csv)
        if codigo_producto in dic_campos['codigo']:
# se crea un diccionario con 1 string con el nombre del producto y una lista con los nombres de los clientes
            dicc = Utilidad.ClientesPorProducto(codigo_producto,dic_campos['codigo'],dic_campos['cliente'],dic_campos['producto'])
            nombre_producto = dicc['producto']
            lista_clientes = dicc['clientes']
            return render_template('clientes_por_producto.html', codigo_producto = codigo_producto , nombre_producto = nombre_producto
            ,lista_clientes = lista_clientes ,rango = len(lista_clientes))
        else:
            return render_template('no_valido.html', mensaje='El código {} no se encuentra registrado'.format(codigo_producto))
    return render_template('sin_permiso.html')

@app.route('/mejores_clientes',methods=["GET", 'POST'])
def mejores_clientes():
    if request.method == 'POST':
        archivo_csv = Archivo.AbrirComoLista('tabla.csv')
    # crea un diccionario que contiene en listas el contenido de los 5 campos
        dic_campos = Archivo.DicCampos(archivo_csv)
    # se crea un diccionario con 1 string con el nombre del producto y una lista con los nombres de los clientes
        cliente_gasto = Utilidad.TopClientes(dic_campos['cliente'],archivo_csv)
    # se ordenan las listas de mayor a menor segun los gastos de los clientes
        dic_cliente_gasto = Utilidad.OrdenarListasClienteGastos(cliente_gasto[0],cliente_gasto[1])
        rango = len(cliente_gasto[0])
        return render_template('mejores_clientes.html',lista_clientes = dic_cliente_gasto['cliente'], lista_gastos = dic_cliente_gasto['gasto'], rango = rango)
    else:
        return render_template('sin_permiso.html')

@app.route('/productos_mas_vendidos',methods=["GET", 'POST'])
def productos_mas_vendidos():
    if request.method == 'POST':
        archivo_csv = Archivo.AbrirComoLista('tabla.csv')
    # crea un diccionario que contiene en listas el contenido de los 5 campos
        dic_campos = Archivo.DicCampos(archivo_csv)
    # se crea un diccionario con 1 string con el nombre del producto y una lista con los nombres de los clientes
        producto_cantidad = Utilidad.TopProductos(dic_campos['producto'],archivo_csv)
    # se ordenan las listas de mayor a menor segun la cantidad de ventas
        dic_prod_cantidad = Utilidad.OrdenarListasProductosCantidad(producto_cantidad[0],producto_cantidad[1])
        rango = len(producto_cantidad[0])
        return render_template('productos_mas_vendidos.html',lista_productos = dic_prod_cantidad['producto'],
         lista_cantidad = dic_prod_cantidad['cantidad'], rango = rango)
    else:
        return render_template('sin_permiso.html')



@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', form=formulario)


@app.route('/secret', methods=['GET'])
def secreto():
    if 'username' in session:
        return render_template('private.html', username=session['username'])
    else:
        return render_template('sin_permiso.html')


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    #app.run(host='0.0.0.0', debug=True)
    manager.run()
