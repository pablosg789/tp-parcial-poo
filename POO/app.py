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
                    # creamos un diccionario por producto y cantidad
                        producto_cantidad = Utilidad.CrearDiccionario(producto,cantidad)
                        producto_cantidad = Utilidad.OrdenarDiccionario(producto_cantidad)
                        producto_cantidad.reverse()
                        print(producto_cantidad)
                    # creamos un diccionario por cliente y precio
                        gasto = Utilidad.GastoCliente(cantidad,precio)
                        print(gasto)

                        cliente_gasto = Utilidad.CrearDiccionario(cliente[1:],gasto)
                        cliente_gasto = Utilidad.OrdenarDiccionario(cliente_gasto)
                        cliente_gasto.reverse()
                        gasto.insert(0,'GASTO')
                        print(cliente_gasto)


                    # Validacion de campos

                        if Validacion.ValidarCampoCodigo(codigo[1:]) == False:
                            return render_template('no_valido.html' , mensaje = 'El campo CODIGO debe estar compuesto por 3 letras máyusculas seguidas de 3 caracteres númericos')
                        elif Validacion.ValidarCampoCantidad(cantidad[1:]) == False:
                            return render_template('no_valido.html' , mensaje = 'El campo CANTIDAD solo permite números enteros')
                        elif Validacion.ValidarCampoPrecio(precio[1:]) == False:
                            return render_template('no_valido.html' , mensaje = 'El campo PRECIO solo premite números decimales')
                        elif Validacion.ValidarCampos(archivo_csv) == False:
                            return render_template('no_valido.html' , mensaje= 'Verifique la cantidad de CAMPO')
                        else:
                            return render_template('tabla.html',nombre= 'Tabla de Ventas',nameParametro = 'TABLA', campo1 = codigo, campo2 = producto,campo3 = cliente,
                            campo4 = cantidad, campo5 = precio, rango= rango, producto_cantidad= producto_cantidad, cliente_gasto = cliente_gasto)
                    else:
                        return render_template('no_valido.html', mensaje= 'El csv archivo inexistente')

                registro = next(usuarios_csv, None)
            else:
                flash('Revisá nombre de usuario y contraseña')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)

@app.route('/consulta', methods=["GET", 'POST'])
def consulta():
    if request.method == 'POST':
        nombre_cliente = request.form['nombre']
        apellido_cliente = request.form['apellido']
        nombre_completo = Utilidad.CombinarNombre(nombre_cliente,apellido_cliente)
        print(nombre_completo)

        if nombre_completo == False:
            return render_template('no_valido.html', mensaje= 'Erro al ingresar los datos del cliente')
        codigo_producto = request.form['codigo']
        codigo_producto = codigo_producto.upper()


        if codigo_producto == False:
            return render_template('no_valido.html', mensaje= 'Error en el código del producto')
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
            
    # obtener indices de listas
        indices_cliente = Utilidad.CapturarIndices(nombre_completo,cliente)
        
    # creamos un diccionario con los productos que compro un cliente
        dicc_cliente = Utilidad.ClienteCompras(nombre_completo,indices_cliente,producto)
        productos_comprados = dicc_cliente[nombre_completo] 
        

    # obtener indices codigos
        indices_codigo = Utilidad.CapturarIndices(codigo_producto,codigo)
        
    # creamos un diccionario con los clientes que compraron un producto
        dicc_producto = Utilidad.ProductoClientes(codigo_producto,indices_codigo,cliente)
        clientes_que_compraron = dicc_producto[codigo_producto]
        i = codigo.index(codigo_producto)
        
        return render_template('consulta.html',nombre='Consulta', productos_por_cliente = productos_comprados,
         nombre_completo = nombre_completo,clientes_por_producto=clientes_que_compraron ,codigo_producto = codigo_producto,
         nombre_producto = producto[i])

    return redirect(url_for('ingresar'))



@app.route('/registrar')
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

#app.route("/prueba")
#def prueba():



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
