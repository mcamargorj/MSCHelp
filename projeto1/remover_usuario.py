import mysql.connector # Módulo para conexão com banco de dados
import os # Faz com que a função "os.environ.get" seja reconhecida no código

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
