# Código para sortear qualquer coisa, basta substituir as imagens e respeitar os nomes time1.png, time2.png,...,time6.png
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from random import randint

class VencedorApp(App):
    def build(self):
        layout = FloatLayout()

        self.resultado_sorteio = Image(source='', size_hint=(None, None), size=(300, 300), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.resultado_sorteio.keep_ratio = True
        self.resultado_sorteio.allow_stretch = True
        layout.add_widget(self.resultado_sorteio)

        botao = Button(text="Sortear", size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'y': 0.05})
        botao.bind(on_press=self.animar_imagem)  # Vincula a animação ao evento de pressionar o botão
        layout.add_widget(botao)

        return layout

    def animar_imagem(self, instance):
        # Gera um número aleatório entre 1 e 6 (índices das imagens)
        vencedor = randint(1, 6)
        # Define a imagem correspondente ao resultado do dado
        nova_imagem = 'assets/'+f'time{vencedor}.png'
        self.resultado_sorteio.source = nova_imagem

        # Cancela qualquer animação anterior
        Animation.cancel_all(self.resultado_sorteio)

        # Define e inicia a animação de aumento de tamanho
        anim = Animation(size=(400, 400), duration=0.8)
        anim.bind(on_complete=self.reset_animation)  # Vincula a função de retorno de chamada ao término da animação
        anim.start(self.resultado_sorteio)

        # Redefine o tamanho do botão
        #instance.size = (150, 50)

    def reset_animation(self, *args):
        # Define e inicia a animação de redução de tamanho
        anim = Animation(size=(300, 300), duration=0)
        anim.start(self.resultado_sorteio)

if __name__ == '__main__':
    VencedorApp().run()
