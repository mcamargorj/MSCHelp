from flask import Flask, render_template, request, redirect, url_for, session, escape
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

# Conectar ao banco de dados MySQL/MariaDB com senha criptografada e variável ambiente
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ.get('MYSQL_PASSWORD'),
    database="MSCHELP"
)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = escape(request.form['email'])
        password = escape(request.form['password'])
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            stored_password_hash = user[3]  # A quarta coluna (índice 3) contém o hash da senha
            if check_password_hash(stored_password_hash, password):
                session['user'] = user[0]
                return redirect(url_for('dashboard', nome=user[1]))
            else:
                return render_template('login.html', mensagem='Usuário ou senha incorretos.')
    
    return render_template('login.html')

@app.route('/dashboard/<nome>')
def dashboard(nome):
    if 'user' in session:
        # Aqui você pode usar a variável 'nome' que foi passada
        return render_template('dashboard.html', nome=nome)
    else:
        return redirect(url_for('login'))

# Página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = escape(request.form['nome'])
        email = escape(request.form['email'])
        password = escape(request.form['password'])
        password_hash = generate_password_hash(password)
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, password) VALUES (%s, %s, %s)", (nome, email, password_hash))
        conexao.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
