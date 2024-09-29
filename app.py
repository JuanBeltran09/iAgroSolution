from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import Filtro_Df as fil

app = Flask(__name__)
user = ''
def guardarNombre(nombre):
    global user
    user = nombre

def leerUsuarios():
    df = pd.read_csv('users.csv')
    df['password'] = df['password'].astype(str)
    return df

def leerProductoProveedor():
    productos = pd.read_csv('productoProveedor.csv')
    return productos

def leerPedidos():
    pedidos = pd.read_csv('pedidos.csv')
    return pedidos

def leerEnvios():
    Envios = pd.read_csv('Envios.csv')
    return Envios

def leerTransporte():
    Transporte = pd.read_csv('transportes.csv')
    return Transporte

def leerProductoCliente():
    productos = pd.read_csv('productoCliente.csv')
    productos_list = productos.to_dict(orient='records')
    return productos_list

def guardarUsuario(username, password, account):
    df_new = pd.DataFrame([{'username':username,'password':password,'account':account}])
    df = leerUsuarios()
    df = pd.concat([df,df_new], ignore_index=True)
    df.to_csv('users.csv',index=False)

def guardarPedido(producto,nombreCliente,nombreProveedor,cantidad,fechaPedida,fechaEntrega,estado):
    df_new = pd.DataFrame([{
        "producto":producto,
        "nombreCliente":nombreCliente,
        "nombreProveedor":nombreProveedor,
        "cantidad":cantidad,
        "fechaPedida":fechaPedida,
        "fechaEntrega":fechaEntrega,
        "estado":estado
    }])
    df = leerPedidos()
    df = pd.concat([df,df_new], ignore_index=True)
    df.to_csv('pedidos.csv',index=False)

def guardarEnvio(producto,nombreCliente,nombreProveedor):
    df_new = pd.DataFrame([{
        "producto":producto,
        "nombreCliente":nombreCliente,
        "nombreProveedor":nombreProveedor
    }])
    df = leerEnvios()
    df = pd.concat([df,df_new], ignore_index=True)
    df.to_csv('Envios.csv',index=False)

def guardarProducto(producto,precio,nombreProveedor):
    df_new = pd.DataFrame([{
        "producto":producto,
        "precio":precio,
        "nombreProveedor":nombreProveedor
    }])
    df = leerProductoProveedor()
    df = pd.concat([df,df_new], ignore_index=True)
    df.to_csv('productoProveedor.csv',index=False)

def actualizarEstado(indice, estado):
    df = leerPedidos()
    df.loc[indice, "estado"] = estado
    df.to_csv('pedidos.csv',index=False)
@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/acercaNosotros')
def acercaNosotros():  # put application's code here
    return render_template('acercaNosotros.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():  # put application's code here
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        account = request.form.get('type')
        guardarUsuario(username, password, account)
        return render_template('index.html')
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        df = leerUsuarios()

        usuario_valido = df[(df['username'] == username) & (df['password'] == password)]

        if not usuario_valido.empty:

            guardarNombre(usuario_valido['username'].iloc[0])

            if usuario_valido['account'].iloc[0] == "Cliente":
                return render_template('cliente_index.html', producto = leerProductoCliente())
            elif usuario_valido['account'].iloc[0] == "Proveedor":
                return redirect(url_for('indexProveedor'))
        else:
            return render_template('index.html')

    return render_template('registro.html')

@app.route('/indexCliente')
def indexCliente():  # put application's code here
    return render_template('cliente_index.html', producto = leerProductoCliente())

@app.route('/indexProveedor')
def indexProveedor():
    return render_template('proveedor_index.html', producto = leerPedidos().loc[leerPedidos()['estado'] == 'No Enviado'].to_dict(orient='records'))

@app.route('/pedirProducto', methods=['GET', 'POST'])
def pedirProducto():
    if request.method == 'POST':
        producto = request.form['producto']
        precio = request.form['precio']
        nombreProveedor = request.form['nombreProveedor']
        nombreCliente = user
        fechaPedido = datetime.now()
        fechaEntrega = fechaPedido + relativedelta(months=1)
        return render_template('confirmarPedido.html', producto=producto, precio=precio,
                               nombreProveedor=nombreProveedor, nombreCliente=nombreCliente,
                               fechaEntrega=fechaEntrega.strftime('%d-%m-%Y'))

    return render_template('pedirProducto.html', producto = leerProductoProveedor().to_dict(orient='records'))

@app.route('/confirmarProducto', methods=['GET', 'POST'])
def confirmarProducto():
    if request.method == 'POST':
        producto = request.form['producto']
        nombreProveedor = request.form['nombreProveedor']
        nombreCliente = user
        cantidad = request.form['cantidad']
        fechaPedida = datetime.now().strftime('%d-%m-%Y')
        fechaEntrega = request.form['fechaEntrega']
        estado = "No Enviado"

        guardarPedido(producto, nombreCliente, nombreProveedor, cantidad, fechaPedida, fechaEntrega, estado)

        return redirect(url_for('indexCliente'))

    return render_template('pedirProducto.html', producto = leerProductoProveedor().to_dict(orient='records'))

@app.route('/pedidosCliente')
def pedidosCliente():
    return render_template('pedidosCliente.html', producto = leerPedidos().to_dict(orient='records'))

@app.route('/enviarPedido', methods=['GET', 'POST'])
def enviarPedido():
    if request.method == 'POST':
        indice = int(request.form['indice'])
        pedido_seleccionado = leerPedidos().iloc[indice]
        return render_template('enviarPedido.html', producto = leerTransporte().to_dict(orient='records'), indice = indice, user = pedido_seleccionado["nombreCliente"])

@app.route('/enviarTransportador', methods=['GET', 'POST'])
def enviarTransportador():
    if request.method == 'POST':
        indice = int(request.form['indice'])
        pedido_seleccionado = leerPedidos().iloc[indice]
        nombre =request.form['nombre']
        guardarEnvio(nombre, pedido_seleccionado["nombreCliente"], pedido_seleccionado["nombreProveedor"])
        actualizarEstado(indice,"Enviado")
        return redirect(url_for('indexProveedor'))

@app.route('/agregarProducto', methods=['GET', 'POST'])
def agregarProducto():
    if request.method == 'POST':
        producto = request.form['producto']
        precio = request.form['precio']
        nombreProveedor = user
        guardarProducto(producto, precio, nombreProveedor)
        return redirect(url_for('indexProveedor'))
    return render_template('agregarProducto.html')

@app.route('/analisisData', methods=['GET', 'POST'])
def analisisData():
    df = fil.filtro()
    municipios = df['municipio'].drop_duplicates().tolist()

    if request.method == 'POST':
        municipio = request.form.get('municipio')
        product_info = fil.graficar(df, municipio)
        show = 1
        return render_template("Data.html",
                               municipios=municipios,
                               show=show,
                               municipio=municipio,
                               product_info=product_info)

    return render_template('Data.html', municipios=municipios)

if __name__ == '__main__':
    app.run()
