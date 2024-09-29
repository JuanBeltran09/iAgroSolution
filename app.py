from flask import Flask, render_template,request
import pandas as pd
app = Flask(__name__)

df_users = pd.read_csv('users.csv')

def guardarUsuario(username, password, account, df):
    df_new = pd.DataFrame([{'username':username,'password':password,'account':account}])
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

        print(username, password, account, df_users)
        guardarUsuario(username, password, account, df_users)
        return render_template('index.html')
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        account = request.form.get('type')

        print(username, password, account, df_users)
        guardarUsuario(username, password, account, df_users)
        return render_template('index.html')
    return render_template('registro.html')


if __name__ == '__main__':
    app.run()
