from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class tela_gerenciar_mao_de_obra(Screen):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        add_btn = Button(text="Adicionar Mão de Obra", size_hint=(1, None), height=44)
        add_btn.bind(on_release=self.form_adicionar_mao_obra)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.mao_obra_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.mao_obra_layout.bind(minimum_height=self.mao_obra_layout.setter("height"))
        self.scroll.add_widget(self.mao_obra_layout)

        back_btn = Button(text="Voltar", size_hint=(1, None), height=44)
        back_btn.bind(on_release=lambda x: setattr(self.manager, "current", "inicial"))

        root.add_widget(Label(text="Gerenciamento de mão de obra"))
        root.add_widget(add_btn)
        root.add_widget(self.scroll)
        root.add_widget(back_btn)

        self.add_widget(root)

    def form_adicionar_mao_obra(self, instance):
        self.mao_obra_layout.clear_widgets()

        linha = BoxLayout(size_hint_y=None, height=40)
        nome_input = TextInput(hint_text="Nome da mão de obra")
        valor_input = TextInput(hint_text="Valor (R$)", input_filter="float")
        salvar_btn = Button(text="Salvar", size_hint=(None, 1), width=80)

        def salvar(instance):
            try:
                valor = float(valor_input.text)
            except ValueError:
                return
            self.data.adicionar_mao_obra(nome_input.text, valor)
            self.on_enter()

        salvar_btn.bind(on_release=salvar)

        linha.add_widget(nome_input)
        linha.add_widget(valor_input)
        linha.add_widget(salvar_btn)

        self.mao_obra_layout.add_widget(linha)

    def on_enter(self):
        self.mao_obra_layout.clear_widgets()
        for row in self.data.listar_mao_obra():
            linha = BoxLayout(size_hint_y=None, height=40)
            lbl = Label(text=f"{row['nome']} - R$ {row['valor']:.2f}")

            editar_btn = Button(text="Editar", size_hint=(None, 1), width=80)
            remover_btn = Button(text="Remover", size_hint=(None, 1), width=80)

            editar_btn.bind(on_release=lambda x, r=row: self.editar_mao_obra(r))
            remover_btn.bind(on_release=lambda x, r=row: self.remover_mao_obra(r["id"]))

            linha.add_widget(lbl)
            linha.add_widget(editar_btn)
            linha.add_widget(remover_btn)
            self.mao_obra_layout.add_widget(linha)

    def editar_mao_obra(self, row):
        self.mao_obra_layout.clear_widgets()
        linha = BoxLayout(size_hint_y=None, height=40)
        nome_input = TextInput(text=row["nome"])
        valor_input = TextInput(text=str(row["valor"]), input_filter="float")
        salvar_btn = Button(text="Salvar", size_hint=(None, 1), width=80)

        def salvar(instance):
            try:
                novo_valor = float(valor_input.text)
            except ValueError:
                return
            self.data.atualizar_mao_obra(row["id"], nome_input.text, novo_valor)
            self.on_enter()

        salvar_btn.bind(on_release=salvar)

        linha.add_widget(nome_input)
        linha.add_widget(valor_input)
        linha.add_widget(salvar_btn)
        self.mao_obra_layout.add_widget(linha)

    def remover_mao_obra(self, mao_obra_id):
        self.data.remover_mao_obra(mao_obra_id)
        self.on_enter()
