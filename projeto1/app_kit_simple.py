from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import mysql.connector
import os

class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)

        # Configurar estilo de fundo
        with self.canvas.before:
            self.background_color = get_color_from_hex("#f0f0f0")  # Cor de fundo

        # Adicionar campos de entrada e botão à interface
        self.orientation = 'vertical'
        self.padding = [50, 20]
        self.spacing = 20

        self.nome_input = TextInput(hint_text='Nome', multiline=False)
        self.email_input = TextInput(hint_text='Email', multiline=False)
        self.senha_input = TextInput(hint_text='Senha', multiline=False, password=True)

        self.botao_criar = Button(text='Criar Usuário')
        self.botao_criar.bind(on_press=self.criar_usuario)

        self.add_widget(self.nome_input)
        self.add_widget(self.email_input)
        self.add_widget(self.senha_input)
        self.add_widget(self.botao_criar)

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
        return MyBoxLayout()

if __name__ == '__main__':
    MyApp().run()
