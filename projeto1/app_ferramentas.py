import mysql.connector
from werkzeug.security import generate_password_hash44
import os

# Função para criar um novo usuário
def criar_usuario():
    # Conectar ao banco de dados MySQL/MariaDB - Utilizar o MySQL do seu servidor
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ.get('MYSQL_PASSWORD'),  # MYSQL_PASSWORD - variável ambiente criada para que a senha não fique exposta no código.
        database="MSCHELP"
    )

    # Criar um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Receber dados do novo usuário via input
    nome = input("Digite o nome do novo usuário: ")
    email = input("Digite o email do novo usuário: ")
    senha = input("Digite a senha do novo usuário: ")

    # Criptografar a senha usando Werkzeug
    password_hash = generate_password_hash(senha)

    # Dados do novo usuário
    novo_usuario = {
        "nome": nome,
        "email": email,
        "password": senha  # A senha em texto simples
    }

    # Inserir o novo usuário na tabela
    sql = "INSERT INTO usuarios (nome, email, password) VALUES (%s, %s, %s)"
    valores = (novo_usuario["nome"], novo_usuario["email"], password_hash)

    cursor.execute(sql, valores)

    # Confirmar a inserção
    conexao.commit()

    # Fechar cursor e conexão
    cursor.close()
    conexao.close()

    print("Novo usuário inserido com sucesso!")

# Função para remover um usuário existente
def remover_usuario():
    # Conectar ao banco de dados MySQL/MariaDB - Utilizar o MySQL do seu servidor
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ.get('MYSQL_PASSWORD'),
        database="MSCHELP"
    )

    # Criar um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Solicitar o email do usuário a ser removido
    email_usuario = input("Digite o email do usuário que deseja remover: ")

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

    print("Usuário removido com sucesso!")

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
        # Você pode adicionar mais campos aqui conforme necessário

    # Fechar cursor e conexão
    cursor.close()
    conexao.close()

# Função principal para exibir o menu de opções
def main():
    while True:
        print("\nSelecione uma opção:")
        print("1. Criar usuário")
        print("2. Remover usuário")
        print("3. Listar usuários")
        print("4. Sair")

        opcao = input("Opção: ")

        if opcao == "1":
            criar_usuario()
        elif opcao == "2":
            remover_usuario()
        elif opcao == "3":
            listar_usuarios()
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")

if __name__ == "__main__":
    main()
