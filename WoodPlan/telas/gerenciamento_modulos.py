# telas/gerenciamento_modulos.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder

# Carrega tema global
Builder.load_file("theme.kv")


class TelaGerenciamentoModulos(Screen):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.build_ui()

    def build_ui(self):
        from kivy.factory import Factory
        Titulo = Factory.Titulo
        BotaoPadrao = Factory.BotaoPadrao
        BotaoSecundario = Factory.BotaoSecundario

        root = BoxLayout(orientation="vertical", padding=40, spacing=20)

        root.add_widget(Titulo(text="Gerenciar Módulos"))

        # Botões principais
        botoes_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        add_btn = BotaoPadrao(text="Adicionar Módulo")
        back_btn = BotaoSecundario(text="Voltar")
        botoes_layout.add_widget(add_btn)
        botoes_layout.add_widget(back_btn)
        root.add_widget(botoes_layout)

        add_btn.bind(on_release=self.form_adicionar_modulo)
        back_btn.bind(on_release=lambda x: setattr(self.manager, "current", "tela_inicial"))

        # Scroll com lista
        self.scroll = ScrollView(size_hint=(1, 1))
        self.modulos_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.modulos_layout.bind(minimum_height=self.modulos_layout.setter("height"))
        self.scroll.add_widget(self.modulos_layout)
        root.add_widget(self.scroll)

        self.add_widget(root)

    def on_pre_enter(self):
        self.atualizar_lista()

    def atualizar_lista(self):
        self.modulos_layout.clear_widgets()

        for row in self.data.listar_modulos():
            linha = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=[10, 5])

            lbl = Label(
                text=f"{row['nome_modulo']} — R$ {row['valor_base']:.2f}/m²",
                halign="left",
                valign="middle",
                text_size=(400, None),
            )

            editar_btn = Button(text="Editar", size_hint=(None, 1), width=90)
            remover_btn = Button(text="Remover", size_hint=(None, 1), width=100)

            editar_btn.bind(on_release=lambda x, r=row: self.editar_modulo(r))
            remover_btn.bind(on_release=lambda x, r=row: self.remover_modulo(r["id"]))

            linha.add_widget(lbl)
            linha.add_widget(editar_btn)
            linha.add_widget(remover_btn)
            self.modulos_layout.add_widget(linha)

    def form_adicionar_modulo(self, instance):
        self.modulos_layout.clear_widgets()

        linha = BoxLayout(size_hint_y=None, height=50, spacing=10)
        nome_input = TextInput(hint_text="Nome do módulo", size_hint_x=0.5)
        valor_input = TextInput(hint_text="Valor base (R$/m²)", input_filter="float", size_hint_x=0.3)
        salvar_btn = Button(text="Salvar", size_hint_x=0.2)

        linha.add_widget(nome_input)
        linha.add_widget(valor_input)
        linha.add_widget(salvar_btn)

        def salvar(instance):
            try:
                valor = float(valor_input.text)
            except ValueError:
                return
            self.data.adicionar_modulo(nome_input.text, valor)
            self.atualizar_lista()

        salvar_btn.bind(on_release=salvar)
        self.modulos_layout.add_widget(linha)

    def editar_modulo(self, row):
        self.modulos_layout.clear_widgets()

        linha = BoxLayout(size_hint_y=None, height=50, spacing=10)
        nome_input = TextInput(text=row["nome_modulo"], size_hint_x=0.5)
        valor_input = TextInput(text=str(row["valor_base"]), input_filter="float", size_hint_x=0.3)
        salvar_btn = Button(text="Salvar", size_hint_x=0.2)

        linha.add_widget(nome_input)
        linha.add_widget(valor_input)
        linha.add_widget(salvar_btn)

        def salvar(instance):
            try:
                novo_valor = float(valor_input.text)
            except ValueError:
                return
            self.data.atualizar_modulo(row["id"], nome_input.text, novo_valor)
            self.atualizar_lista()

        salvar_btn.bind(on_release=salvar)
        self.modulos_layout.add_widget(linha)

    def remover_modulo(self, modulo_id):
        self.data.remover_modulo(modulo_id)
        self.atualizar_lista()