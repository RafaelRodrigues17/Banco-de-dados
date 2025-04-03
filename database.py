import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Função para conectar ao banco de dados SQLite
def conectar_banco():
    conexao = sqlite3.connect("tarefas.db")
    return conexao

# Função para criar as tabelas do banco de dados, caso não existam
def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Criando a tabela de usuários
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                   (email TEXT PRIMARY KEY, nome TEXT, senha TEXT)''')
    
    # Criando a tabela de tarefas
    cursor.execute('''CREATE TABLE IF NOT EXISTS tarefas
                   (id INTEGER PRIMARY KEY, conteudo TEXT, esta_concluida INTEGER, email TEXT,
                   FOREIGN KEY(email) REFERENCES usuarios(email))''')
    
    conexao.commit()

# Função para criar um novo usuário no banco de dados
def criar_usuario(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Verificando se o e-mail já está cadastrado
    cursor.execute('''SELECT COUNT(email) FROM usuarios WHERE email=?''', (formulario['email'],))
    conexao.commit()
    
    quantidade_de_emails = cursor.fetchone()
    print(quantidade_de_emails)
    
    # Se o e-mail já existir, retorna False
    if quantidade_de_emails[0] > 0:
        print("E-mail já cadastrado! Tente novamente")
        return False
    
    # Criptografando a senha do usuário
    senha_criptografada = generate_password_hash(formulario['senha'])
    
    # Inserindo os dados do novo usuário no banco
    cursor.execute('''INSERT INTO usuarios(email, nome, senha) 
                   VALUES (?, ?, ?)''', (formulario['email'], formulario['nome'], senha_criptografada))
    
    conexao.commit()
    return True

# Função para realizar login de um usuário
def login(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Verificando se o e-mail existe no banco de dados
    cursor.execute('''SELECT COUNT(email) FROM usuarios WHERE email=?''', (formulario['email'],))
    conexao.commit()
    
    quantidade_de_emails = cursor.fetchone()
    print(quantidade_de_emails)
    
    # Se o e-mail não estiver cadastrado, retorna False
    if quantidade_de_emails[0] == 0:
        print("E-mail não cadastrado! Tente novamente")
        return False
    
    # Obtendo a senha criptografada do usuário no banco
    cursor.execute('''SELECT senha FROM usuarios WHERE email=?''', (formulario['email'],))
    conexao.commit()
    senha_criptografada = cursor.fetchone()
    
    # Verificando se a senha fornecida corresponde à senha armazenada
    return check_password_hash(senha_criptografada[0], formulario['senha'])

def criar_tarefa(conteudo, email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO tarefas (conteudo, esta_concluida, email)
                   VALUES (?, ?, ?) ''',
                   (conteudo, False, email))
    conexao.commit()
    return True

def buscar_tarefas(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(''' SELECT id, conteudo, esta_concluida
                   FROM tarefas WHERE email=?''',
                   (email,))
    conexao.commit()
    tarefas = cursor.fetchall()
    return tarefas

if __name__ == "__main__":
    criar_tabelas()
