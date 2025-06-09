import tkinter as tk
from tkinter import font as tkFont


class CRUD_Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x800")
        self.title("CRUD Menu")
        self.configure(bg="#1F1F1F")
        bttn_font = tkFont.Font(family="Aptos",size = 24)
        title_font = tkFont.Font(family="Aptos",size=48,weight=tkFont.BOLD)
        subtitle_font = tkFont.Font(family="Aptos",size=10)


        self.title_label = tk.Label(text="STEAM",fg="white",bg="#1F1F1F",font=title_font)
        self.title_label.place(x=585,y=70)

        self.subtitle_label = tk.Label(text="SISTEMA DE GERENCIAMENTO DE BANCO DE DADOS",fg="white",bg="#1F1F1F",font=subtitle_font)
        self.subtitle_label.place(x=527,y=150)

        self.navto_create_btt = tk.Button(text="Inserir um novo registro",padx=220,pady=10,font=bttn_font)
        self.navto_create_btt.place(x=300,y=195)

        self.navto_read_btt = tk.Button(text="Ler Registros Atuais",padx=244,pady=10,font=bttn_font)
        self.navto_read_btt.place(x=300,y=315)

        self.navto_update_btt = tk.Button(text="Atualizar Registros",padx=255,pady=10,font=bttn_font)
        self.navto_update_btt.place(x=300,y=435)

        self.navto_delete_btt =tk.Button(text="Deletar Registros",padx=265,pady=10,font=bttn_font)
        self.navto_delete_btt.place(x=300,y=555)

        print(self.get_width_height(self.title_label))
    def get_width_height(self,widget:tk.Widget):
        self.update()
        w = widget.winfo_width()
        h = widget.winfo_height()
        return w,h


def main():
    menu = CRUD_Menu()
    menu.mainloop()

if __name__ == "__main__":
    main()