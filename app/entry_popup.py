# %% Imports
import tkinter as tk
from tkinter import ttk

# %% Code

class EntryPopup(ttk.Entry):
    def __init__(self, parent, table, iid, column, text, **kw):
        super().__init__(parent, **kw)
        self.table = table  # Referencia a la tabla (top_table o bottom_table)
        self.iid = iid      # ID de la fila
        self.column = column  # Índice de la columna

        self.insert(0, text)
        self['exportselection'] = False
        self.focus_force()
        self.select_all()
        self.binds()
        
    def binds(self):
        self.bind("<Return>", self.on_return)  # Acción al presionar Enter
        self.bind("<Control-a>", self.select_all)  # Selección con Ctrl+A
        self.bind("<Escape>", lambda *ignore: self.destroy())  # Cierra con Escape
        
    def on_return(self, event):
        '''Inserta el texto en la tabla y destruye el widget'''
        vals = list(self.table.item(self.iid, 'values'))  # Obtiene los valores de la fila como lista
        vals[self.column] = self.get()  # Actualiza el valor de la columna específica
        self.table.item(self.iid, values=vals)  # Inserta los nuevos valores en la tabla
        self.destroy()  # Destruye el widget de entrada

    def select_all(self, *ignore):
        '''Selecciona todo el texto en el widget'''
        self.selection_range(0, 'end')
        return 'break'
