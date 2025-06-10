import tkinter as tk
from tkinter import font as tkFont

class CRUD_utils():
    """
    Classe utilitária para operações CRUD (Create, Read, Update, Delete) em um banco de dados.
    Fornece métodos e estruturas de dados comuns para as operações CRUD.
    """
    def __init__(self, master: tk.Tk, MenuConstructor):
        """
        Inicializa a classe utilitária CRUD.

        Args:
            master (tk.Tk): A janela principal do Tkinter.
            MenuConstructor: Construtor da classe do menu principal para navegação.
        """
        self.master = master  # Referência à janela principal
        self.MenuConstructor = MenuConstructor  # Construtor do menu principal

        # Lista de relações (tabelas) disponíveis no banco de dados
        self.relations = [
            "usuario", "avaliacao", "desenvolvedor", "dist. contrata dev.", 
            "dev. desenvolve jogo", "dist. distribui jogo", "distribuidor", 
            "familia", "genero", "jogo", "transacao", "usr. amigo de usr.", 
            "usr.joga. jogo"
        ]
        
        # Mapeamento de nomes de relações para chaves simplificadas (usadas internamente)
        self.relation_key = {
            "dist. contrata dev.": "devcontratodist",
            "dev. desenvolve jogo": "devdesenvolvejg",
            "dist. distribui jogo": "distdistribuijg",
            "usr. amigo de usr.": "usreamigodeusr",
            "usr.joga. jogo": "usrjogajg"
        }
        
        # Dicionário que define os campos de filtro para cada relação (tabela)
        # Cada entrada contém:
        #   - text_filters: Campos que aceitam filtros de texto (strings)
        #   - num_filters: Campos que aceitam filtros numéricos/datas
        self.col_labl_pairs = {
            "usuario": {
                "text_filters": [
                    {"Column": "idusuario", "Label": "ID: "},
                    {"Column": "nomedeperfil", "Label": "Nome: "},
                    {"Column": "emaildousuario", "Label": "Email: "},
                    {"Column": "numerodetelefone", "Label": "Telefone: "},
                    {"Column": "idfamilia", "Label": "ID Fam: "}
                ],
                "num_filters": [
                    {"Column": "datadecriacao", "Label": "Data: "},
                    {"Column": "saldonacarteira", "Label": "Saldo: "}
                ]
            },
            "familia": {
                "text_filters": [
                    {"Column": "idfamilia", "Label": "ID: "},
                    {"Column": "nomedafamilia", "Label": "Nome: "}
                ],
                "num_filters": []
            },
            "distribuidor": {
                "text_filters": [
                    {"Column": "idnomedist", "Label": "ID: "},
                    {"Column": "descricaodist", "Label": "Desc: "},
                    {"Column": "emaildodist", "Label": "Email: "},
                    {"Column": "linkparasitedistribuidor", "Label": "Site: "}
                ],
                "num_filters": []
            },
            "desenvolvedor": {
                "text_filters": [
                    {"Column": "idnomedev", "Label": "ID: "},
                    {"Column": "emaildodev", "Label": "Email: "},
                    {"Column": "descricaodev", "Label": "Desc: "},
                    {"Column": "linkparasitedesenvolvedor", "Label": "Site: "}
                ],
                "num_filters": []
            },
            "jogo": {
                "text_filters": [
                    {"Column": "idjogo", "Label": "ID: "},
                    {"Column": "nomejogo", "Label": "Nome: "},
                    {"Column": "descricaojogo", "Label": "Desc: "}
                ],
                "num_filters": [
                    {"Column": "datadelancamento", "Label": "Data: "},
                    {"Column": "preco", "Label": "Preço: "}
                ]
            },
            "genero": {
                "text_filters": [
                    {"Column": "idjogo", "Label": "ID Jogo: "},
                    {"Column": "genero", "Label": "Gênero: "}
                ],
                "num_filters": []
            },
            "transacao": {
                "text_filters": [
                    {"Column": "idtransacao", "Label": "ID: "},
                    {"Column": "idjogo", "Label": "ID Jogo: "},
                    {"Column": "idusuario", "Label": "ID Usr: "}
                ],
                "num_filters": [
                    {"Column": "datadatransacao", "Label": "Data: "},
                    {"Column": "desconto", "Label": "Desconto: "}
                ]
            },
            "avaliacao": {
                "text_filters": [
                    {"Column": "idavaliacao", "Label": "ID: "},
                    {"Column": "idjogo", "Label": "ID Jogo: "},
                    {"Column": "idusuario", "Label": "ID Usr: "},
                    {"Column": "conteudo", "Label": "Conteúdo: "},
                    {"Column": "classeavaliativa", "Label": "Classe: "}
                ],
                "num_filters": []
            },
            "usreamigodeusr": {
                "text_filters": [
                    {"Column": "idusuario1", "Label": "ID Usuário 1: "},
                    {"Column": "idusuario2", "Label": "ID Usuário 2: "}
                ],
                "num_filters": [
                    {"Column": "datadecriacao", "Label": "Data: "}
                ]
            },
            "usrjogajg": {
                "text_filters": [
                    {"Column": "idusuario", "Label": "ID Usuário: "},
                    {"Column": "idjogo", "Label": "ID Jogo: "}
                ],
                "num_filters": [
                    {"Column": "horasjogadas", "Label": "Horas: "},
                    {"Column": "dataultimasessao", "Label": "Últ Sessão: "}
                ]
            },
            "devcontratodist": {
                "text_filters": [
                    {"Column": "idnomedev", "Label": "ID Dev: "},
                    {"Column": "idnomedist", "Label": "ID Dist: "}
                ],
                "num_filters": []
            },
            "devdesenvolvejg": {
                "text_filters": [
                    {"Column": "idnomedev", "Label": "ID Dev: "},
                    {"Column": "idjogo", "Label": "ID Jogo: "}
                ],
                "num_filters": []
            },
            "distdistribuijg": {
                "text_filters": [
                    {"Column": "idnomedist", "Label": "ID Dist: "},
                    {"Column": "idjogo", "Label": "ID Jogo: "}
                ],
                "num_filters": []
            }
        }

    def place_home_bttn(self):
        """
        Cria e posiciona um botão "Menu" na janela atual.
        Quando clicado, retorna ao menu principal.
        """
        bttn_font = tkFont.Font(family="Aptos", size=18)
        bttn = tk.Button(
            master=self.master, 
            text="Menu", 
            bg="White",
            fg="black",
            font=bttn_font,
            padx=10,
            command=self.nav_home
        )
        bttn.place(x=1250, y=700)
    
    def nav_home(self):
        """
        Navega de volta para o menu principal.
        Fecha a janela atual e recria o menu principal.
        """
        self.master.destroy()  # Fecha a janela atual
        self.MenuConstructor()  # Recria o menu principal