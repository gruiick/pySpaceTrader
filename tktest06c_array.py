#!/usr/bin/env python3
# coding:utf-8

# $Id: tktest06c_array.py 1094 $
# SPDX-License-Identifier: BSD-2-Clause

# origin: https://stackoverflow.com/questions/11047803/creating-a-table-look-a-like-tkinter/11049650#11049650

import tkinter as tk


class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = SimpleTable(self, 13, 3)
        t.pack(side='top', fill='x')
        t.set(0, 0, 'Hello, world')
        t.set(12, 2, 'coin')
        print(t.size)
        print(t.rows)

        # tout effacer
        # t.clear()


class SimpleTable(tk.Frame):
    """ """
    def __init__(self, parent, rows=10, columns=2):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background='black')
        self._widgets = []
        self.rows = rows
        self.columns = columns
        # print(self.rows)
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                label = tk.Label(self, text='%s,%s' % (row, column), 
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky='news', padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)

    # retourne current (rows, columns) as attributs
    # SimpleTable.rows = self.rows already exist !!
    @property
    def size(self):
        """ return current size """
        return (self.rows, self.columns)

    def clear(self):
        """ empty all cells on demand """
        for i in range(self.rows):
            for j in range(self.columns):
                self.set(i, j, '')

    def set(self, row, column, value):
        """ set value inside the cell """
        widget = self._widgets[row][column]
        widget.configure(text=value)

if __name__ == '__main__':
    app = ExampleApp()
    app.mainloop()
