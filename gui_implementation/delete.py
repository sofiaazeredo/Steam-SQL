import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox as msg
from crud_utils import CRUD_utils

class CRUD_delete(tk.Tk):
    def __init__(self):
        super().__init__()
        self.utils = CRUD_utils()

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

        self.filter_vars = []
        self.filter_widgets = []

        self.relation_opt = tk.StringVar(master=self,value=self.utils.relations[0])

        self.title_label = tk.Label(master=self, text="Deletar Registros",fg="white",bg=self.bg_color,font=title_font)
        self.title_label.place(x=431,y=50)

        self.show_button = tk.Button(master=self, text="Aplicar Filtros e Deletar", bg="White",fg="black",font = bttn_font,padx=255,command=self.delete_query)
        self.show_button.place(x=350,y=700)
        
        for index, each_relation in enumerate(self.utils.relations):
            value = each_relation
            if(each_relation in self.utils.relation_key):
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
            rb.place(x=50, y=145+40*index)

        self.place_relation_filters()

        print(self.get_width_height(self.title_label))

    def get_width_height(self,widget:tk.Widget):
        self.update()
        w = widget.winfo_width()
        h = widget.winfo_height()
        return w,h
    
    def delete_query(self):
        relation = self.relation_opt.get()
        query = f"DELETE FROM {relation} WHERE "

        filters = []
        for filter_var in self.filter_vars:
            
            field_value = filter_var[0].get("1.0", tk.END).strip()
            column = filter_var[1]
            equivalence = filter_var[2].get()

            if field_value:
                filters.append(f"{column} {equivalence} '{field_value}'")      

        if filters:
            query += " AND ".join(filters)
            query += ";"
            print(query)
        else:
            msg.showerror(title="ERRO!",message="NENHUM FILTRO INSERIDO!!!!!!!")
            print("fail")
            


    def on_relation_select(self):
        self.place_relation_filters()

    def place_relation_filters(self):
        self.destroy_temp_widgets()
        rel_opt = self.relation_opt.get()
        
        self.place_text_filters(self.utils.col_labl_pairs[rel_opt]["text_filters"])
        self.place_num_filter(self.utils.col_labl_pairs[rel_opt]["num_filters"])

    def place_text_filters(self,text_filters:list):
        index_corection = len(self.filter_vars)
        for index, text_filter in enumerate(text_filters):
            y_iter = 150 + 80* (index + index_corection)

            filter_input = tk.Text(master=self,padx=80,pady=10,height=0,width=60)
            filter_input.place(x=500,y=y_iter)

            filter_label = tk.Label(master=self,fg="white",bg=self.bg_color,text=text_filter["Label"],font=self.tag_font)
            filter_label.place(x=350,y=y_iter)

            equivalence_opt = tk.StringVar(master=self,value="=")

            self.filter_vars.append((filter_input,text_filter["Column"],equivalence_opt))

            self.filter_widgets.append(filter_input)
            self.filter_widgets.append(filter_label)

    def place_num_filter(self,num_filters:list):
        index_corection = len(self.filter_vars)
        for index, num_filter in enumerate(num_filters):
            y_iter = 150 + 80* (index + index_corection)

            filter_label = tk.Label(master=self,fg="white",bg=self.bg_color,text=num_filter["Label"],font=self.tag_font)
            filter_label.place(x=350,y=y_iter)

            equivalence_opt = tk.StringVar(master=self,value="=")
            filter_config = tk.OptionMenu(self,equivalence_opt,"<",">","=")
            filter_config.place(x=500,y=y_iter+5)

            filter_input = tk.Text(master=self,padx=40,pady=10,height=0,width=60)
            filter_input.place(x=580,y=y_iter)

            self.filter_vars.append((filter_input,num_filter["Column"],equivalence_opt))
            self.filter_widgets.append(filter_input)
            self.filter_widgets.append(filter_label)
            self.filter_widgets.append(filter_config)

    def destroy_temp_widgets(self):
        for each_widget in self.filter_widgets:
            each_widget.destroy()
        self.filter_vars.clear()
        self.filter_widgets.clear()