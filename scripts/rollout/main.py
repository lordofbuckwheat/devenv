import tkinter as tk

root = tk.Tk()
label = tk.Label(root, text='Hello World')
label.pack()


def click():
    print('clicked')
    label.setvar('text', 'clicked')


button = tk.Button(root, text='click me', command=click)
button.pack()
root.mainloop()
