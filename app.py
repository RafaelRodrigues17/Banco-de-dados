from flask import Flask, render_template, request # Importando a biblioteca Flask
#biblioteca de segurança no login
from werkzeug.security import generate_password_hash, check_password_hash
import database

app = Flask(__name__) # Criando um objeto do Flask

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        if database.login(form) == True:
            return render_template('lista.html')
        else:
            return "Ocorreu um erro ao fazer o login do usuário"     
    else:    
       return render_template('login.html')

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        form = request.form
        if database.criar_usuario(form) == True:
            return render_template('login.html')
        else:
            return "Ocorreu um erro ao cadastrar usuário"     
    else:    
       return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)