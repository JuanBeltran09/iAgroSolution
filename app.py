from flask import Flask, render_template,request
import pandas as pd
app = Flask(__name__)

def leerUsuarios():
    df = pd.read_csv('users.csv')
    df['password'] = df['password'].astype(str)
    return df

def leerProductoCliente():
    productos = pd.read_csv('productoCliente.csv')
    productos_list = productos.to_dict(orient='records')
    return productos_list

def guardarUsuario(username, password, account):
    df_new = pd.DataFrame([{'username':username,'password':password,'account':account}])
    df = leerUsuarios()
    df = pd.concat([df,df_new], ignore_index=True)
    df.to_csv('users.csv',index=False)

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
            if usuario_valido['account'].iloc[0] == "Cliente":
                return render_template('cliente_index.html', producto = leerProductoCliente())
            elif usuario_valido['account'].iloc[0] == "Transportador":
                return render_template('registro.html')
            elif usuario_valido['account'].iloc[0] == "Proveedor":
                return render_template('registro.html')
        else:
            return render_template('index.html')

    return render_template('registro.html')

@app.route('/indexCliente')
def indexCliente():  # put application's code here
    return render_template('cliente_index.html', producto = leerProductoCliente())

if __name__ == '__main__':
    app.run()
