from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import mysql.connector
import os

class MyBoxLayout(BoxLayout):
    def criar_usuario(self):
        # Obter dados dos campos de entrada
        nome = self.ids.nome_input.text
        email = self.ids.email_input.text
        senha = self.ids.senha_input.text

        # Conectar ao banco de dados MySQL/MariaDB
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.environ.get('MYSQL_PASSWORD'),
            database="MSCHELP"
        )

        # Criar um cursor para executar comandos SQL
        cursor = conexao.cursor()

        # Exemplo de consulta SQL
        sql = "INSERT INTO usuarios (nome, email, password) VALUES (%s, %s, %s)"
        valores = (nome, email, senha)

        # Executar a consulta
        cursor.execute(sql, valores)

        # Confirmar a inserção
        conexao.commit()

        # Fechar cursor e conexão
        cursor.close()
        conexao.close()

        print("Novo usuário inserido com sucesso!")

class MyApp(App):
    def build(self):
        layout = MyBoxLayout()

        # Adicionar campos de entrada e botão à interface
        layout.add_widget(TextInput(id='nome_input', hint_text='Nome'))
        layout.add_widget(TextInput(id='email_input', hint_text='Email'))
        layout.add_widget(TextInput(id='senha_input', hint_text='Senha', password=True))
        layout.add_widget(Button(text='Criar Usuário', on_press=layout.criar_usuario))

        return layout

if __name__ == '__main__':
    MyApp().run()
