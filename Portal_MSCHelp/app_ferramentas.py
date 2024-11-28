import mysql.connector
from werkzeug.security import generate_password_hash
import os
from datetime import datetime
from flask import request 



def email_existe(email,conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = %s", (email,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0


def criar_usuario():
    if request.method == 'POST':
        # Conectar ao banco de dados MySQL/MariaDB - Utilizar o MySQL do seu servidor
        conexao = mysql.connector.connect(
            host="sql10.freesqldatabase.com",
            user="sql10748285",
            password=os.environ.get('MYSQL_PASSWORD'),
            database="sql10748285"
        )

        # Criar um cursor para executar comandos SQL
        cursor = conexao.cursor()

        # Receber dados do novo usuário via formulário
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        # Criptografar a senha usando Werkzeug
        password_hash = generate_password_hash(senha)

        if email_existe(email,conexao):
            return False
        
        # Dados do novo usuário
        novo_usuario = {
            "nome": nome,
            "email": email,
            "password": password_hash,  # A senha em texto simples
            "role": 'user' # Definir nível de permissão padrão para todos os usuários
        }

        # Inserir o novo usuário na tabela
        sql = "INSERT INTO usuarios (nome, email, password, role) VALUES (%s, %s, %s, %s)"
        valores = (novo_usuario["nome"], novo_usuario["email"], novo_usuario["password"], novo_usuario["role"])

        cursor.execute(sql, valores)

        # Confirmar a inserção
        conexao.commit()

        # Fechar cursor e conexão
        cursor.close()
        conexao.close()
        
        return True
    
    else:
        
        return False

# Função para remover um usuário existente
def remover_usuario():
    if request.method == 'POST':
        # Conectar ao banco de dados MySQL/MariaDB
        conexao = mysql.connector.connect(
            host="sql10.freesqldatabase.com",
            user="sql10748285",
            password=os.environ.get('MYSQL_PASSWORD'),
            database="sql10748285"
        )

        # Receber o email do usuário a ser removido via formulário
        email_usuario = request.form['email']

        if not email_existe(email_usuario,conexao):
            return False

        # Criar um cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Comando SQL para deletar o usuário com o email especificado
        sql = "DELETE FROM usuarios WHERE email = %s"
        valor = (email_usuario,)

        # Executar o comando SQL
        cursor.execute(sql, valor)

        # Confirmar a remoção
        conexao.commit()

        # Fechar cursor e conexão
        cursor.close()
        conexao.close()
        return True
    
    else:
        return False




# Função para listar todos os usuários

def listar_usuarios():
    # Conectar ao banco de dados MySQL/MariaDB - Utilizar o MySQL do seu servidor
    conexao = mysql.connector.connect(
            host="sql10.freesqldatabase.com",
            user="sql10748285",
            password=os.environ.get('MYSQL_PASSWORD'),
            database="sql10748285"
        )

    # Criar um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Consulta SQL para selecionar todos os dados da tabela usuarios
    sql = "SELECT * FROM usuarios"

    # Executar a consulta
    cursor.execute(sql)

    # Recuperar todos os resultados da consulta
    usuarios = cursor.fetchall()

    # Mostrar os dados dos usuários
    #print("Dados dos usuários:")
    #or usuario in usuarios:
        #print("Nome:", usuario[1])
        #print("Email:", usuario[2])
        #print("Permissão:", usuario[4])
        # Você pode adicionar mais campos aqui conforme necessário

    # Exibir resumo
    #total_usuarios = len(usuarios)
    #data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #print(f"Resumo: {total_usuarios} usuários cadastrados até a data de hoje {data_atual}")

    # Fechar cursor e conexão
    cursor.close()
    conexao.close()

    # Retornar os usuários
    return usuarios

def editar_usuarios(id, nome, email, password, role):
    conexao = mysql.connector.connect(
            host="sql10.freesqldatabase.com",
            user="sql10748285",
            password=os.environ.get('MYSQL_PASSWORD'),
            database="sql10748285"
        )
    cursor = conexao.cursor()

    # Buscar o hash atual da senha para comparação
    cursor.execute("SELECT password FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()

    if not usuario:
        return False, "Usuário não encontrado."
    
    senha_atual = usuario[0]

    # Se uma nova senha foi fornecida, gerar um hash
    if password and password != senha_atual:
        password = generate_password_hash(password)
    else:
        password = senha_atual  # Mantém o hash atual

    # Atualizar os dados do usuário
    campos = []
    valores = []

    if nome:
        campos.append("nome = %s")
        valores.append(nome)
    if email:
        campos.append("email = %s")
        valores.append(email)
    if password != senha_atual:  # Atualiza apenas se a senha mudou
        campos.append("password = %s")
        valores.append(password)
    if role:
        campos.append("role = %s")
        valores.append(role)

    # Adiciona o ID no final para a condição WHERE
    valores.append(id)

    # Monta a consulta dinamicamente
    sql = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = %s"

    try:
        cursor.execute(sql, valores)
        conexao.commit()
        return True, None
    except mysql.connector.Error as e:
        conexao.rollback()
        return False, str(e)



def buscar_usuario_por_id(id):
    conexao = mysql.connector.connect(
            host="sql10.freesqldatabase.com",
            user="sql10748285",
            password=os.environ.get('MYSQL_PASSWORD'),
            database="sql10748285"
        )
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()
    return usuario

