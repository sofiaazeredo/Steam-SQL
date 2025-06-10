import tkinter as tk
from tkinter import font as tkFont
from delete import CRUD_delete
from read import CRUD_read
from create import CRUD_create
from update import CRUD_update

class CRUD_Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x800")  # Define o tamanho da janela principal
        self.title("CRUD Menu")    # Define o título da janela
        self.configure(bg="#1F1F1F")  # Define a cor de fundo da janela
        
        # Configuração de fontes
        bttn_font = tkFont.Font(family="Aptos", size=24)  
        title_font = tkFont.Font(family="Aptos", size=48, weight=tkFont.BOLD)  
        subtitle_font = tkFont.Font(family="Aptos", size=10)  

        # Elementos da interface
        self.title_label = tk.Label(master=self, text="STEAM", fg="white", bg="#1F1F1F", font=title_font)
        self.title_label.place(x=585, y=70)

        self.subtitle_label = tk.Label(master=self, 
                                     text="SISTEMA DE GERENCIAMENTO DE BANCO DE DADOS",
                                     fg="white", bg="#1F1F1F", font=subtitle_font)
        self.subtitle_label.place(x=527, y=150)

        # Botões de navegação
        # Botão para acessar a função de criação (Create)
        self.navto_create_btt = tk.Button(master=self, 
                                        text="Inserir um novo registro",
                                        padx=220, pady=10, font=bttn_font,
                                        command=self.nav_create)
        self.navto_create_btt.place(x=300, y=195)

        # Botão para acessar a função de leitura (Read)
        self.navto_read_btt = tk.Button(master=self, 
                                      text="Ler Registros Atuais",
                                      padx=244, pady=10, font=bttn_font,
                                      command=self.nav_read)
        self.navto_read_btt.place(x=300, y=315)

        # Botão para acessar a função de atualização (Update)
        self.navto_update_btt = tk.Button(master=self, 
                                        text="Atualizar Registros",
                                        padx=255, pady=10, font=bttn_font,
                                        command=self.nav_update)
        self.navto_update_btt.place(x=300, y=435)

        # Botão para acessar a função de exclusão (Delete)
        self.navto_delete_btt = tk.Button(master=self, 
                                       text="Deletar Registros",
                                       padx=265, pady=10, font=bttn_font,
                                       command=self.nav_delete)
        self.navto_delete_btt.place(x=300, y=555)

    def nav_create(self):
        """Fecha a janela atual e abre a janela de criação (Create)."""
        self.destroy()
        CRUD_create(CRUD_Menu)  # Instancia a nova janela CRUD_create

    def nav_read(self):
        """Fecha a janela atual e abre a janela de leitura (Read)."""
        self.destroy()
        CRUD_read(CRUD_Menu)  # Instancia a nova janela CRUD_read

    def nav_update(self):
        """Fecha a janela atual e abre a janela de atualização (Update)."""
        self.destroy()
        CRUD_update(CRUD_Menu)  # Instancia a nova janela CRUD_update

    def nav_delete(self):
        """Fecha a janela atual e abre a janela de exclusão (Delete)."""
        self.destroy()
        CRUD_delete(CRUD_Menu)  # Instancia a nova janela CRUD_delete

def main():
    """Função principal que inicia a aplicação."""
    menu = CRUD_Menu()  # Cria a instância do menu principal
    menu.mainloop()     # Inicia o loop principal da interface gráfica

if __name__ == "__main__":
    main()