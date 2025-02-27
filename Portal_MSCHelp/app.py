from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
import os


# Importar as funções do kit ferramentas para utilizar no painel_admin
from app_ferramentas import criar_usuario, remover_usuario, listar_usuarios, email_existe, editar_usuarios,buscar_usuario_por_id

app = Flask(__name__)
app.secret_key = os.urandom(16)

# Conectar ao banco de dados MySQL/MariaDB com senha criptografada e variável ambiente
conexao = mysql.connector.connect(
    host="sql10.freesqldatabase.com",
    user="sql10748285",
    password=os.environ.get('MYSQL_PASSWORD'),
    database="sql10748285"
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
                session['nome'] = user[1]
                session['role'] = user[4]
                return redirect(url_for('dashboard', nome=session['nome']))
            else:
                return render_template('login.html', mensagem='Usuário ou senha incorretos.')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        # Aqui você pode usar a variável 'nome' que foi passada
        nome = session.get('nome')

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
        

        if email_existe(email,conexao):
            return render_template('register.html', sucesso=False, erro="Este email já está cadastrado!")
        
        
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, password, role) VALUES (%s, %s, %s, %s)", (nome, email, password_hash, 'user'))
        conexao.commit()
        cursor.close()
        
        return render_template('register.html', sucesso=True)
        
    else:
        return render_template('register.html')
    
    ####



# Rota para exibir o painel admin
@app.route('/painel_admin')
def painel_admin():
    if 'user' in session and session.get('role') == 'admin':
        # O usuário é um administrador, então permitir acesso ao painel admin
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios")  # Ajuste na consulta para selecionar apenas o nome
        usuarios = cursor.fetchall() 
        cursor.close()
        return render_template('painel_admin.html', usuarios=usuarios)
    else:
        # O usuário não está autenticado como administrador, redirecionar para a página de login
        return redirect(url_for('login'))
    
# Rota para exibir o template de criar usuário
@app.route('/criar_usuario', methods=['GET', 'POST'])
def criar_usuario_form():
    if 'user' in session and session.get('role') == 'admin':
        if request.method == 'GET':
            return render_template('criar_usuario.html')
        elif request.method == 'POST':
            if criar_usuario():
                return render_template('painel_admin.html', sucesso=True)
            else:
                return render_template('painel_admin.html', sucesso=False, erro="E-mail já cadastrado!")
    else:
        return redirect(url_for('login'))

# Rota para exibir o template de remover usuário
@app.route('/remover_usuario', methods=['GET', 'POST'])
def remover_usuario_form():
    if 'user' in session and session.get('role') == 'admin':
        if request.method == 'GET':
            return render_template('remover_usuario.html')
        elif request.method == 'POST':
            if remover_usuario():
                return render_template('painel_admin.html', delete=True)
            else:
                return render_template('painel_admin.html', delete=False, erro="E-mail não cadastrado!")        
    else:
        return redirect(url_for('login'))
    
    # Rota para exibir o template de listar usuários
@app.route('/listar_usuarios', methods=['GET', 'POST'])
def listar_usuarios_painel_admin():
    if 'user' in session and session.get('role') == 'admin':
        if request.method == 'GET':
            usuarios = listar_usuarios()  # Obter os usuários
            return render_template('listar_usuarios.html', usuarios=usuarios)  # Passar os usuários para o template
        elif request.method == 'POST':
            listar_usuarios()  # Chamar a função listar_usuarios quando um POST for feito
            return redirect(url_for('painel_admin'))
    else:
        return redirect(url_for('login'))

@app.route('/editar_usuarios/<int:id>', methods=['GET', 'POST'])
def editar_usuarios_painel_admin(id):
    if 'user' in session and session.get('role') == 'admin':
        if request.method == 'GET':
            usuario = buscar_usuario_por_id(id)  # Buscar dados do usuário específico
            if usuario:
                return render_template('editar_usuarios.html', usuario=usuario)
            else:
                return redirect(url_for('painel_admin')) # Redirecionar se o usuário não for encontrado

        elif request.method == 'POST':
            nome = request.form['nome']
            email = request.form['email']
            password = request.form['password']
            role = request.form['role']

            atualizado = editar_usuarios(id, nome, email, password, role)

            if atualizado:
                return render_template('painel_admin.html', atualizado=True)
            else:
                return render_template('editar_usuarios.html', usuario=request.form, atualizado=False, erro="Erro ao atualizar usuário!")
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)



