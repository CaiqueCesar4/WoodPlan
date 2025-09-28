from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class tela_gerenciar_modulos(Screen):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        add_btn = Button(text="Adicionar Módulo", size_hint=(1, None), height=44)
        add_btn.bind(on_release=self.form_adicionar_modulo)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.subprodutos_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.subprodutos_layout.bind(minimum_height=self.subprodutos_layout.setter("height"))
        self.scroll.add_widget(self.subprodutos_layout)

        back_btn = Button(text="Voltar", size_hint=(1, None), height=44)
        back_btn.bind(on_release=lambda x: setattr(self.manager, "current", "inicial"))

        root.add_widget(Label(text="Gerenciamento de módulos"))
        root.add_widget(add_btn)
        root.add_widget(self.scroll)
        root.add_widget(back_btn)

        self.add_widget(root)

    def form_adicionar_modulo(self, instance):
        self.subprodutos_layout.clear_widgets()

        linha = BoxLayout(size_hint_y=None, height=40)
        categoria_input = TextInput(hint_text="Categoria")
        nome_input = TextInput(hint_text="Nome do módulo")
        preco_input = TextInput(hint_text="Preço por m²", input_filter="float")
        salvar_btn = Button(text="Salvar", size_hint=(None, 1), width=80)

        def salvar(instance):
            try:
                preco = float(preco_input.text)
            except ValueError:
                return
            self.data.adicionar_subproduto(
                categoria_input.text, nome_input.text, preco
            )
            self.on_enter()

        salvar_btn.bind(on_release=salvar)

        linha.add_widget(categoria_input)
        linha.add_widget(nome_input)
        linha.add_widget(preco_input)
        linha.add_widget(salvar_btn)

        self.subprodutos_layout.add_widget(linha)

    def on_enter(self):
        self.subprodutos_layout.clear_widgets()
        for row in self.data.listar_todos_subprodutos():
            linha = BoxLayout(size_hint_y=None, height=40)
            lbl = Label(text=f"{row['categoria']} - {row['nome']} (R$ {row['preco_m2']:.2f}/m²)")

            editar_btn = Button(text="Editar", size_hint=(None, 1), width=80)
            remover_btn = Button(text="Remover", size_hint=(None, 1), width=80)

            editar_btn.bind(on_release=lambda x, r=row: self.editar_subproduto(r))
            remover_btn.bind(on_release=lambda x, r=row: self.remover_subproduto(r["id"]))

            linha.add_widget(lbl)
            linha.add_widget(editar_btn)
            linha.add_widget(remover_btn)
            self.subprodutos_layout.add_widget(linha)

    def editar_subproduto(self, row):
        self.subprodutos_layout.clear_widgets()
        linha = BoxLayout(size_hint_y=None, height=40)
        nome_input = TextInput(text=row["nome"])
        preco_input = TextInput(text=str(row["preco_m2"]), input_filter="float")
        salvar_btn = Button(text="Salvar", size_hint=(None, 1), width=80)

        def salvar(instance):
            try:
                novo_preco = float(preco_input.text)
            except ValueError:
                return
            self.data.atualizar_subproduto(row["id"], nome_input.text, novo_preco)
            self.on_enter()

        salvar_btn.bind(on_release=salvar)

        linha.add_widget(Label(text=row["categoria"]))
        linha.add_widget(nome_input)
        linha.add_widget(preco_input)
        linha.add_widget(salvar_btn)
        self.subprodutos_layout.add_widget(linha)

    def remover_subproduto(self, subproduto_id):
        self.data.remover_subproduto(subproduto_id)
        self.on_enter()