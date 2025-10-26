# telas/orcamento_mao_de_obra.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class TelaOrcamentoMaoDeObra(Screen):
    def __init__(self, data, orcamento_id=None, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.orcamento_id = orcamento_id
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=15)

        root.add_widget(Label(
            text="Orçamento - Mão de Obra",
            font_size=28,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=50
        ))

                # Informações do orçamento (nome e descrição)
        self.lbl_nome_orcamento = Label(
            text="",
            font_size=20,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=30
        )
        self.lbl_descricao_orcamento = Label(
            text="",
            font_size=14,
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=30
        )
        root.add_widget(self.lbl_nome_orcamento)
        root.add_widget(self.lbl_descricao_orcamento)

        self.spinner_trabalhador = Spinner(
            text="Selecione o trabalhador",
            values=[],
            size_hint=(1, None),
            height=50,
            background_color=(0.35, 0.35, 0.35, 1),
            color=(1, 1, 1, 1)
        )

        self.dias_input = TextInput(
            hint_text="Dias de trabalho",
            input_filter="int",
            size_hint=(1, None),
            height=45,
            foreground_color=(1, 1, 1, 1),
            background_color=(0.3, 0.3, 0.3, 1),
            cursor_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.7, 0.7, 1),
            padding=[10, 10],
        )

        add_btn = Button(
            text="Adicionar Mão de Obra",
            size_hint=(1, None),
            height=50,
            background_color=(0.45, 0.25, 0.15, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        add_btn.bind(on_release=self.adicionar_mao_de_obra)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.lista_layout = GridLayout(cols=1, spacing=8, size_hint_y=None)
        self.lista_layout.bind(minimum_height=self.lista_layout.setter("height"))
        self.scroll.add_widget(self.lista_layout)

        finalizar_btn = Button(
            text="Finalizar Orçamento",
            size_hint=(1, None),
            height=50,
            background_color=(0.45, 0.25, 0.15, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        finalizar_btn.bind(on_release=self.finalizar_orcamento)

        voltar_btn = Button(
            text="Voltar",
            size_hint=(1, None),
            height=45,
            background_color=(0.35, 0.35, 0.35, 1),
            color=(1, 1, 1, 1)
        )
        voltar_btn.bind(on_release=lambda x: setattr(self.manager, "current", "orcamento_modulo"))

        root.add_widget(self.spinner_trabalhador)
        root.add_widget(self.dias_input)
        root.add_widget(add_btn)
        root.add_widget(self.scroll)
        root.add_widget(finalizar_btn)
        root.add_widget(voltar_btn)

        self.add_widget(root)

    def on_pre_enter(self):
        """Carrega lista de trabalhadores e mostra info do orçamento"""
        trabalhadores = [t["nome_trabalhador"] for t in self.data.listar_mao_de_obra()]
        self.spinner_trabalhador.values = trabalhadores
        if trabalhadores:
            self.spinner_trabalhador.text = trabalhadores[0]

        orc_info = getattr(self.manager, "current_orcamento_info", None)
        if orc_info:
            self.lbl_nome_orcamento.text = f"Nome: {orc_info.get('nome', '(sem nome)')}"
            self.lbl_descricao_orcamento.text = f"Descrição: {orc_info.get('descricao', '(sem descrição)')}"
        elif self.orcamento_id:
            orc = self.data.obter_orcamento(self.orcamento_id)
            if orc:
                self.lbl_nome_orcamento.text = f"Nome: {orc['nome_orcamento']}"
                self.lbl_descricao_orcamento.text = f"Descrição: {orc['descricao'] or '(sem descrição)'}"
            else:
                self.lbl_nome_orcamento.text = ""
                self.lbl_descricao_orcamento.text = ""
        else:
            self.lbl_nome_orcamento.text = ""
            self.lbl_descricao_orcamento.text = ""

        self.atualizar_lista()

    def adicionar_mao_de_obra(self, instance):
        if not self.orcamento_id:
            print("⚠️ Nenhum orçamento selecionado.")
            return

        nome = self.spinner_trabalhador.text
        try:
            dias = int(self.dias_input.text)
        except ValueError:
            return

        trabalhador = next((t for t in self.data.listar_mao_de_obra() if t["nome_trabalhador"] == nome), None)
        if not trabalhador:
            return

        valor_total = dias * trabalhador["custo_dia"]
        self.data.adicionar_mao_de_obra_ao_orcamento(self.orcamento_id, trabalhador["id"], dias, valor_total)

        self.dias_input.text = ""
        self.atualizar_lista()

    def atualizar_lista(self):
        self.lista_layout.clear_widgets()
        for row in self.data.listar_mao_de_obra_do_orcamento(self.orcamento_id):
            linha = BoxLayout(size_hint_y=None, height=40)
            lbl = Label(
                text=f"{row['nome_trabalhador']} - {row['dias_utilizados']} dias - R$ {row['valor_total_servico']:.2f}",
                color=(1, 1, 1, 1)
            )
            linha.add_widget(lbl)
            self.lista_layout.add_widget(linha)

    def finalizar_orcamento(self, instance):
        if not self.orcamento_id:
            print("⚠️ Nenhum orçamento ativo para finalizar.")
            return

        total = self.data.calcular_total_orcamento(self.orcamento_id)
        print(f"💾 Orçamento {self.orcamento_id} finalizado! Total: R$ {total:.2f}")

        # Mostra o total na tela
        self.lista_layout.add_widget(Label(
            text=f"[b]TOTAL GERAL: R$ {total:.2f}[/b]",
            markup=True,
            color=(1, 1, 1, 1),
            font_size=20,
            size_hint_y=None,
            height=50
        ))

        # Limpa o estado atual (pronto para novo orçamento)
        self.orcamento_id = None
        self.dias_input.text = ""
        self.lista_layout.clear_widgets()
        self.manager.current_orcamento_info = None

        self.manager.current = "tela_inicial"