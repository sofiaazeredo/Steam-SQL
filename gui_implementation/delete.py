import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox as msg
from crud_utils import CRUD_utils

# Classe principal para a interface de deleção de registros em CRUD
class CRUD_delete(tk.Tk):
    """
    Classe que define a interface gráfica para deleção de registros em um banco de dados.
    A interface permite que o usuário selecione filtros e deleta registros baseados nesses filtros.
    """
    
    def __init__(self, MenuConstructor):
        """
        Construtor da classe CRUD_delete.
        
        Inicializa a janela principal, configura os estilos e componentes gráficos da interface.
        
        Args:
            MenuConstructor (obj): O construtor do menu que gerencia as relações disponíveis no banco de dados.
        """
        super().__init__()  # Chama o construtor da classe pai (Tkinter)

        # Instancia a classe de utilitários CRUD
        self.utils = CRUD_utils(self, MenuConstructor)

        # Definições de fontes
        bttn_font = tkFont.Font(family="Aptos", size=18)  # Fonte para botões
        title_font = tkFont.Font(family="Aptos", size=48, weight=tkFont.BOLD)  # Fonte para título
        subtitle_font = tkFont.Font(family="Aptos", size=14)  # Fonte para subtítulo
        self.tag_font = tkFont.Font(family="Aptos", size=20)  # Fonte para etiquetas (labels)

        # Definições de cores
        self.bg_color = "#1F1F1F"  # Cor de fundo escuro
        fg_colors = {
            "active": "#E0E0E0",  # Cor de texto ativa (cinza claro)
            "default": "#4FC3F7",  # Cor de texto padrão (azul claro)
        }

        # Configuração da janela principal
        self.geometry("1400x800")  # Tamanho da janela
        self.title("CRUD Menu")  # Título da janela
        self.configure(bg=self.bg_color)  # Cor de fundo da janela

        # Variáveis e widgets para filtros
        self.filter_vars = []  # Lista para armazenar variáveis dos filtros
        self.filter_widgets = []  # Lista para armazenar widgets dos filtros

        # Variável para armazenar a relação (tabela) selecionada
        self.relation_opt = tk.StringVar(master=self, value=self.utils.relations[0])

        # Título da tela de deleção
        self.title_label = tk.Label(master=self, text="Deletar Registros", fg="white", bg=self.bg_color, font=title_font)
        self.title_label.place(x=431, y=50)

        # Botão para aplicar filtros e deletar registros
        self.show_button = tk.Button(master=self, text="Aplicar Filtros e Deletar", bg="White", fg="black", font=bttn_font, padx=255, command=self.delete_query)
        self.show_button.place(x=350, y=700)
        
        # Criar os botões de seleção de relação (tabela) disponíveis
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
                font=subtitle_font,
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
            rb.place(x=50, y=145 + 40 * index)  # Posiciona o Radiobutton na tela

        # Método para adicionar um botão "Home" (de navegação)
        self.utils.place_home_bttn()

        # Coloca os filtros específicos da relação selecionada
        self.place_relation_filters()

    def get_width_height(self, widget: tk.Widget):
        """
        Obtém as dimensões de um widget após a atualização da interface.

        Args:
            widget (tk.Widget): O widget para o qual as dimensões serão obtidas.

        Returns:
            tuple: Tupla com a largura e altura do widget.
        """
        self.update()  # Atualiza a interface para garantir que o widget foi desenhado
        w = widget.winfo_width()  # Obtém a largura do widget
        h = widget.winfo_height()  # Obtém a altura do widget
        return w, h  # Retorna as dimensões

    def delete_query(self):
        """
        Gera a query SQL para deletar registros com base nos filtros fornecidos.
        Exibe um erro caso nenhum filtro tenha sido inserido.
        """
        # Recupera a relação (tabela) selecionada
        relation = self.relation_opt.get()
        query = f"DELETE FROM {relation} WHERE "  # Inicia a query DELETE

        filters = []  # Lista para armazenar os filtros

        # Loop para adicionar filtros à query
        for filter_var in self.filter_vars:
            field_value = filter_var[0].get("1.0", tk.END).strip()  # Obtém o valor do filtro
            column = filter_var[1]  # Coluna a ser filtrada
            equivalence = filter_var[2].get()  # Opção de comparação (igual, maior, menor)

            if field_value:  # Se o filtro não estiver vazio
                filters.append(f"{column} {equivalence} '{field_value}'")  # Adiciona o filtro à lista

        # Se houver filtros, monta a query SQL
        if filters:
            query += " AND ".join(filters)  # Junta os filtros com "AND"
            query += ";"  # Finaliza a query
            print(query)  # Exibe a query no console
        else:
            # Exibe erro caso não haja filtros inseridos
            msg.showerror(title="ERRO!", message="NENHUM FILTRO INSERIDO!!!!!!!")
            print("fail")  # Imprime falha no console

    def on_relation_select(self):
        """
        Função chamada quando o usuário seleciona uma nova relação (tabela).
        Chama a função para reposicionar filtros.
        """
        self.place_relation_filters()

    def place_relation_filters(self):
        """
        Coloca os filtros específicos para a relação selecionada.
        Limpa os filtros existentes antes de adicionar novos.
        """
        self.destroy_temp_widgets()  # Limpa widgets temporários de filtros
        rel_opt = self.relation_opt.get()  # Obtém a relação selecionada
        
        # Coloca filtros de texto e numéricos relacionados à relação selecionada
        self.place_text_filters(self.utils.col_labl_pairs[rel_opt]["text_filters"])
        self.place_num_filter(self.utils.col_labl_pairs[rel_opt]["num_filters"])

    def place_text_filters(self, text_filters: list):
        """
        Coloca filtros de texto na tela (campos de texto para pesquisa).

        Args:
            text_filters (list): Lista de filtros de texto para a relação selecionada.
        """
        index_corection = len(self.filter_vars)  # Ajuste para posição dos filtros
        for index, text_filter in enumerate(text_filters):
            y_iter = 150 + 80 * (index + index_corection)  # Ajusta posição do filtro na tela

            # Cria o campo de entrada de texto para o filtro
            filter_input = tk.Text(master=self, padx=80, pady=10, height=0, width=60)
            filter_input.place(x=500, y=y_iter)

            # Cria o rótulo para o filtro
            filter_label = tk.Label(master=self, fg="white", bg=self.bg_color, text=text_filter["Label"], font=self.tag_font)
            filter_label.place(x=350, y=y_iter)

            equivalence_opt = tk.StringVar(master=self, value="=")  # Opção de comparação (padrão "=")

            # Adiciona o filtro à lista de variáveis para manipulação futura
            self.filter_vars.append((filter_input, text_filter["Column"], equivalence_opt))
            self.filter_widgets.append(filter_input)
            self.filter_widgets.append(filter_label)

    def place_num_filter(self, num_filters: list):
        """
        Coloca filtros numéricos na tela (campos para comparação de valores numéricos).

        Args:
            num_filters (list): Lista de filtros numéricos para a relação selecionada.
        """
        index_corection = len(self.filter_vars)  # Ajuste para posição dos filtros
        for index, num_filter in enumerate(num_filters):
            y_iter = 150 + 80 * (index + index_corection)  # Ajusta posição do filtro

            # Cria o rótulo para o filtro numérico
            filter_label = tk.Label(master=self, fg="white", bg=self.bg_color, text=num_filter["Label"], font=self.tag_font)
            filter_label.place(x=350, y=y_iter)

            equivalence_opt = tk.StringVar(master=self, value="=")  # Opção de comparação
            filter_config = tk.OptionMenu(self, equivalence_opt, "<", ">", "=")  # Menu de seleção para o tipo de comparação
            filter_config.place(x=500, y=y_iter + 5)

            # Cria o campo de entrada para o filtro numérico
            filter_input = tk.Text(master=self, padx=40, pady=10, height=0, width=60)
            filter_input.place(x=580, y=y_iter)

            # Adiciona o filtro à lista de variáveis para manipulação futura
            self.filter_vars.append((filter_input, num_filter["Column"], equivalence_opt))
            self.filter_widgets.append(filter_input)
            self.filter_widgets.append(filter_label)
            self.filter_widgets.append(filter_config)

    def destroy_temp_widgets(self):
        """
        Destrói todos os widgets temporários (filtros) antes de criar novos.
        """
        for each_widget in self.filter_widgets:
            each_widget.destroy()  # Remove cada widget de filtro

        # Limpa as listas de variáveis e widgets
        self.filter_vars.clear()
        self.filter_widgets.clear()
