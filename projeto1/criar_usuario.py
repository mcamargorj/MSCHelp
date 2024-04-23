import mysql.connector
from werkzeug.security import generate_password_hash
import os

# Conectar ao banco de dados MySQL/MariaDB - Utilizar o MySQL do seu servidor
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password= os.environ.get('MYSQL_PASSWORD'), #MYSQL_PASSWORD - variável ambiente criada para que a senha não fique exposta no código.
    database="MSCHELP"
)

# Criar um cursor para executar comandos SQL
cursor = conexao.cursor()

# Dados do novo usuário
novo_usuario = {
    "nome": "Marcelo",
    "email": "mcamargoce@outlook.com",
    "password": "davi1211"  # A senha em texto simples
}

# Criptografar a senha usando Werkzeug
password_hash = generate_password_hash(novo_usuario["password"])


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
