from flask import Flask, render_template, request, redirect, url_for, session, Markup
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
import secrets
import hashlib

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configuração do banco de dados MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'seu_usuario'
app.config['MYSQL_PASSWORD'] = 'sua_senha'
app.config['MYSQL_DB'] = 'sua_base_de_dados'
mysql = MySQL(app)

# Configuração do banco de dados PostgreSQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://seu_usuario:sua_senha@localhost/sua_base_de_dados'
# db = SQLAlchemy(app)

# Função para gerar token CSRF
def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(16)
    return session['_csrf_token']

# Função para criptografar senhas
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = escape(request.form['email'])  # Escapar dados do usuário para prevenir XSS
        password = request.form['password']
        password_hash = hash_password(password)  # Criptografar senha
        csrf_token = session.pop('_csrf_token', None)
        if not csrf_token or csrf_token != request.form.get('_csrf_token'):
            return "Erro de CSRF"  # Rejeitar solicitação CSRF inválida
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password_hash))
        user = cur.fetchone()
        cur.close()
        if user:
            session['user'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            return "Login inválido"
    return render_template('login.html', csrf_token=generate_csrf_token())

# Página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = escape(request.form['email'])  # Escapar dados do usuário para prevenir XSS
        password = request.form['password']
        password_hash = hash_password(password)  # Criptografar senha
        csrf_token = session.pop('_csrf_token', None)
        if not csrf_token or csrf_token != request.form.get('_csrf_token'):
            return "Erro de CSRF"  # Rejeitar solicitação CSRF inválida
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password_hash))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('register.html', csrf_token=generate_csrf_token())

# Página inicial após login
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return "Página inicial após login"
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
