import tkinter as tk
import pandas as pd
from pandastable import Table

class PandasApp:
    def __init__(self, df: pd.DataFrame) -> None:
        self.window = tk.Tk()
        self.window.title("Pandas Table Window")

        self.window.geometry("800x600")
        self.window.minsize(600, 400)
        
        self.frame = tk.Frame(self.window)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.table = Table(self.frame, dataframe=df)
        self.table.show()

        self.window.mainloop()
