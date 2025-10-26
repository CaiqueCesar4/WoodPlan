# telas/tela_inicial.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.factory import Factory
from kivy.graphics import Color, Rectangle

Builder.load_file("theme.kv")


class TelaInicial(Screen):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.build_ui()

    def build_ui(self):
        # Fundo (herdado do theme.kv)
        with self.canvas.before:
            Color(0.25, 0.25, 0.25, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # Referências aos componentes do tema
        Titulo = Factory.Titulo
        Subtitulo = Factory.Subtitulo
        BotaoPadrao = Factory.BotaoPadrao
        BotaoSecundario = Factory.BotaoSecundario

        # Layout principal
        root = BoxLayout(
            orientation="vertical",
            spacing=18,
            padding=[0, 100, 0, 40],  # sobe o conteúdo
        )

        # Título e subtítulo
        root.add_widget(Titulo(text="WoodPlan", font_size=42))
        root.add_widget(Subtitulo(text="Gerenciamento de Orçamentos e Produção"))
        root.add_widget(Widget(size_hint_y=None, height=20))

        # Botões
        botoes = GridLayout(cols=1, spacing=12, size_hint=(0.6, None))
        botoes.height = 4 * 56 + 3 * 12
        botoes.pos_hint = {"center_x": 0.5}

        btn_novo_orcamento = BotaoPadrao(text="Novo Orçamento")
        btn_gerenciar_modulos = BotaoSecundario(text="Gerenciar Módulos")
        btn_gerenciar_mao_obra = BotaoSecundario(text="Gerenciar Mão de Obra")
        btn_historico = BotaoSecundario(text="Histórico de Orçamentos")

        # Navegação
        def abrir_novo_orcamento(_):
            tela_modulo = self.manager.get_screen("orcamento_modulo")
            tela_mao = self.manager.get_screen("orcamento_mao_de_obra")
            tela_modulo.orcamento_id = None
            tela_mao.orcamento_id = None
            self.manager.current = "orcamento_modulo"

        btn_novo_orcamento.bind(on_release=abrir_novo_orcamento)
        btn_gerenciar_modulos.bind(on_release=lambda x: setattr(self.manager, "current", "gerenciamento_modulos"))
        btn_gerenciar_mao_obra.bind(on_release=lambda x: setattr(self.manager, "current", "gerenciamento_mao_de_obra"))
        btn_historico.bind(on_release=lambda x: setattr(self.manager, "current", "historico_orcamentos"))

        for b in (btn_novo_orcamento, btn_gerenciar_modulos, btn_gerenciar_mao_obra, btn_historico):
            botoes.add_widget(b)

        root.add_widget(botoes)
        root.add_widget(Widget(size_hint_y=None, height=40))

        self.add_widget(root)

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos