import json
import time
import tkinter
import differance
from tkinter import scrolledtext, ttk


with open('config.json', 'r', encoding='utf-8-sig') as config:
    cfg = json.loads(config.read())
trained = open('trained_data.json', 'r', encoding='utf8')
try:
    mem = json.loads(trained.read())
except:
    mem = {}


def write():
    message = entry.get()
    if message:
        output.insert(tkinter.END, f'{message}')
        entry.delete(0, tkinter.END)
    else:
        temp[0] = output.get(0.0, tkinter.END)
        last = output.get(1.0, tkinter.END)
        last = last.replace('\n', '').replace('.', ' . ').replace(',', ' , ').replace(';', ' ; ').split(' ')
        for w in last:
            if w == '':
                last.remove('')
        last = last[-3:]
        tx1 = differance.write(mem, last, cfg)
        tx2 = differance.write(mem, last, cfg)
        tx3 = differance.write(mem, last, cfg)
        option1.config(text=tx1 if tx1.startswith(('.', ',', ';')) else ' ' + tx1,
                       command=lambda: [output.insert(tkinter.END, option1['text']), replace()])
        option2.config(text=tx2 if tx2.startswith(('.', ',', ';')) else ' ' + tx2,
                       command=lambda: [output.insert(tkinter.END, option2['text']), replace()])
        option3.config(text=tx3 if tx3.startswith(('.', ',', ';')) else ' ' + tx3,
                       command=lambda: [output.insert(tkinter.END, option3['text']), replace()])


def train(text, data):
    if data:
        try:
            file = open('data.txt', 'r', encoding='utf8')
            text = file.read()
            file.close()
        except:
            file = open('data.txt', 'w')
            file.close()
    if text or data:
        ref = differance.init(text, cfg)
        temp[0] = text
        start = time.time()
        fin = differance.train(ref['ref'], ref['tag'])
        dic = {'lang': fin[0], 'gram': fin[1]}
        with open('trained_data.json', 'w', encoding='utf8') as trained:
            json.dump(dic, trained)
        entry.delete(0, tkinter.END)
        entry.insert(tkinter.END, f'Training took {round(time.time() - start, 3)} seconds.')


def menu():
    submenu = tkinter.Menu(win, tearoff=0)
    submenu.add_command(label='Train', command=lambda: train(output.get(0.0, tkinter.END), False))
    submenu.add_command(label='Data', command=lambda: train(output.get(0.0, tkinter.END), True))
    submenu.add_command(label='Paste', command=lambda: output.insert(tkinter.END, win.clipboard_get()))
    submenu.add_command(label='Copy', command=lambda: win.clipboard_append(output.get(0.0, tkinter.END)))
    submenu.post(menu.winfo_rootx(), menu.winfo_rooty())


def replace():
    option1.config(text='', command='')
    option2.config(text='', command='')
    option3.config(text='', command='')


def add_to(option):
    temp[1] = option


temp = ['', '']
win = tkinter.Tk()
win.title('Differance')
win.iconbitmap("icon.ico")

entry_frame = ttk.Frame(win)
entry_frame.pack(pady=15)
entry = ttk.Entry(entry_frame, width=50)
entry.pack(side='left', fill='x')
entry.bind('<Return>', lambda event: write())

menumg = tkinter.PhotoImage(file='menu.png')
menu = tkinter.Button(entry_frame, image=menumg, command=menu, highlightthickness=0, borderwidth=0)
menu.pack(padx=10, side=tkinter.RIGHT)

sendmg = tkinter.PhotoImage(file='send.png')
send = tkinter.Button(entry_frame, image=sendmg, command=write, highlightthickness=0, borderwidth=0)
send.pack(padx=10, side=tkinter.RIGHT)

output = scrolledtext.ScrolledText(win, wrap='word', width=50, height=20, highlightthickness=0, borderwidth=0)
output.config(maxundo=-1, undo=True, autoseparators=True, font=('Courier', cfg['font']))
output.pack(fill='both', expand=True, side=tkinter.BOTTOM)

linemg = tkinter.PhotoImage(file='line.png')
option1 = tkinter.Button(win, highlightthickness=0, borderwidth=0)
option1.pack(anchor='w', side=tkinter.LEFT, fill='x', expand=True)
tkinter.Label(image=linemg).pack(anchor='w', side=tkinter.LEFT, fill='x', expand=True)
option2 = tkinter.Button(win, highlightthickness=0, borderwidth=0)
option2.pack(anchor='w', side=tkinter.LEFT, fill='x', expand=True)
tkinter.Label(image=linemg).pack(anchor='w', side=tkinter.LEFT, fill='x', expand=True)
option3 = tkinter.Button(win, highlightthickness=0, borderwidth=0)
option3.pack(anchor='w', side=tkinter.LEFT, fill='x', expand=True)

win.mainloop()
