import tkinter as tk
from tkinter import font as tkFont

class CRUD_create(tk.Tk):
    def __init__(self,):
        super().__init__()
        bttn_font = tkFont.Font(family="Aptos",size = 18)
        title_font = tkFont.Font(family="Aptos",size=48,weight=tkFont.BOLD)
        subtitle_font = tkFont.Font(family="Aptos",size=14)
        self.tag_font =  tkFont.Font(family="Aptos",size=20)
        self.bg_color = "#1F1F1F"
        fg_colors = {
            "active": "#E0E0E0",  # Light gray (best readability)
            "default": "#4FC3F7",   # Light blue (for selected/hover)
        }

        self.geometry("1400x800")
        self.title("CRUD Menu")
        self.configure(bg=self.bg_color)

        self.insertion_vars = []
        self.insertion_widgets = []

        relations = ["usuario","avaliacao", "desenvolvedor", "dist. contrata dev.", "dev. desenvolve jogo", "dist. distribui jogo",
                      "distribuidor", "familia", "genero", "jogo", "transacao", "usr. amigo de usr.", "usr.joga. jogo"]
        
        realtion_key = {"dist. contrata dev.":"devcontratodist",
                        "dev. desenvolve jogo":"devdesenvolvejg",
                        "dist. distribui jogo":"distdistribuijg",
                        "usr. amigo de usr.":"usreamigodeusr",
                        "usr.joga. jogo":"usrjogajg"}

        self.relation_opt = tk.StringVar(master=self,value=relations[0])

        self.title_label = tk.Label(master=self, text="O que tem de Novo?",fg="white",bg=self.bg_color,font=title_font)
        self.title_label.place(x=385,y=50)

        self.show_button = tk.Button(master=self, text="Inserir Novo Registro", bg="White",fg="black",font = bttn_font,padx=255,command=self.insert_values)
        self.show_button.place(x=350,y=700)
        
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
            rb.place(x=50, y=125+40*index)

        self.place_insert_fields()
        print(self.get_width_height(self.title_label))

    def get_width_height(self,widget:tk.Widget):
        self.update()
        w = widget.winfo_width()
        h = widget.winfo_height()
        return w,h
    
    def insert_values(self):
        relation = self.relation_opt.get()
        query = f"INSERT INTO {relation}"

        if self.insertion_vars:
            insert_vals = []
            insert_cols = []
            for filter_var in self.insertion_vars:
                
                field_value = filter_var[0].get("1.0", tk.END).strip()
                column = filter_var[1]

                if field_value:
                    insert_vals.append(f"'{field_value}'")    
                    insert_cols.append(column)           
            if insert_vals:
                query += " (" + ", ".join(insert_cols) +")"
                query += " VALUES (" + ", ".join(insert_vals) + ")"
        query += ";"

        print(query)

    def on_relation_select(self):
        self.place_insert_fields()

    def place_insert_fields(self):
        self.destroy_temp_widgets()
        rel_opt = self.relation_opt.get()
        filter_config = {
            "usuario": {
                "text_insert_fields": [
                    {"Column": "idusuario", "Label": "ID: "},
                    {"Column": "nomedeperfil", "Label": "Nome: "},
                    {"Column": "emaildousuario", "Label": "Email: "},
                    {"Column": "numerodetelefone", "Label": "Telefone: "},
                    {"Column": "idfamilia", "Label": "ID Fam: "},
                    {"Column": "datadecriacao", "Label": "Data: "},
                    {"Column": "saldonacarteira", "Label": "Saldo: "}
                ]
            },
            "familia": {
                "text_insert_fields": [
                    {"Column": "idfamilia", "Label": "ID: "},
                    {"Column": "nomedafamilia", "Label": "Nome: "}]
            },
            "distribuidor": {
                "text_insert_fields": [
                    {"Column": "idnomedist", "Label": "ID: "},
                    {"Column": "descricaodist", "Label": "Desc: "},
                    {"Column": "emaildodist", "Label": "Email: "},
                    {"Column": "linkparasitedistribuidor", "Label": "Site: "}]
            },
            "desenvolvedor": {
                "text_insert_fields": [
                    {"Column": "idnomedev", "Label": "ID: "},
                    {"Column": "emaildodev", "Label": "Email: "},
                    {"Column": "descricaodev", "Label": "Desc: "},
                    {"Column": "linkparasitedesenvolvedor", "Label": "Site: "}]
            },
            "jogo": {
                "text_insert_fields": [
                    {"Column": "idjogo", "Label": "ID: "},
                    {"Column": "nomejogo", "Label": "Nome: "},
                    {"Column": "descricaojogo", "Label": "Desc: "},
                    {"Column": "datadelancamento", "Label": "Data: "},
                    {"Column": "preco", "Label": "Preço: "}
                ]
            },
            "genero": {
                "text_insert_fields": [
                    {"Column": "idjogo", "Label": "ID Jogo: "},
                    {"Column": "genero", "Label": "Gênero: "}]
            },
            "transacao": {
                "text_insert_fields": [
                    {"Column": "idtransacao", "Label": "ID: "},
                    {"Column": "idjogo", "Label": "ID Jogo: "},
                    {"Column": "idusuario", "Label": "ID Usr: "},
                    {"Column": "datadatransacao", "Label": "Data: "},
                    {"Column": "desconto", "Label": "Desconto: "}
                ]
            },
            "avaliacao": {
                "text_insert_fields": [
                    {"Column": "idavaliacao", "Label": "ID: "},
                    {"Column": "idjogo", "Label": "ID Jogo: "},
                    {"Column": "idusuario", "Label": "ID Usr: "},
                    {"Column": "conteudo", "Label": "Conteúdo: "},
                    {"Column": "classeavaliativa", "Label": "Classe: "}]
            },
            "usreamigodeusr": {
                "text_insert_fields": [
                    {"Column": "idusuario1", "Label": "ID Usuário 1: "},
                    {"Column": "idusuario2", "Label": "ID Usuário 2: "},
                    {"Column": "datadecriacao", "Label": "Data: "}
                ]
            },
            "usrjogajg": {
                "text_insert_fields": [
                    {"Column": "idusuario", "Label": "ID Usuário: "},
                    {"Column": "idjogo", "Label": "ID Jogo: "},
                    {"Column": "horasjogadas", "Label": "Horas: "},
                    {"Column": "dataultimasessao", "Label": "Últ Sessão: "}
                ]
            },
            "devcontratodist": {
                "text_insert_fields": [
                    {"Column": "idnomedev", "Label": "ID Dev: "},
                    {"Column": "idnomedist", "Label": "ID Dist: "}]
            },
            "devdesenvolvejg": {
                "text_insert_fields": [
                    {"Column": "idnomedev", "Label": "ID Dev: "},
                    {"Column": "idjogo", "Label": "ID Jogo: "}]
            },
            "distdistribuijg": {
                "text_insert_fields": [
                    {"Column": "idnomedist", "Label": "ID Dist: "},
                    {"Column": "idjogo", "Label": "ID Jogo: "}]
            }
        }
        self.place_inputs(filter_config[rel_opt]["text_insert_fields"])

    def place_inputs(self,text_insert_fields:list):
        index_corection = len(self.insertion_vars)
        for index, insert_val in enumerate(text_insert_fields):
            y_iter = 150 + 80* (index + index_corection)

            field_input = tk.Text(master=self,padx=80,pady=10,height=0,width=60)
            field_input.place(x=500,y=y_iter)

            field_label = tk.Label(master=self,fg="white",bg=self.bg_color,text=insert_val["Label"],font=self.tag_font)
            field_label.place(x=350,y=y_iter)

            self.insertion_vars.append((field_input,insert_val["Column"]))

            self.insertion_widgets.append(field_input)
            self.insertion_widgets.append(field_label)

    def destroy_temp_widgets(self):
        for each_widget in self.insertion_widgets:
            each_widget.destroy()
        self.insertion_vars.clear()
        self.insertion_widgets.clear()
