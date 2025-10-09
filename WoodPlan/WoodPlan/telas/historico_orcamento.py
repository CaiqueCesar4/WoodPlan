from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class TelaHistoricoOrcamentos(Screen):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Título
        root.add_widget(Label(
            text="Histórico de Orçamentos",
            font_size=28,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=60
        ))

        # Scroll com lista de orçamentos
        self.scroll = ScrollView(size_hint=(1, 1))
        self.lista_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.lista_layout.bind(minimum_height=self.lista_layout.setter("height"))
        self.scroll.add_widget(self.lista_layout)
        root.add_widget(self.scroll)

        # Botão voltar
        voltar_btn = Button(
            text="Voltar",
            size_hint=(1, None),
            height=50,
            background_color=(0.35, 0.35, 0.35, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        voltar_btn.bind(on_release=lambda x: setattr(self.manager, "current", "tela_inicial"))
        root.add_widget(voltar_btn)

        self.add_widget(root)

    def on_pre_enter(self):
        """Carrega a lista de orçamentos"""
        self.lista_layout.clear_widgets()
        orcamentos = self.data.listar_orcamentos()

        if not orcamentos:
            self.lista_layout.add_widget(Label(
                text="Nenhum orçamento cadastrado ainda.",
                color=(1, 1, 1, 1),
                font_size=18,
                size_hint_y=None,
                height=50
            ))
            return

        for o in orcamentos:
            total = self.data.calcular_total_orcamento(o["id"])
            linha = BoxLayout(size_hint_y=None, height=50)
            lbl = Label(
                text=f"{o['nome_orcamento']} • {o['data_criacao']} • Total: R$ {total:.2f}",
                color=(1, 1, 1, 1),
                halign="left"
            )
            linha.add_widget(lbl)
            self.lista_layout.add_widget(linha)
