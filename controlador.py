import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
from scipy import signal
from coeficientes import Coeficientes
import threading
import tkinter as tk
import sys


class Controlador():
        
    def controlePI(self):
        
        mat = scipy.io.loadmat('_data/amostras_equipe4.mat')
        #Degrau
        deg = mat['degrau0_4']
        #Resposta
        resp = mat['resp0_4']
        #Tempo
        tmp = mat['tempo0_4']
        tmp = tmp.flatten()

        #------ Minimos quadrados -------
        F = np.concatenate((resp.T, deg.T), axis=1)
        F = np.delete(F, -1, 0)
        J = resp[:,1:]
        J = J.T

        coef = (np.linalg.inv(F.T @ F)) @ F.T @ J
        a1 = coef[0,0]
        b1 = coef[1,0]

        resp = resp.flatten()
        deg = deg.flatten()

        den = [1, -a1]

        sysZ = ctrl.tf(b1, den, 0.4)
        a1 = np.array(sysZ.den[0])
        a1 = a1[0,1]*-1
        b1 = np.array(sysZ.num[0])
        b1 = b1[0,0]

        [x, y] = ctrl.step_response(sysZ, tmp)
        resp_ident = (y * deg[0]).tolist()

        figure1 = plt.figure()
        plt.plot(tmp, resp, color='tab:blue')
        plt.plot(tmp, resp_ident, color='tab:red')
        plt.grid()
        plt.title('Resposta identificada x Resposta real')
        figure1.show()

        #------Resposta em malha aberta ----------
        malha_aberta = [0]

        for i in range(1, len(resp_ident)):
            malha_aberta.append(a1 * malha_aberta[i-1] + b1 * deg[i-1])


        #-------- Resposta em malha fechada ----------
        malha_fechada = [0]
        erro = [0]

        for i in range(1, len(resp_ident)):
            malha_fechada.append(a1 * malha_fechada[i-1] + b1 * erro[i-1])
            erro.append(deg[i] - malha_fechada[i])

        #--------- Malha fechada com Kp -------------
        #Acomodação: 50  Overshoot: 20%

        malha_fechada_kp = [0]
        erro = [0]
        Kp = 9
        

        for i in range(1, len(resp_ident)):
            malha_fechada_kp.append(a1 * malha_fechada_kp[i-1] + b1 * erro[i-1])
            erro.append((deg[i] - malha_fechada_kp[i]) * Kp)

        #--------- Malha fechada com Kp e Ki-------------
        #Acomodação: 50  Overshoot: 20%

        malha_fechadakp_ki = [0]
        erro = [0]
        I = [0]
        P = [0]
        K = [0]
        T = 0.4
        Ki = 1.3

        for i in range(1, len(resp_ident)):
            malha_fechadakp_ki.append(a1 * malha_fechadakp_ki[i-1] + b1 * K[i-1])
            erro.append(deg[i] - malha_fechadakp_ki[i])
            P.append(Kp * erro[i])
            I.append(I[i-1] + Ki * erro[i] * T)
            K.append(P[i] + I[i])

        figure2 = plt.figure()
        plt.plot(tmp, malha_aberta, color='tab:red', label='Malha Aberta')
        plt.plot(tmp, malha_fechada, color='tab:blue', label='Malha Fechada')
        plt.plot(tmp, malha_fechada_kp, color='tab:orange', label='Malha Fechada com Kp')
        plt.plot(tmp, malha_fechadakp_ki, color='tab:purple', label='Malha Fechada com Kp e Ki')
        plt.grid()
        plt.legend()
        plt.title('Comparativo')
        figure2.show()

        return sysZ
