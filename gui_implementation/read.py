import tkinter as tk
from tkinter import font as tkFont
from crud_utils import CRUD_utils


class CRUD_read(tk.Tk):
    def __init__(self, MenuConstructor):
        """
        Classe para a interface de leitura (READ) de registros no banco de dados.
        
        Args:
            MenuConstructor: Construtor da classe do menu principal para navegação de volta.
        """
        super().__init__()
        self.utils = CRUD_utils(self, MenuConstructor)

        # Configuração de fontes
        bttn_font = tkFont.Font(family="Aptos", size=18)
        title_font = tkFont.Font(family="Aptos", size=48, weight=tkFont.BOLD)
        subtitle_font = tkFont.Font(family="Aptos", size=14)
        self.tag_font = tkFont.Font(family="Aptos", size=20)
        
        # Configuração de cores
        self.bg_color = "#1F1F1F"  # Cor de fundo escura
        fg_colors = {
            "active": "#E0E0E0",  # Cinza claro (para elementos ativos)
            "default": "#4FC3F7",  # Azul claro (para elementos selecionados)
        }

        # Configuração da janela
        self.geometry("1400x800")
        self.title("CRUD Menu")
        self.configure(bg=self.bg_color)

        # Variáveis para armazenar widgets e valores de filtro
        self.filter_vars = []  # Armazena os campos de filtro e suas configurações
        self.filter_widgets = []  # Armazena todos os widgets temporários

        # Variável para a opção de relação (tabela) selecionada
        self.relation_opt = tk.StringVar(master=self, value=self.utils.relations[0])

        # Elementos da interface
        self.title_label = tk.Label(
            master=self, 
            text="O Que Tem nesse BD?",
            fg="white",
            bg=self.bg_color,
            font=title_font
        )
        self.title_label.place(x=350, y=50)

        # Botão para aplicar filtros e mostrar resultados
        self.show_button = tk.Button(
            master=self, 
            text="Aplicar Filtros e Procurar", 
            bg="White",
            fg="black",
            font=bttn_font,
            padx=255,
            command=self.show_table
        )
        self.show_button.place(x=350, y=700)
        
        # Criação dos botões de rádio para seleção de tabelas
        for index, each_relation in enumerate(self.utils.relations):
            value = each_relation
            if each_relation in self.utils.relation_key:
                value = self.utils.relation_key[each_relation]
            
            rb = tk.Radiobutton(
                master=self,
                text=each_relation,
                variable=self.relation_opt,
                value=value,
                font=subtitle_font,
                bg=self.bg_color,
                fg=fg_colors["default"],
                activebackground=self.bg_color,
                activeforeground=fg_colors["active"],                
                selectcolor=self.bg_color,
                padx=10,
                pady=5,   
                anchor="w",  
                cursor="hand2",
                command=self.on_relation_select
            )
            rb.place(x=50, y=125 + 40 * index)
            
        # Adiciona o botão para voltar ao menu principal
        self.utils.place_home_bttn()

        # Coloca os filtros iniciais para a primeira tabela
        self.place_relation_filters()

    def get_width_height(self, widget: tk.Widget):
        """Obtém a largura e altura de um widget."""
        self.update()
        return widget.winfo_width(), widget.winfo_height()
    
    def show_table(self):
        """Gera e executa a query SQL com os filtros aplicados."""
        relation = self.relation_opt.get()
        query = f"SELECT * FROM {relation}"

        if self.filter_vars:
            filters = []
            for filter_var in self.filter_vars:
                # Obtém o valor do campo de filtro
                field_value = filter_var[0].get("1.0", tk.END).strip()
                column = filter_var[1]
                equivalence = filter_var[2].get()

                if field_value:
                    filters.append(f"{column} {equivalence} '{field_value}'")
            
            if filters:
                query += " WHERE " + " AND ".join(filters)
        
        query += ";"
        print(query)  # TODO: Substituir por execução real e exibição dos resultados

    def on_relation_select(self):
        """Atualiza os campos de filtro quando uma nova tabela é selecionada."""
        self.place_relation_filters()

    def place_relation_filters(self):
        """Posiciona os campos de filtro para a tabela selecionada."""
        self.destroy_temp_widgets()  # Remove widgets antigos
        rel_opt = self.relation_opt.get()

        # Coloca filtros para campos de texto e numéricos
        self.place_text_filters(self.utils.col_labl_pairs[rel_opt]["text_filters"])
        self.place_num_filter(self.utils.col_labl_pairs[rel_opt]["num_filters"])

    def place_text_filters(self, text_filters: list):
        """Cria e posiciona campos de filtro para texto.
        
        Args:
            text_filters: Lista de dicionários com informações dos campos de texto.
        """
        index_corection = len(self.filter_vars)
        
        for index, text_filter in enumerate(text_filters):
            y_iter = 150 + 80 * (index + index_corection)

            # Campo de entrada para filtro de texto
            filter_input = tk.Text(
                master=self,
                padx=80,
                pady=10,
                height=0,
                width=60
            )
            filter_input.place(x=500, y=y_iter)

            # Rótulo do campo
            filter_label = tk.Label(
                master=self,
                fg="white",
                bg=self.bg_color,
                text=text_filter["Label"],
                font=self.tag_font
            )
            filter_label.place(x=350, y=y_iter)

            # Operador de equivalência padrão para texto
            equivalence_opt = tk.StringVar(master=self, value="=")

            # Armazena referências para uso posterior
            self.filter_vars.append((filter_input, text_filter["Column"], equivalence_opt))
            self.filter_widgets.append(filter_input)
            self.filter_widgets.append(filter_label)

    def place_num_filter(self, num_filters: list):
        """Cria e posiciona campos de filtro para números/datas.
        
        Args:
            num_filters: Lista de dicionários com informações dos campos numéricos.
        """
        index_corection = len(self.filter_vars)
        
        for index, num_filter in enumerate(num_filters):
            y_iter = 150 + 80 * (index + index_corection)

            # Rótulo do campo
            filter_label = tk.Label(
                master=self,
                fg="white",
                bg=self.bg_color,
                text=num_filter["Label"],
                font=self.tag_font
            )
            filter_label.place(x=350, y=y_iter)

            # Menu de opções para operadores de comparação
            equivalence_opt = tk.StringVar(master=self, value="=")
            filter_config = tk.OptionMenu(
                self,
                equivalence_opt,
                "<", ">", "="
            )
            filter_config.place(x=500, y=y_iter + 5)

            # Campo de entrada para filtro numérico
            filter_input = tk.Text(
                master=self,
                padx=40,
                pady=10,
                height=0,
                width=60
            )
            filter_input.place(x=580, y=y_iter)

            # Armazena referências para uso posterior
            self.filter_vars.append((filter_input, num_filter["Column"], equivalence_opt))
            self.filter_widgets.append(filter_input)
            self.filter_widgets.append(filter_label)
            self.filter_widgets.append(filter_config)

    def destroy_temp_widgets(self):
        """Remove todos os widgets temporários da interface."""
        for each_widget in self.filter_widgets:
            each_widget.destroy()
        
        self.filter_vars.clear()
        self.filter_widgets.clear()