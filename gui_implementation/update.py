import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox as msg
from crud_utils import CRUD_utils
from conn_handle import DBConnection

# Classe principal para a interface de atualização de registros em CRUD
class CRUD_update(tk.Tk):
    """
    Classe que define a interface gráfica para atualização de registros em um banco de dados.
    A interface permite que o usuário selecione filtros e campos para atualização, gerando
    uma query SQL correspondente.
    """
    def __init__(self, MenuConstructor):
        """
        Construtor da classe CRUD_update.
        
        Inicializa a janela principal e todos os componentes da interface gráfica.
        
        Args:
            MenuConstructor (obj): O construtor do menu que gera a interface de seleção de relações.
        """
        super().__init__()  # Chama o construtor da classe pai (Tkinter)
        
        # Instancia a classe de utilitários CRUD
        self.utils = CRUD_utils(self, MenuConstructor)
        self.db = DBConnection()

        # Definições de fontes
        bttn_font = tkFont.Font(family="Aptos", size=18)  # Fonte para botões
        title_font = tkFont.Font(family="Aptos", size=48, weight=tkFont.BOLD)  # Fonte para título
        subtitle_font = tkFont.Font(family="Aptos", size=24)  # Fonte para subtítulo
        opt_font = tkFont.Font(family="Aptos", size=14)  # Fonte para opções
        self.tag_font = tkFont.Font(family="Aptos", size=20)  # Fonte para etiquetas (labels)

        # Cores da interface
        self.bg_color = "#1F1F1F"  # Cor de fundo escuro
        fg_colors = {
            "active": "#E0E0E0",  # Cor de texto ativa (cinza claro)
            "default": "#4FC3F7",  # Cor de texto padrão (azul claro)
        }

        # Configuração da janela principal
        self.geometry("1400x800")  # Tamanho da janela
        self.title("CRUD Menu")  # Título da janela
        self.configure(bg=self.bg_color)  # Cor de fundo da janela

        # Variáveis e widgets para filtros e atualizações
        self.filter_vars = []  # Lista para armazenar variáveis dos filtros
        self.filter_widgets = []  # Lista para armazenar widgets dos filtros

        self.update_vars = []  # Lista para armazenar variáveis das atualizações
        self.update_widgets = []  # Lista para armazenar widgets das atualizações

        # Variável para armazenar a relação (tabela) selecionada
        self.relation_opt = tk.StringVar(master=self, value=self.utils.relations[0])

        # Título da tela de atualização
        self.title_label = tk.Label(master=self, text="Atualizar Registros", fg="white", bg=self.bg_color, font=title_font)
        self.title_label.place(x=405, y=30)

        # Botão para aplicar filtros e atualizar registros
        self.show_button = tk.Button(master=self, text="Aplicar Filtros e Atualizar", bg="White", fg="black", font=bttn_font, padx=255, command=self.gen_update_query)
        self.show_button.place(x=350, y=700)

        # Labels para seções de Filtros e Atualizações
        self.filter_section_label = tk.Label(master=self, text="Filtros", bg=self.bg_color, fg="white", font=subtitle_font)
        self.filter_section_label.place(x=620, y=140)

        self.update_section_label = tk.Label(master=self, text="Atualizações", bg=self.bg_color, fg="white", font=subtitle_font)
        self.update_section_label.place(x=910, y=140)

        # Adiciona os botões de seleção de relação (tabela)
        for index, each_relation in enumerate(self.utils.relations):
            value = each_relation
            if(each_relation in self.utils.relation_key):
                value = self.utils.relation_key[each_relation]
            
            # Criação do botão de seleção (Radiobutton) para cada relação
            rb = tk.Radiobutton(
                master=self,
                text=each_relation,
                variable=self.relation_opt,
                value=value,
                font=opt_font,
                bg=self.bg_color,
                fg=fg_colors["default"],
                activebackground=self.bg_color,
                activeforeground=fg_colors["active"],                
                selectcolor=self.bg_color,
                padx=10,
                pady=5,
                anchor="w",  # Alinhamento à esquerda
                cursor="hand2",  # Cursor de mão para indicar interatividade
                command=self.on_relation_select  # Chama função ao selecionar uma relação
            )
            rb.place(x=50, y=145+40*index)  # Posiciona o Radiobutton na tela

        # Método para adicionar um botão "Home" (de navegação)
        self.utils.place_home_bttn()

        # Chama função para posicionar filtros e campos de atualização
        self.place_all_filters()

    def get_width_height(self, widget: tk.Widget):
        """
        Obtém as dimensões de um widget após a atualização.

        Args:
            widget (tk.Widget): O widget para o qual as dimensões serão obtidas.

        Returns:
            tuple: Tupla com largura e altura do widget.
        """
        self.update()  # Atualiza a interface para garantir que o widget foi desenhado
        w = widget.winfo_width()  # Obtém a largura
        h = widget.winfo_height()  # Obtém a altura
        return w, h  # Retorna as dimensões

    def gen_update_query(self):
        """
        Gera a query SQL para atualização dos registros no banco de dados com base nos filtros e dados fornecidos.
        Exibe um erro caso os campos necessários não sejam preenchidos.
        """
        relation = self.relation_opt.get()  # Obtém a relação (tabela) selecionada
        query = f"UPDATE {relation} SET "  # Começa a query de atualização

        filters = []  # Lista de filtros
        updates = []  # Lista de atualizações

        # Loop para construir os filtros
        for each_var in self.filter_vars:
            field_input = each_var[0].get("1.0", tk.END).strip()  # Obtém o valor do filtro
            field_column = each_var[1]  # Coluna a ser filtrada
            field_equivalence = each_var[2].get().strip()  # Opção de comparação (igual, maior, menor)

            if field_input:
                filters.append(f"{field_column} {field_equivalence} '{field_input}'")

        # Loop para construir as atualizações
        for each_var in self.update_vars:
            field_input = each_var[0].get("1.0", tk.END).strip()  # Obtém o valor de atualização
            field_column = each_var[1]  # Coluna a ser atualizada
            
            if field_input:
                updates.append(f"{field_column} = '{field_input}'")

        # Se houver filtros e atualizações, monta a query SQL
        if filters and updates:
            query += ", ".join(updates)
            query += " WHERE " + " AND ".join(filters) + ";"
            self.db.execute(query=query)
        else:
            # Exibe erro se campos obrigatórios não forem preenchidos
            msg.showerror(title="ERRO!", message="CAMPOS CRUCIAIS VAZIOS!!!!!!!")

    def on_relation_select(self):
        """
        Função chamada quando o usuário seleciona uma nova relação (tabela).
        Chama a função para reposicionar filtros e campos de atualização.
        """
        self.place_all_filters()

    def place_all_filters(self):
        """
        Coloca todos os filtros e campos de atualização na tela com base na relação selecionada.
        Destrói widgets temporários antes de criar novos.
        """
        self.destroy_temp_widgets()  # Limpa filtros e campos de atualização anteriores
        rel_opt = self.relation_opt.get()  # Obtém a relação selecionada

        # Coloca filtros de texto e numéricos e campos de atualização
        self.place_text_filters(self.utils.col_labl_pairs[rel_opt]["text_filters"])
        self.place_num_filter(self.utils.col_labl_pairs[rel_opt]["num_filters"])
        all_columns = self.utils.col_labl_pairs[rel_opt]["text_filters"] + self.utils.col_labl_pairs[rel_opt]["num_filters"]
        self.place_update_fields(all_columns)

    def place_text_filters(self, text_cols: list):
        """
        Coloca filtros de texto (campos de texto para pesquisa).

        Args:
            text_cols (list): Lista de colunas que serão usadas como filtros de texto.
        """
        index_corection = len(self.filter_vars)
        for index, filter_spec in enumerate(text_cols):
            y_iter = 200 + 70 * (index + index_corection)

            # Cria o campo de entrada para o filtro de texto
            filter_input = tk.Text(master=self, padx=40, pady=10, height=0, width=32)
            filter_input.place(x=500, y=y_iter)

            # Cria o rótulo para o filtro
            filter_label = tk.Label(master=self, fg="white", bg=self.bg_color, text=filter_spec["Label"], font=self.tag_font)
            filter_label.place(x=350, y=y_iter)

            equivalence_opt = tk.StringVar(master=self, value="=")  # Opção de comparação

            # Adiciona o filtro às listas para manipulação posterior
            self.filter_vars.append((filter_input, filter_spec["Column"], equivalence_opt))
            self.filter_widgets.append(filter_input)
            self.filter_widgets.append(filter_label)

    def place_num_filter(self, num_cols: list):
        """
        Coloca filtros numéricos (campos para comparação de valores numéricos).

        Args:
            num_cols (list): Lista de colunas que serão usadas como filtros numéricos.
        """
        index_corection = len(self.filter_vars)
        for index, filter_spec in enumerate(num_cols):
            y_iter = 200 + 70 * (index + index_corection)

            # Cria o rótulo para o filtro numérico
            filter_label = tk.Label(master=self, fg="white", bg=self.bg_color, text=filter_spec["Label"], font=self.tag_font)
            filter_label.place(x=350, y=y_iter)

            equivalence_opt = tk.StringVar(master=self, value="=")  # Opção de comparação
            filter_config = tk.OptionMenu(self, equivalence_opt, "<", ">", "=")  # Menu para escolher a comparação
            filter_config.place(x=500, y=y_iter + 5)

            # Cria o campo de entrada para o filtro numérico
            filter_input = tk.Text(master=self, padx=0, pady=10, height=0, width=32)
            filter_input.place(x=580, y=y_iter)

            # Adiciona o filtro às listas para manipulação posterior
            self.filter_vars.append((filter_input, filter_spec["Column"], equivalence_opt))
            self.filter_widgets.append(filter_input)
            self.filter_widgets.append(filter_label)
            self.filter_widgets.append(filter_config)

    def place_update_fields(self, cols_list: list):
        """
        Coloca os campos de atualização de registros na tela.
        
        Args:
            cols_list (list): Lista de colunas que serão usadas para atualização de dados.
        """
        for index, column_spec in enumerate(cols_list):
            y_iter = 200 + 70 * (index)

            # Cria o campo de entrada para a atualização de dados
            input_field = tk.Text(master=self, padx=10, pady=10, height=0, width=32)
            input_field.place(x=865, y=y_iter)

            # Adiciona o campo às listas para manipulação posterior
            self.update_vars.append((input_field, column_spec["Column"]))
            self.update_widgets.append(input_field)

    def destroy_temp_widgets(self):
        """
        Destrói todos os widgets temporários (filtros e campos de atualização) antes de criar novos.
        """
        for each_widget in self.filter_widgets:
            each_widget.destroy()

        for each_widget in self.update_widgets:
            each_widget.destroy()

        # Limpa as listas de variáveis e widgets
        self.filter_vars.clear()
        self.filter_widgets.clear()
        self.update_widgets.clear()
        self.update_vars.clear()
