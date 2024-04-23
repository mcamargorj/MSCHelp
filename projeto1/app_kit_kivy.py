from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import mysql.connector
import os

class MyBoxLayout(BoxLayout):
    def criar_usuario(self, instance):
        # Obter dados dos campos de entrada
        nome = self.nome_input.text
        email = self.email_input.text
        senha = self.senha_input.text

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
        layout = MyBoxLayout(orientation='vertical', padding=20, spacing=10)

        # Adicionar campos de entrada e botão à interface
        layout.nome_input = TextInput(hint_text='Nome', multiline=False, size_hint=(1, None), height=40)
        layout.email_input = TextInput(hint_text='Email', multiline=False, size_hint=(1, None), height=40)
        layout.senha_input = TextInput(hint_text='Senha', multiline=False, password=True, size_hint=(1, None), height=40)
        layout.add_widget(layout.nome_input)
        layout.add_widget(layout.email_input)
        layout.add_widget(layout.senha_input)
        
        botao_criar = Button(text='Criar Usuário', size_hint=(1, None), height=40)
        botao_criar.bind(on_press=layout.criar_usuario)
        layout.add_widget(botao_criar)

        return layout

if __name__ == '__main__':
    MyApp().run()
