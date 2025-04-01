# Importando as bibliotecas necessárias: Flask para a aplicação web e werkzeug para segurança de senhas
from flask import Flask, render_template, request 
from werkzeug.security import generate_password_hash, check_password_hash
import database  # Importando o arquivo onde o banco de dados é manipulado

# Criando a aplicação Flask
app = Flask(__name__) 

# Rota principal ('/') que renderiza o template 'index.html'
@app.route('/')
def hello():
    return render_template('index.html')

# Rota de login ('/login') que pode ser acessada por métodos GET ou POST
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form  # Coletando os dados do formulário de login
        # Chamando a função 'login' do arquivo database para verificar a senha
        if database.login(form) == True:
            return render_template('lista.html')  # Se login for bem-sucedido, redireciona para 'lista.html'
        else:
            return "Ocorreu um erro ao fazer o login do usuário"  # Caso contrário, exibe mensagem de erro
    else:
        return render_template('login.html')  # Se for GET, renderiza o formulário de login

# Rota de cadastro ('/cadastro') que também pode ser acessada por GET ou POST
@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        form = request.form  # Coletando os dados do formulário de cadastro
        # Chamando a função 'criar_usuario' do arquivo database para cadastrar o usuário
        if database.criar_usuario(form) == True:
            return render_template('login.html')  # Se cadastro for bem-sucedido, redireciona para o login
        else:
            return "Ocorreu um erro ao cadastrar usuário"  # Caso contrário, exibe mensagem de erro
    else:
        return render_template('cadastro.html')  # Se for GET, renderiza o formulário de cadastro

# Executa a aplicação Flask no modo de debug
if __name__ == '__main__':
    app.run(debug=True)
