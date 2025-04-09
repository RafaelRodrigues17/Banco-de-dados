# Importando as bibliotecas necessárias: Flask para a aplicação web e werkzeug para segurança de senhas
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import database  # Importando o arquivo onde o banco de dados é manipulado

# Criando a aplicação Flask
app = Flask(__name__) 
app.secret_key ="SENHA SECRETA" #senha secreta que geralmente

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
            session['usuario'] = form['email'] # Armazena o email do usuário na sessão
            return redirect(url_for('lista'))
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
    
@app.route('/lista') 
def lista():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    lista_tarefas = database.buscar_tarefas(session['usuario'])
    print(lista_tarefas)
    
    return render_template('lista.html', tarefas=lista_tarefas)

@app.route('/criar_tarefa', methods=["POST"])
def criar_tarefa():
    form = request.form
    if database.criar_tarefa(form['conteudo'], session['usuario']) == True:
        return redirect(url_for('lista'))
    else:
        return "Ocorreu um erro ao registar tarefa"

@app.route('/tarefas/atualizar/<int:id>', methods=['GET'])
def tarefa_concluida(id):
    if database.tarefa_concluida(id):
        return redirect(url_for('lista'))
    else:
        return "Ocorreu um erro ao marcar a tarefa como concluída"

@app.route('/tarefas/excluir/<int:id>', methods=['GET'])
def excluir_tarefa(id):
    if database.excluir_tarefa(id):
        return redirect(url_for('lista'))
    else:
        return "Ocorreu um erro ao excluir a tarefa"

@app.route('/tarefas/editar/<int:id>', methods=["GET", "POST"])
def editar_tarefa(id):

    email = session['usuario'] # Pega o e-mail da sessão e verifica se é o dono da tarefa
    if(request.method == "GET"):
        conteudo_tarefa  = database.buscar_conteudo_tarefa(id)
        return render_template('editar.html', tarefa = conteudo_tarefa, id=id)
    
    if(request.method == "POST"):
        form = request.form
        novo_conteudo = form['conteudo']
        database.editar_tarefa(novo_conteudo, id)
        return redirect(url_for('lista'))

@app.route('/excluir_usuario')
def excluir_usuario():
    email = session['usuario']
    
    if database.excluir_usuario(email):
        return redirect(url_for('hello'))
    else:
        return "Ocorreu um erro ao excluir o usuário"
    
# Executa a aplicação Flask no modo de debug
if __name__ == '__main__':
    app.run(debug=True)
