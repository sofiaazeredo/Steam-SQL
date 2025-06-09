import tkinter as tk
from tkinter import font as tkFont
from delete import CRUD_delete
from read import CRUD_read

class CRUD_Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x800")
        self.title("CRUD Menu")
        self.configure(bg="#1F1F1F")
        self.current_window = None
        
        # Font setup
        bttn_font = tkFont.Font(family="Aptos", size=24)
        title_font = tkFont.Font(family="Aptos", size=48, weight=tkFont.BOLD)
        subtitle_font = tkFont.Font(family="Aptos", size=10)

        # UI Elements
        self.title_label = tk.Label(master=self, text="STEAM", fg="white", bg="#1F1F1F", font=title_font)
        self.title_label.place(x=585, y=70)

        self.subtitle_label = tk.Label(master=self, 
                                     text="SISTEMA DE GERENCIAMENTO DE BANCO DE DADOS",
                                     fg="white", bg="#1F1F1F", font=subtitle_font)
        self.subtitle_label.place(x=527, y=150)

        # Navigation Buttons
        self.navto_create_btt = tk.Button(master=self, 
                                        text="Inserir um novo registro",
                                        padx=220, pady=10, font=bttn_font,
                                        command=self.nav_create)
        self.navto_create_btt.place(x=300, y=195)

        self.navto_read_btt = tk.Button(master=self, 
                                      text="Ler Registros Atuais",
                                      padx=244, pady=10, font=bttn_font,
                                      command=self.nav_read)
        self.navto_read_btt.place(x=300, y=315)

        self.navto_update_btt = tk.Button(master=self, 
                                        text="Atualizar Registros",
                                        padx=255, pady=10, font=bttn_font,
                                        command=self.nav_update)
        self.navto_update_btt.place(x=300, y=435)

        self.navto_delete_btt = tk.Button(master=self, 
                                       text="Deletar Registros",
                                       padx=265, pady=10, font=bttn_font,
                                       command=self.nav_delete)
        self.navto_delete_btt.place(x=300, y=555)

    def close_current_window(self):
        if self.current_window:
            self.current_window.destroy()
            self.current_window = None

    def nav_create(self):
        self.close_current_window()
        print("create")


    def nav_read(self):
        self.close_current_window()
        self.current_window = CRUD_read(self) 
        print("read")

    def nav_update(self):
        self.close_current_window()
        print("up")
        

    def nav_delete(self):
        self.close_current_window()
        self.current_window = CRUD_delete(self)
        print("del")

def main():
    menu = CRUD_Menu()
    menu.mainloop()

if __name__ == "__main__":
    main()