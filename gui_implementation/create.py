import tkinter as tk
from tkinter import font as tkFont
from crud_utils import CRUD_utils
from conn_handle import DBConnection

class CRUD_create(tk.Tk):
    def __init__(self, MenuConstructor):
        """
        Classe para a interface de criação (CREATE) de registros no banco de dados.
        
        Args:
            MenuConstructor: Construtor da classe do menu principal para navegação de volta.
        """
        super().__init__()
        self.utils = CRUD_utils(self, MenuConstructor)  # Instância das utilidades CRUD
        self.db = DBConnection()
        
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

        # Variáveis para armazenar widgets e valores de inserção
        self.insertion_vars = []  # Armazena os campos de entrada e suas colunas correspondentes
        self.insertion_widgets = []  # Armazena todos os widgets temporários

        # Variável para a opção de relação (tabela) selecionada
        self.relation_opt = tk.StringVar(master=self, value=self.utils.relations[0])

        # Elementos da interface
        self.title_label = tk.Label(
            master=self, 
            text="O que tem de Novo?",
            fg="white",
            bg=self.bg_color,
            font=title_font
        )
        self.title_label.place(x=385, y=50)

        # Botão para inserir novos registros
        self.show_button = tk.Button(
            master=self, 
            text="Inserir Novo Registro", 
            bg="White",
            fg="black",
            font=bttn_font,
            padx=255,
            command=self.insert_values
        )
        self.show_button.place(x=350, y=700)
        
        # Criação dos botões de rádio para seleção de tabelas
        for index, each_relation in enumerate(self.utils.relations):
            value = each_relation

            # Verifica se o nome da relação precisa ser convertido
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

        # Coloca os campos de inserção iniciais
        self.place_insert_fields()
    
    def insert_values(self):
        """Gera e executa a query SQL para inserção dos valores."""
        relation = self.relation_opt.get()
        query = f"INSERT INTO {relation}"

        if self.insertion_vars:
            insert_vals = []
            insert_cols = []
            for filter_var in self.insertion_vars:
                # Obtém o valor do campo de texto
                field_value = filter_var[0].get("1.0", tk.END).strip()
                column = filter_var[1]

                if field_value:
                    insert_vals.append(f"'{field_value}'")    
                    insert_cols.append(column)           
            
            if insert_vals:
                query += " (" + ", ".join(insert_cols) + ")"
                query += " VALUES (" + ", ".join(insert_vals) + ")"
        
        query += ";"
        self.db.execute(query=query)

    def on_relation_select(self):
        """Atualiza os campos de inserção quando uma nova tabela é selecionada."""
        self.place_insert_fields()

    def place_insert_fields(self):
        """Posiciona os campos de inserção para a tabela selecionada."""
        self.destroy_temp_widgets()  # Remove widgets antigos
        rel_opt = self.relation_opt.get()
        
        # Combina filtros de texto e numéricos
        all_columns = (
            self.utils.col_labl_pairs[rel_opt]["text_filters"] + 
            self.utils.col_labl_pairs[rel_opt]["num_filters"]
        )
        
        self.place_inputs(all_columns)

    def place_inputs(self, text_insert_fields: list):
        """Cria e posiciona os campos de entrada na interface.
        
        Args:
            text_insert_fields: Lista de dicionários com informações dos campos.
        """
        index_corection = len(self.insertion_vars)
        
        for index, insert_val in enumerate(text_insert_fields):
            y_iter = 150 + 80 * (index + index_corection)

            # Campo de entrada de texto
            field_input = tk.Text(
                master=self,
                padx=80,
                pady=10,
                height=0,
                width=60
            )
            field_input.place(x=500, y=y_iter)

            # Rótulo do campo
            field_label = tk.Label(
                master=self,
                fg="white",
                bg=self.bg_color,
                text=insert_val["Label"],
                font=self.tag_font
            )
            field_label.place(x=350, y=y_iter)

            # Armazena referências para uso posterior
            self.insertion_vars.append((field_input, insert_val["Column"]))
            self.insertion_widgets.append(field_input)
            self.insertion_widgets.append(field_label)

    def destroy_temp_widgets(self):
        """Remove todos os widgets temporários da interface."""
        for each_widget in self.insertion_widgets:
            each_widget.destroy()
        
        self.insertion_vars.clear()
        self.insertion_widgets.clear()