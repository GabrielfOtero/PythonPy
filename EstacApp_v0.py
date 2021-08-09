from tkinter import *
from functools import partial



root = Tk()
root.title('EstacApp v0')
root.geometry("1200x500")
root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 1)

my_canvas = Canvas(root, width=1200, height=200, bg="white")
my_canvas.grid(row = 2, column = 0, columnspan = 2)

txt1 = Text(height = 1, font = "Arial 9")
txt1.grid(column = 1, row = 0)

def Desenhar():
    diam = int(txt1.get("1.0",'end-1c'))
    my_canvas.delete("all")
    my_canvas.create_oval(50,50,diam,diam)

def Limpa():
    my_canvas.delete("all")


#comando_com_arg = partial(Desenhar, txt1.get("1.0",END))

lbl1 = Label(text = "Informe o diâmetro da estaca:", height = 1, font = "Arial")
lbl1.grid(column = 0, row = 0)


btn1 = Button(text = "Gerar desenho", command = Desenhar)
btn1.grid(column = 0, row = 1)

btn2 = Button(text = "Limpar", command = Limpa)
btn2.grid(column = 1, row = 1)




root.mainloop()