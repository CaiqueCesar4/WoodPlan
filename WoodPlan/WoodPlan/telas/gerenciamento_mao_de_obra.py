# telas/gerenciamento_mao_de_obra.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder

# Carrega tema visual
Builder.load_file("theme.kv")


class TelaGerenciamentoMaoDeObra(Screen):
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

        root.add_widget(Titulo(text="Gerenciar Mão de Obra"))

        # Botões principais
        botoes_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        add_btn = BotaoPadrao(text="Adicionar Trabalhador")
        back_btn = BotaoSecundario(text="Voltar")
        botoes_layout.add_widget(add_btn)
        botoes_layout.add_widget(back_btn)
        root.add_widget(botoes_layout)

        add_btn.bind(on_release=self.form_adicionar_trabalhador)
        back_btn.bind(on_release=lambda x: setattr(self.manager, "current", "tela_inicial"))

        # Área de rolagem
        self.scroll = ScrollView(size_hint=(1, 1))
        self.trabalhadores_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.trabalhadores_layout.bind(minimum_height=self.trabalhadores_layout.setter("height"))
        self.scroll.add_widget(self.trabalhadores_layout)
        root.add_widget(self.scroll)

        self.add_widget(root)

    def on_pre_enter(self):
        self.atualizar_lista()

    def atualizar_lista(self):
        self.trabalhadores_layout.clear_widgets()

        for row in self.data.listar_mao_de_obra():
            linha = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=[10, 5])

            lbl = Label(
                text=f"{row['nome_trabalhador']} — R$ {row['custo_dia']:.2f}/dia",
                halign="left",
                valign="middle",
                text_size=(400, None),
            )

            editar_btn = Button(text="Editar", size_hint=(None, 1), width=90)
            remover_btn = Button(text="Remover", size_hint=(None, 1), width=100)

            editar_btn.bind(on_release=lambda x, r=row: self.editar_trabalhador(r))
            remover_btn.bind(on_release=lambda x, r=row: self.remover_trabalhador(r["id"]))

            linha.add_widget(lbl)
            linha.add_widget(editar_btn)
            linha.add_widget(remover_btn)
            self.trabalhadores_layout.add_widget(linha)

    def form_adicionar_trabalhador(self, instance):
        self.trabalhadores_layout.clear_widgets()

        linha = BoxLayout(size_hint_y=None, height=50, spacing=10)
        nome_input = TextInput(hint_text="Nome do trabalhador", size_hint_x=0.5)
        custo_input = TextInput(hint_text="Custo por dia (R$)", input_filter="float", size_hint_x=0.3)
        salvar_btn = Button(text="Salvar", size_hint_x=0.2)

        linha.add_widget(nome_input)
        linha.add_widget(custo_input)
        linha.add_widget(salvar_btn)

        def salvar(instance):
            try:
                custo = float(custo_input.text)
            except ValueError:
                return
            self.data.adicionar_mao_de_obra(nome_input.text, custo)
            self.atualizar_lista()

        salvar_btn.bind(on_release=salvar)
        self.trabalhadores_layout.add_widget(linha)

    def editar_trabalhador(self, row):
        self.trabalhadores_layout.clear_widgets()

        linha = BoxLayout(size_hint_y=None, height=50, spacing=10)
        nome_input = TextInput(text=row["nome_trabalhador"], size_hint_x=0.5)
        custo_input = TextInput(text=str(row["custo_dia"]), input_filter="float", size_hint_x=0.3)
        salvar_btn = Button(text="Salvar", size_hint_x=0.2)

        linha.add_widget(nome_input)
        linha.add_widget(custo_input)
        linha.add_widget(salvar_btn)

        def salvar(instance):
            try:
                novo_custo = float(custo_input.text)
            except ValueError:
                return
            self.data.atualizar_mao_de_obra(row["id"], nome_input.text, novo_custo)
            self.atualizar_lista()

        salvar_btn.bind(on_release=salvar)
        self.trabalhadores_layout.add_widget(linha)

    def remover_trabalhador(self, trabalhador_id):
        self.data.remover_mao_de_obra(trabalhador_id)
        self.atualizar_lista()
