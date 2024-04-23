import mysql.connector
import os

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
