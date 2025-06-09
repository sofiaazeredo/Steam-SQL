import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk


class CRUD_read(tk.Tk):
    def __init__(self):
        super().__init__()
        bttn_font = tkFont.Font(family="Aptos",size = 18)
        title_font = tkFont.Font(family="Aptos",size=48,weight=tkFont.BOLD)
        subtitle_font = tkFont.Font(family="Aptos",size=14)
        bg_color = "#1F1F1F"
        fg_colors = {
            "active": "#E0E0E0",  # Light gray (best readability)
            "default": "#4FC3F7",   # Light blue (for selected/hover)
        }

        self.geometry("1400x800")
        self.title("CRUD Menu")
        self.configure(bg=bg_color)

        relations = ["usuario","avaliacao", "desenvolvedor", "dist. contrata dev.", "dev. desenvolve jogo", "dist. distribui jogo",
                      "distribuidor", "familia", "genero", "jogo", "transacao", "usr. amigo de usr.", "usr.joga. jogo"]
        
        realtion_key = {"dist. contrata dev.":"devcontratodist",
                        "dev. desenvolve jogo":"devdesenvolvejg",
                        "dist. distribui jogo":"distdistribuijg",
                        "usr. amigo de usr.":"usreamigodeusr",
                        "usr.joga. jogo":"usrjogajg"}

        self.relation_opt = tk.StringVar(master=self,value=relations[0])

        self.title_label = tk.Label(master=self, text="O Que Tem nesse BD?",fg="white",bg=bg_color,font=title_font)
        self.title_label.place(x=350,y=50)

        self.show_button = tk.Button(master=self, text="Procurar", bg="White",fg="black",font = bttn_font,padx=100,command=self.show_table)
        self.show_button.place(x=525,y=700)
        
        for index, each_relation in enumerate(relations):
            value = each_relation
            if(each_relation in realtion_key):
                value = realtion_key[each_relation]
            rb = tk.Radiobutton(
                master=self,
                text=each_relation,
                variable=self.relation_opt,
                value=value,
                font=subtitle_font,
                bg=bg_color,
                fg=fg_colors["default"],
                activebackground=bg_color,
                activeforeground=fg_colors["active"],                
                selectcolor=bg_color,
                padx=10,
                pady=5,   
                anchor="w",  
                cursor="hand2",
                command=self.on_relation_select
            )
            rb.place(x=50, y=125+40*index)


        print(self.get_width_height(self.show_button))

    def get_width_height(self,widget:tk.Widget):
        self.update()
        w = widget.winfo_width()
        h = widget.winfo_height()
        return w,h
    
    def show_table(self):
        pass

    def on_relation_select(self):
        print(self.relation_opt.get())

def main():
    menu = CRUD_read()
    menu.mainloop()

if __name__ == "__main__":
    main()