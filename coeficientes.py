import math

class Coeficientes:
    def __init__(self, overshoot, tempAcomodacao):
        self.overshoot = overshoot
        self.tempAcomodacao = tempAcomodacao
        
    def calc_KpKi(self):
        x = (math.log(self.overshoot) / math.pi) ** 2
        e = math.sqrt(-x / (-x - 1))

        w = 4 / (e * self.tempAcomodacao)

        mf = math.degrees(math.asin(e)) * 2

        wcg = w

        # PLANTA
        mod_gj = math.sqrt(0.02011 ** 2) / math.sqrt(wcg ** 2 + 0.02402 ** 2)
        #mod_gj = math.sqrt(80  2) / math.sqrt((wcg * 16)  2 + 1  2)

        fase_gj = math.degrees(math.atan(0/0.02011)) - math.degrees(math.atan(wcg/0.02402))
        #fase_gj = math.degrees(math.atan(0/80)) - math.degrees(math.atan((wcg * 16)/1))

        # CONTROLADOR
        mod_c = 1/mod_gj

        fase_c = -180 + mf - fase_gj

        x = 1/(wcg ** 2)
        t = math.tan(math.radians(fase_c))
        y = t * -wcg

        kp = math.sqrt((mod_c ** 2) / (1 + x * (y ** 2)))

        ki = y * kp

        return "Kp: {} \nKi: {}".format(kp, ki)