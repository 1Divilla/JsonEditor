# %% Imports
import tkinter as tk
from tkinter import ttk

# %% Code

class EntryPopup(ttk.Entry):
    def __init__(self, parent, table, iid, column, text, **kw):
        super().__init__(parent, **kw)
        self.table = table
        self.iid = iid
        self.column = column

        self.insert(0, text)
        self['exportselection'] = False
        self.focus_force()
        self.select_all()
        self.binds()
        
    def binds(self):
        self.bind("<Return>", self.on_return)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Escape>", lambda *ignore: self.destroy())
        
    def on_return(self, event):
        '''Insert the text into the table and destroy the widget'''
        vals = list(self.table.item(self.iid, 'values'))
        vals[self.column] = self.get()
        self.table.item(self.iid, values=vals)
        self.destroy()

    def select_all(self, *ignore):
        '''Select all text in the widget'''
        self.selection_range(0, 'end')
        return 'break'
