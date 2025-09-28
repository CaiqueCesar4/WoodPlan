from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class tela_orcamento_mao_de_obra(Screen):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.spinner_mao_obra = Spinner(
            text="Escolha a mão de obra",
            values=[row["nome"] for row in self.data.listar_mao_obra()],
            size_hint=(1, None),
            height=44,
        )

        add_btn = Button(text="Adicionar Mão de Obra", size_hint=(1, None), height=44)
        add_btn.bind(on_release=self.adicionar_mao_obra)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.itens_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.itens_layout.bind(minimum_height=self.itens_layout.setter("height"))
        self.scroll.add_widget(self.itens_layout)

        self.total_label = Label(
            text=f"Total Produtos: R$ {self.data.get_total():.2f}",
            size_hint=(1, None),
            height=40,
        )

        finalizar_btn = Button(text="Finalizar Orçamento Completo", size_hint=(1, None), height=44)
        finalizar_btn.bind(on_release=self.finalizar_orcamento)

        back_btn = Button(text="Voltar", size_hint=(1, None), height=44)
        back_btn.bind(on_release=lambda x: setattr(self.manager, "current", "principal"))

        root.add_widget(Label(text="Adicione mão de obra ao orçamento"))
        root.add_widget(self.spinner_mao_obra)
        root.add_widget(add_btn)
        root.add_widget(self.scroll)
        root.add_widget(self.total_label)
        root.add_widget(finalizar_btn)
        root.add_widget(back_btn)

        self.add_widget(root)

    def on_enter(self):
        self.spinner_mao_obra.values = [row["nome"] for row in self.data.listar_mao_obra()]

    def adicionar_mao_obra(self, instance):
        nome = self.spinner_mao_obra.text
        valor = self.data.adicionar_mao_obra_ao_total(nome)
        if valor == 0:
            return

        item_label = Label(
            text=f"Mão de Obra - {nome} - R$ {valor:.2f}",
            size_hint_y=None,
            height=30,
        )
        self.itens_layout.add_widget(item_label)
        self.total_label.text = f"Total Parcial + Mão de Obra: R$ {self.data.get_total():.2f}"

    def finalizar_orcamento(self, instance):
        final_label = Label(
            text=f"===== ORÇAMENTO FINAL =====\nTOTAL: R$ {self.data.get_total():.2f}",
            size_hint_y=None,
            height=50,
        )
        self.itens_layout.add_widget(final_label)