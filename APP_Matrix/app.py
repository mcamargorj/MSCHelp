
# App de login, códigos Python com Flask para Web APP, roda em qualquer plataforma, Windows, Linux, Android e IOS
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Simples autenticação direto no APP, sem banco de dados. Não aconselhável para produção.
login_data = {
    'marcelo': 'davi'
    
}
# Aqui está a primeira rota que chama o template login.html e recebe os dados do form.
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

       #Aqui é a condição
        if usuario in login_data and login_data[usuario] == senha:
            
            return redirect(url_for('bem_vindo', usuario=usuario))
        else:
           
            return render_template('login.html', mensagem='Usuário ou senha incorretos.')


    return render_template('login.html', mensagem='')
#Aqui é a rota da página bem-vindo após o login ter sido realizado com sucesso
@app.route('/bem_vindo/<usuario>')
def bem_vindo(usuario):
    #Chama o template bem_vindo.html
    return render_template('bem_vindo.html', usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)
# Para que os templates sejam chamados corretamente, estes deverão estar dentro do diretório templates, conforme consta no projeto