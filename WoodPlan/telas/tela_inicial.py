# tela_inicial.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.label import Label

# Carrega o tema global
Builder.load_file("theme.kv")


class TelaInicial(Screen):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", padding=40, spacing=30)

        # Logo (opcional, caso queira adicionar um)
        logo = Image(source="assets/logo.png", size_hint=(1, 0.4), allow_stretch=True)
        root.add_widget(logo)

        # Título
        from kivy.factory import Factory
        Titulo = Factory.Titulo
        Subtitulo = Factory.Subtitulo
        BotaoPadrao = Factory.BotaoPadrao
        BotaoSecundario = Factory.BotaoSecundario

        root.add_widget(Titulo(text="WoodPlan"))
        root.add_widget(Subtitulo(text="Gerenciamento de Orçamentos e Produção"))

        root.add_widget(Widget(size_hint_y=None, height=30))

        # Botões principais
        btn_novo_orcamento = BotaoPadrao(text="Novo Orçamento")
        btn_gerenciar_modulos = BotaoSecundario(text="Gerenciar Módulos")
        btn_gerenciar_mao_obra = BotaoSecundario(text="Gerenciar Mão de Obra")
        btn_historico = BotaoSecundario(text="Histórico de Orçamentos")

        def abrir_novo_orcamento(instance):
            novo_id = self.data.criar_orcamento("Novo Orçamento")
            print(f"🆕 Novo orçamento criado! ID = {novo_id}")

            tela_modulo = self.manager.get_screen("orcamento_modulo")
            tela_mao = self.manager.get_screen("orcamento_mao_de_obra")

            tela_modulo.orcamento_id = novo_id
            tela_mao.orcamento_id = novo_id

            self.manager.current = "orcamento_modulo"

        btn_novo_orcamento.bind(on_release=abrir_novo_orcamento)

        btn_gerenciar_modulos.bind(on_release=lambda x: setattr(self.manager, "current", "gerenciamento_modulos"))
        btn_gerenciar_mao_obra.bind(on_release=lambda x: setattr(self.manager, "current", "gerenciamento_mao_de_obra"))
        btn_historico.bind(on_release=lambda x: setattr(self.manager, "current", "historico_orcamentos"))


        root.add_widget(btn_novo_orcamento)
        root.add_widget(btn_gerenciar_modulos)
        root.add_widget(btn_gerenciar_mao_obra)
        root.add_widget(btn_historico)

        root.add_widget(Widget(size_hint_y=None, height=50))

        # Rodapé
        rodape = Label(
            text="© 2025 WoodPlan • Sistema de Marcenaria",
            font_size=12,
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=30,
            halign="center",
            valign="middle",
            text_size=(400, None),
        )
        root.add_widget(rodape)

        self.add_widget(root)
