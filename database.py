import sqlite3

def conectar_banco():
    conexao = sqlite3.connect("tarefas.db")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''create table if not exists usuarios
                   (email text primary key,nome text,senha text)''')
    
    cursor.execute('''create table if not exists tarefas
                   (id integer primary key, conteudo text, esta_concluida integer, email text,
                   FOREIGN KEY(email_usuario) REFERENCES usuarios(email))''')
    
    conexao.commit()
    
def criar_usuario(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT COUNT (email) FROM usuarios WHERE email=?''', (formulario['email'],))
    conexao.commit()
    
    quantidade_de_emails = cursor.fetchone()
    print(quantidade_de_emails)
    if (quantidade_de_emails [0]> 0):
        print("E-mail já cadastrado! escolha outro")
        return False

    cursor.execute('''insert into usuarios(email, nome, senha) 
                   VALUES (?, ?, ?)''', (formulario['email'], formulario['nome'], formulario['senha']
                       ))
    conexao.commit()
    return True
    
if __name__ == "__main__":
    criar_tabelas()
