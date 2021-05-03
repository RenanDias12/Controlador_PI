import tkinter as tk
import sys
from controlador import Controlador
from coeficientes import Coeficientes

window = tk.Tk()
window.configure(background='#FFFFFF')

def coeficientes():
    coef = Coeficientes(0.2, 50)
    saida.insert('end',"Por resposta em frequência:\n")
    saida.insert('end', coef.calc_KpKi())

def controle():
    resp = Controlador()
    saida.delete(1.0,'end')
    saida.insert('end',"Função de tranferência:\n")
    saida.insert('end', resp.controlePI())

lbl1 = tk.Label(window, text='Controlador Proporcional Integral', fg='#4169E1', font=("Segoe UI", 20), background = '#FFFFFF')
lbl1.place(x=20, y=2)

btn2 = tk.Button(window,text='   Plot   ', fg='#000000', bg='#FFFFFF', font=("Segoe UI", 12), bd=1, background = '#FFFFFF', command=controle)
btn2.place(x=500, y=150)

btn2 = tk.Button(window,text=' Kp e Ki', fg='#000000', bg='#FFFFFF', font=("Segoe UI", 12), bd=1, background = '#FFFFFF', command=coeficientes)
btn2.place(x=500, y=200)

saida = tk.Text(window, height=10, width= 40,bg= '#FFFFFF', fg='#4169E1', bd=0,font=("Segoe UI",14))
saida.place(x=40, y=80)

window.title('Controlador PI')
window.geometry("600x400")
window.mainloop()