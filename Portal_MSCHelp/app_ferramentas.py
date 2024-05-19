import mysql.connector
from werkzeug.security import generate_password_hash
import os
from datetime import datetime
from flask import request 
import re

def validar_email(email):
    """Função para validar o formato do email."""
    # Padrão de expressão regular para validar email
    padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao_email, email)



def criar_usuario():
    if request.method == 'POST':
        # Conectar ao banco de dados MySQL/MariaDB - Utilizar o MySQL do seu servidor
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.environ.get('MYSQL_PASSWORD'),  # MYSQL_PASSWORD - variável ambiente criada para que a senha não fique exposta no código.
            database="MSCHELP"
        )

        # Criar um cursor para executar comandos SQL
        cursor = conexao.cursor()

        # Receber dados do novo usuário via formulário
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Validar o formato do email
        if not validar_email(email):
            print("Email inválido.")
            return False

        # Criptografar a senha usando Werkzeug
        password_hash = generate_password_hash(senha)

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

        #print("Novo usuário inserido com sucesso!")  # Mensagem para indicar sucesso
        return True
    else:
        
        return False

# Função para remover um usuário existente
def remover_usuario():
    if request.method == 'POST':
        # Conectar ao banco de dados MySQL/MariaDB
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.environ.get('MYSQL_PASSWORD'),
            database="MSCHELP"
        )

        # Receber o email do usuário a ser removido via formulário
        email_usuario = request.form['email']

        # Validar o formato do email
        if not validar_email(email_usuario):
            print("Email inválido.")
            return False
        # Verifica se o e-mail existe na base de dados
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email_usuario,))
        user = cursor.fetchone()
        cursor.close()

        if user:
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
        
    else:
        return False   



# Função para listar todos os usuários

def listar_usuarios():
    # Conectar ao banco de dados MySQL/MariaDB - Utilizar o MySQL do seu servidor
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ.get('MYSQL_PASSWORD'),  # MYSQL_PASSWORD - variável ambiente criada para que a senha não fique exposta no código.
        database="MSCHELP"
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
    print("Dados dos usuários:")
    for usuario in usuarios:
        print("Nome:", usuario[1])
        print("Email:", usuario[2])
        print("Permissão:", usuario[4])
        # Você pode adicionar mais campos aqui conforme necessário

    # Exibir resumo
    total_usuarios = len(usuarios)
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"Resumo: {total_usuarios} usuários cadastrados até a data de hoje {data_atual}")

    # Fechar cursor e conexão
    cursor.close()
    conexao.close()

    # Retornar os usuários
    return usuarios



if __name__ == "__main__":
    main()
