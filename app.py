from flask import Flask, render_template,request
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
            elif usuario_valido['account'].iloc[0] == "Transportador":
                return render_template('proveedor_index.html',producto = leerPedidos().to_dict(orient='records'))
            elif usuario_valido['account'].iloc[0] == "Proveedor":
                return render_template('proveedor_index.html',producto = leerPedidos().to_dict(orient='records'))
        else:
            return render_template('index.html')

    return render_template('registro.html')

@app.route('/indexCliente')
def indexCliente():  # put application's code here
    return render_template('cliente_index.html', producto = leerProductoCliente())

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

        return render_template('pedidosCliente.html')

    return render_template('pedirProducto.html', producto = leerProductoProveedor().to_dict(orient='records'))

@app.route('/pedidosCliente')
def pedidosCliente():
    return render_template('pedidosCliente.html', producto = leerPedidos().to_dict(orient='records'))

if __name__ == '__main__':
    app.run()
