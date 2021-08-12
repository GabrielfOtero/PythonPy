import random
from tkinter import *
root = Tk()

class Application():
    def __init__(self):
        self.root = root
        self.janela()
        self.dados()
        root.mainloop()
    def janela(self):
        self.root.title("Gerador de senhas")
        self.root.configure(background= 'sky blue')
        self.root.geometry("600x600")
        self.root.resizable(True, True)
    def dados(self):
        ## Criação da label e entrada do site
        self.lb_site = Label(text="Site/Software", bg='#dfe3ee', fg='#107db2')
        self.lb_site.place(relx=0.15, rely=0.05)

        self.site_entry = Entry()
        self.site_entry.place(relx=0.35, rely=0.05, relwidth=0.5)
        ## Criação da label e entrada do site
        self.lb_site = Label(text="Site/Software", bg='#dfe3ee', fg='#107db2')
        self.lb_site.place(relx=0.15, rely=0.05)
        self.site_entry = Entry()
        self.site_entry.place(relx=0.35, rely=0.05, relwidth=0.5)
        ## Criação da label e entrada do usuário
        self.lb_email = Label(text="Email/Usuário", bg='#dfe3ee', fg='#107db2')
        self.lb_email.place(relx=0.15, rely=0.15)
        self.email_entry = Entry()
        self.email_entry.place(relx=0.36, rely=0.15, relwidth=0.5)
        ## Criação da label e entrada do Quantidade de caracteres
        self.quantcare = IntVar()
        self.lb_quantcare1 = Label(text="Quantidade de caracteres", bg='#dfe3ee', fg='#107db2')
        self.lb_quantcare1.place(relx=0.15, rely=0.25)
        self.quantcare1_entry = Entry(textvariable=self.quantcare)
        self.quantcare1_entry.place(relx=0.52, rely=0.25, relwidth=0.1)
        # Resultado
        self.resultadogeral = StringVar()
        self.lb_resultado1 = Label(text="Senha gerada ",
                            bg='#dfe3ee', fg='#107db2')
        self.lb_resultado1.place(relx=0.15, rely=0.35)
        self.resultado1 = Label(textvariable=self.resultadogeral)
        self.resultado1.place(relx=0.36, rely=0.35, relwidth=0.4)



        ### Criação do botao Gerar senha
        self.bt_geralsenha1 = Button(text="Gerar senha", bd=2, bg='#107db2', fg='white'
                                , font=('verdana', 8, 'bold'), command=self.gerarsenha)
        self.bt_geralsenha1.place(relx=0.3, rely=0.45, relwidth=0.3, relheight=0.1)
    def gerarsenha(self):
        num_caract = self.quantcare.get()
        char_list = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%¨&*'
        passwd = ""
        while len(passwd) != num_caract:
            passwd = passwd + random.choice(char_list)
        return self.resultadogeral.set(passwd)

Application()