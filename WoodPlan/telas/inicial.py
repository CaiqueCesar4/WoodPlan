from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class tela_inicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=20)

        novo_btn = Button(text="Novo Orçamento", size_hint=(1, None), height=60)
        novo_btn.bind(on_release=lambda x: setattr(self.manager, "current", "orcamento modulos"))

        gerenciar_btn = Button(text="Gerenciar Módulos", size_hint=(1, None), height=60)
        gerenciar_btn.bind(on_release=lambda x: setattr(self.manager, "current", "gerenciamento de modulos"))

        mao_obra_btn = Button(text="Gerenciar Mão de Obra", size_hint=(1, None), height=60)
        mao_obra_btn.bind(on_release=lambda x: setattr(self.manager, "current", "gerenciar_mao_obra"))

        root.add_widget(novo_btn)
        root.add_widget(gerenciar_btn)
        root.add_widget(mao_obra_btn)

        self.add_widget(root)