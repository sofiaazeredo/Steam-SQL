import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox as msg

class CRUD_update(tk.Tk):
    def __init__(self):
        super().__init__()
        bttn_font = tkFont.Font(family="Aptos",size = 18)
        title_font = tkFont.Font(family="Aptos",size=48,weight=tkFont.BOLD)
        subtitle_font = tkFont.Font(family="Aptos",size=24)
        opt_font = tkFont.Font(family="Aptos",size=14)
        self.tag_font =  tkFont.Font(family="Aptos",size=20)
        self.bg_color = "#1F1F1F"
        fg_colors = {
            "active": "#E0E0E0",  # Light gray (best readability)
            "default": "#4FC3F7",   # Light blue (for selected/hover)
        }

        self.geometry("1400x800")
        self.title("CRUD Menu")
        self.configure(bg=self.bg_color)

        self.filter_vars = []
        self.filter_widgets = []

        self.update_vars = []
        self.update_widgets = []

        relations = ["usuario","avaliacao", "desenvolvedor", "dist. contrata dev.", "dev. desenvolve jogo", "dist. distribui jogo",
                      "distribuidor", "familia", "genero", "jogo", "transacao", "usr. amigo de usr.", "usr.joga. jogo"]
        
        realtion_key = {"dist. contrata dev.":"devcontratodist",
                        "dev. desenvolve jogo":"devdesenvolvejg",
                        "dist. distribui jogo":"distdistribuijg",
                        "usr. amigo de usr.":"usreamigodeusr",
                        "usr.joga. jogo":"usrjogajg"}

        self.relation_opt = tk.StringVar(master=self,value=relations[0])

        self.title_label = tk.Label(master=self, text="Atualizar Registros",fg="white",bg=self.bg_color,font=title_font)
        self.title_label.place(x=405,y=30)

        self.show_button = tk.Button(master=self, text="Aplicar Filtros e Atualizar", bg="White",fg="black",font = bttn_font,padx=255,command=self.gen_update_query)
        self.show_button.place(x=350,y=700)

        self.filter_section_label = tk.Label(master = self, text="Filtros",bg=self.bg_color,fg="white",font=subtitle_font)
        self.filter_section_label.place(x=620,y=140)

        self.update_section_label = tk.Label(master = self, text="Atualizações",bg=self.bg_color,fg="white",font=subtitle_font)
        self.update_section_label.place(x=910,y=140)

        
        for index, each_relation in enumerate(relations):
            value = each_relation
            if(each_relation in realtion_key):
                value = realtion_key[each_relation]
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
                anchor="w",  
                cursor="hand2",
                command=self.on_relation_select
            )
            rb.place(x=50, y=145+40*index)

        self.place_all_filters()

    def get_width_height(self,widget:tk.Widget):
        self.update()
        w = widget.winfo_width()
        h = widget.winfo_height()
        return w,h
    
    def gen_update_query(self):
        relation = self.relation_opt.get()
        query = f"UPDATE {relation} SET "

        filters = []
        updates = []

        for each_var in self.filter_vars:
            field_input = each_var[0].get("1.0",tk.END).strip()
            field_column = each_var[1]
            field_equivalence = each_var[2].get().strip()

            if field_input:
                filters.append(f"{field_column} {field_equivalence} '{field_input}'")

        for each_var in self.update_vars:
            field_input = each_var[0].get("1.0",tk.END).strip()
            field_column = each_var[1]
            
            if field_input:
                updates.append(f"{field_column} = '{field_input}'")

        if(filters and updates):
            query += ", ".join(updates)
            query += " WHERE " + " AND ".join(filters) +";"
            print(query)
        else:
            msg.showerror(title="ERRO!",message="CAMPOS CRUCIAIS VAZIOS!!!!!!!")
            print("fail")
            


    def on_relation_select(self):
        self.place_all_filters()

    def place_all_filters(self):
        self.destroy_temp_widgets()
        rel_opt = self.relation_opt.get()
        filter_config = {
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
        self.place_text_filters(filter_config[rel_opt]["text_filters"])
        self.place_num_filter(filter_config[rel_opt]["num_filters"])
        all_columns = filter_config[rel_opt]["text_filters"] + filter_config[rel_opt]["num_filters"]
        self.place_update_fields(all_columns)

    def place_text_filters(self,text_cols:list):
        index_corection = len(self.filter_vars)
        for index, filter_spec in enumerate(text_cols):
            y_iter = 200 + 70* (index + index_corection)

            filter_input = tk.Text(master=self,padx=40,pady=10,height=0,width=32)
            filter_input.place(x=500,y=y_iter)

            filter_label = tk.Label(master=self,fg="white",bg=self.bg_color,text=filter_spec["Label"],font=self.tag_font)
            filter_label.place(x=350,y=y_iter)

            equivalence_opt = tk.StringVar(master=self,value="=")

            self.filter_vars.append((filter_input,filter_spec["Column"],equivalence_opt))

            self.filter_widgets.append(filter_input)
            self.filter_widgets.append(filter_label)

    def place_num_filter(self,num_cols:list):
        index_corection = len(self.filter_vars)
        for index, filter_spec in enumerate(num_cols):
            y_iter = 200 + 70* (index + index_corection)

            filter_label = tk.Label(master=self,fg="white",bg=self.bg_color,text=filter_spec["Label"],font=self.tag_font)
            filter_label.place(x=350,y=y_iter)

            equivalence_opt = tk.StringVar(master=self,value="=")
            filter_config = tk.OptionMenu(self,equivalence_opt,"<",">","=")
            filter_config.place(x=500,y=y_iter+5)

            filter_input = tk.Text(master=self,padx=0,pady=10,height=0,width=32)
            filter_input.place(x=580,y=y_iter)

            self.filter_vars.append((filter_input,filter_spec["Column"],equivalence_opt))
            self.filter_widgets.append(filter_input)
            self.filter_widgets.append(filter_label)
            self.filter_widgets.append(filter_config)
    
    def place_update_fields(self, cols_list:list):
        for index, column_spec in enumerate(cols_list):
            y_iter = 200 + 70* (index)

            input_field = tk.Text(master=self,padx=10,pady=10,height=0,width=32)
            input_field.place(x=865,y=y_iter)

            self.update_vars.append((input_field,column_spec["Column"]))
            self.update_widgets.append(input_field)

    def destroy_temp_widgets(self):
        for each_widget in self.filter_widgets:
            each_widget.destroy()

        for each_widget in self.update_widgets:
            each_widget.destroy()

        self.filter_vars.clear()
        self.filter_widgets.clear()
        self.update_widgets.clear()
        self.update_vars.clear()

r = CRUD_update()
r.mainloop()