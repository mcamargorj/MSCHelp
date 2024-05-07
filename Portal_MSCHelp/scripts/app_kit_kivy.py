from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import mysql.connector
import os

class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [20, 20]

        self.nome_input = TextInput(hint_text='Nome', size_hint=(1, None), height=40)
        self.email_input = TextInput(hint_text='Email', size_hint=(1, None), height=40)
        self.senha_input = TextInput(hint_text='Senha', password=True, size_hint=(1, None), height=40)

        self.botao_criar = Button(text='Criar Usuário', size_hint=(1, None), height=40)
        self.botao_criar.bind(on_press=self.criar_usuario)

        self.mensagem_label = Label(size_hint=(1, None), height=40)

        self.add_widget(self.nome_input)
        self.add_widget(self.email_input)
        self.add_widget(self.senha_input)
        self.add_widget(self.botao_criar)
        self.add_widget(self.mensagem_label)

    def criar_usuario(self, instance):
        nome = self.nome_input.text
        email = self.email_input.text
        senha = self.senha_input.text

        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.environ.get('MYSQL_PASSWORD'),
            database="MSCHELP"
        )

        cursor = conexao.cursor()
        sql = "INSERT INTO usuarios (nome, email, password) VALUES (%s, %s, %s)"
        valores = (nome, email, senha)

        cursor.execute(sql, valores)
        conexao.commit()
        cursor.close()
        conexao.close()

        self.mensagem_label.text = "Usuário criado com sucesso!"

class MyApp(App):
    def build(self):
        return MyBoxLayout()

if __name__ == '__main__':
    MyApp().run()
