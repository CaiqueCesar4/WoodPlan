from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget


class tela_orcamento_modulo(Screen):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.spinner_categoria = Spinner(
            text="Escolha a categoria",
            values=self.data.get_categorias(),
            size_hint=(1, None),
            height=44,
        )
        self.spinner_categoria.bind(text=self.atualizar_subprodutos)

        self.spinner_subproduto = Spinner(
            text="Escolha o subproduto",
            values=[],
            size_hint=(1, None),
            height=44,
        )

        self.largura_input = TextInput(hint_text="Largura (m)", input_filter="float")
        self.altura_input = TextInput(hint_text="Altura (m)", input_filter="float")

        add_btn = Button(text="Adicionar", size_hint=(1, None), height=44)
        add_btn.bind(on_release=self.adicionar_item)

        finalize_btn = Button(text="Finalizar Orçamento", size_hint=(1, None), height=44)
        finalize_btn.bind(on_release=self.finalizar_orcamento)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.itens_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.itens_layout.bind(minimum_height=self.itens_layout.setter("height"))
        self.scroll.add_widget(self.itens_layout)

        self.total_label = Label(text="Total: R$ 0.00", size_hint=(1, None), height=40)

        back_btn = Button(text="Voltar", size_hint=(1, None), height=44)
        back_btn.bind(on_release=lambda x: setattr(self.manager, "current", "inicial"))

        root.add_widget(self.spinner_categoria)
        root.add_widget(self.spinner_subproduto)
        root.add_widget(self.largura_input)
        root.add_widget(self.altura_input)
        root.add_widget(add_btn)
        root.add_widget(finalize_btn)
        root.add_widget(self.scroll)
        root.add_widget(self.total_label)
        root.add_widget(back_btn)

        self.add_widget(root)

    def atualizar_subprodutos(self, spinner, categoria):
        subprodutos = list(self.data.get_subprodutos(categoria).keys())
        self.spinner_subproduto.values = subprodutos if subprodutos else []
        self.spinner_subproduto.text = subprodutos[0] if subprodutos else "Escolha o subproduto"

    def adicionar_item(self, instance):
        categoria = self.spinner_categoria.text
        subproduto = self.spinner_subproduto.text
        try:
            largura = float(self.largura_input.text)
            altura = float(self.altura_input.text)
        except ValueError:
            return

        valor_item = self.data.calcular_valor(categoria, subproduto, largura, altura)
        if valor_item == 0:
            return

        area = largura * altura
        item_label = Label(
            text=f"{categoria} - {subproduto} - {area:.2f} m² - R$ {valor_item:.2f}",
            size_hint_y=None,
            height=30,
        )
        self.itens_layout.add_widget(item_label)
        self.total_label.text = f"Total: R$ {self.data.get_total():.2f}"

        self.largura_input.text = ""
        self.altura_input.text = ""

    def finalizar_orcamento(self, instance):
        self.manager.current = "orcamento mao obra"