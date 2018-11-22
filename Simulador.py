from Individuo import *
from Grelha import *
from Evento import *
from CAP import *
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import pygame


class Simulador:

    def __init__(self, N, Ps, Pi, Th, Td, Tr, Tm, pd, pr, pm, TaS, TaE, TaI, obs):
        self.Th = Th
        self.Td = Td
        self.Tr = Tr
        self.Tm = Tm
        self.pd = pd
        self.pr = pr
        self.pm = pm
        self.TaS = TaS
        self.TaE = TaE
        self.TaI = TaI

        self.grelha = Grelha(N)
        self.obstaculos = obs
        self.grelha.obstaculos(obs)
        self.grelha.popula(Ps, Pi)
        self.IDs = [i for i in range(Ps+Pi)]
        self.contador = Ps + Pi

        self.CAP = CAP()
        self.tempo = 0

        self.tempos = [0]
        self.infetados = [Pi]

        random.seed(0)

        for ind in self.IDs:
            self.CAP.adicionar(Evento(ind, "des", self.randomExp(Td)))
            self.CAP.adicionar(Evento(ind, "rep", self.randomExp(Tr)))
            self.CAP.adicionar(Evento(ind, "mor", self.randomExp(Tm)))

            if ind < Ps:
                self.CAP.adicionar(Evento(ind, "ava", self.randomExp(self.tempoAva("S"))))
            else:
                self.CAP.adicionar(Evento(ind, "ava", self.randomExp(self.tempoAva("I"))))

    def randomExp(self, valorEsperado):
        return np.random.exponential(valorEsperado)

    def tempoAva(self, estado):
        if estado == "S":
            return self.TaS
        elif estado == "E":
            return self.TaE
        elif estado == "I":
            return self.TaI

    def probE(self, pos):
        if self.grelha.pos(pos).estado == "S":
            if self.grelha.infAdjQ(pos):
                n = self.grelha.n1n2(pos)
                n1 = n[0]
                n2 = n[1]
                x = 2*n1 + n2
                pe = (1 / (2 * np.log(1.8))) - (1 / (2 * np.log((x * (x-1)/5) + 1.8)))
                return pe
        return 0

    def probQ(self, p):
        return random.random() <= p

    def deslocamento(self, ID):
        pos = self.grelha.procura(ID)
        ind = self.grelha.pos(pos)
        livres = self.grelha.adjLivre(pos)
        if len(livres) > 0:
            if self.grelha.n1n2(pos)[0] >= 3:
                new_pos = livres.pop(random.randrange(len(livres)))
                self.grelha.remover(pos)
                self.grelha.adicionar(ind, new_pos)
            else:
                if self.probQ(self.pd):
                    new_pos = livres.pop(random.randrange(len(livres)))
                    self.grelha.remover(pos)
                    self.grelha.adicionar(ind, new_pos)

        self.CAP.adicionar(Evento(ID, "des", self.tempo + self.randomExp(self.Td)))

    def reproducao(self, ID):
        pos = self.grelha.procura(ID)
        livres = self.grelha.adjLivre(pos)
        ocupados = self.grelha.adjOcupado(pos)

        ocupadoInd = False
        for p in ocupados:
            if self.grelha.individuoQ(pos):
                ocupadoInd = True
                break

        if len(livres) >= 2 and ocupadoInd:
            if self.probQ(self.Tr):
                new_pos = livres.pop(random.randrange(len(livres)))
                new_ID = self.contador
                self.grelha.adicionar(Individuo(new_ID, "S"), new_pos)
                self.IDs += [new_ID]

                self.CAP.adicionar(Evento(new_ID, "des", self.tempo + self.randomExp(self.Td)))
                self.CAP.adicionar(Evento(new_ID, "rep", self.tempo + self.randomExp(self.Tr)))
                self.CAP.adicionar(Evento(new_ID, "mor", self.tempo + self.randomExp(self.Tm)))
                self.CAP.adicionar(Evento(new_ID, "ava", self.tempo + self.randomExp(self.tempoAva("S"))))

                self.contador += 1

        self.CAP.adicionar(Evento(ID, "rep", self.tempo + self.randomExp(self.Tr)))

    def morte(self, ID):
        pos = self.grelha.procura(ID)
        ind = self.grelha.pos(pos)

        if ind.estado == "I":
            if self.probQ(self.pm + 0.1):
                self.grelha.remover(pos)
                self.IDs.remove(ID)
                self.CAP.eliminarID(ID)
            else:
                self.CAP.adicionar(Evento(ID, "mor", self.tempo + self.randomExp(self.Tm)))
        else:
            if self.probQ(self.pm):
                self.grelha.remover(pos)
                self.IDs.remove(ID)
                self.CAP.eliminarID(ID)
            else:
                self.CAP.adicionar(Evento(ID, "mor", self.tempo + self.randomExp(self.Tm)))

    def avaliacao(self, ID):
        pos = self.grelha.procura(ID)
        ind = self.grelha.pos(pos)

        if ind.estado == "S":
            pe = self.probE(pos)
            if self.probQ(pe):
                ind.estado = "E"
        elif ind.estado == "E":
            ind.estado = "I"
        elif ind.estado == "I":
            ind.estado = "R"

        if ind.estado != "R":
            Ta = self.tempoAva(ind.estado)
            self.CAP.adicionar(Evento(ID, "ava", self.tempo + self.randomExp(Ta)))

        return ind.estado

    def run(self):

        file = open("resultados.txt", "w")
        file.write(str(self.grelha.N)+"\n")
        file.write(str(self.obstaculos)+"\n")

        percentagem = 0
        print(percentagem, "%")

        while self.tempo <= self.Th and self.CAP.tamanho > 0:
            evento = self.CAP.proximo()
            self.CAP.pop()
            self.tempo = evento.tempo

            if round(100*self.tempo/self.Th) > percentagem:
                percentagem = round(100*self.tempo/self.Th)
                print(percentagem, "%")

            ID = evento.ID

            if evento.tipo == "des":
                self.deslocamento(ID)
            elif evento.tipo == "rep":
                self.reproducao(ID)
            elif evento.tipo == "mor":
                self.morte(ID)
            elif evento.tipo == "ava":
                self.avaliacao(ID)

            self.tempos += [self.tempo]
            self.infetados += [self.grelha.infetadosTot()]

            file.write(str(self.grelha.coordSEIR())+"\n")

        file.close()
        return [self.tempos, self.infetados, True]

    def runGraphic(self):
        file = open("resultados.txt", "w")
        file.write(str(self.grelha.N) + "\n")
        file.write(str(self.obstaculos) + "\n")

        pygame.init()
        size = self.grelha.width * 30
        screen = pygame.display.set_mode((size, size))

        time = pygame.time

        running = True

        myfont = pygame.font.SysFont('Arial', 12)
        ended = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            if self.tempo <= self.Th and self.CAP.tamanho > 0:
                evento = self.CAP.proximo()
                self.CAP.pop()
                self.tempo = evento.tempo

                ID = evento.ID

                if evento.tipo == "des":
                    self.deslocamento(ID)
                elif evento.tipo == "rep":
                    self.reproducao(ID)
                elif evento.tipo == "mor":
                    self.morte(ID)
                elif evento.tipo == "ava":
                    self.avaliacao(ID)

                self.tempos += [self.tempo]
                self.infetados += [self.grelha.infetadosTot()]

                screen.fill((0, 0, 0))

                for i in range(len(self.grelha.grelha)):
                    for j in range(len(self.grelha.grelha[0])):
                        ind = self.grelha.grelha[i][j]
                        if ind is not None:
                            if ind == "!":
                                pygame.draw.rect(screen, pygame.Color("gray"), (j * 30, i * 30, 30, 30), 0)
                            else:
                                if ind.estado == "S":
                                    pygame.draw.rect(screen, pygame.Color("white"), (j * 30, i * 30, 30, 30), 0)
                                elif ind.estado == "E":
                                    pygame.draw.rect(screen, pygame.Color("yellow"), (j * 30, i * 30, 30, 30), 0)
                                elif ind.estado == "I":
                                    pygame.draw.rect(screen, pygame.Color("red"), (j * 30, i * 30, 30, 30), 0)
                                elif ind.estado == "R":
                                    pygame.draw.rect(screen, pygame.Color("green"), (j * 30, i * 30, 30, 30), 0)

                                TextSurf = myfont.render(str(ind.ID), True, (0,0,0))
                                TextRect = TextSurf.get_rect()
                                TextRect.center = ((j * 30 + 15), (i * 30 + 15))
                                screen.blit(TextSurf, TextRect)

                TextSurf = myfont.render(str(round(self.tempo,2))+" s", True, (255, 255, 255))
                TextRect = TextSurf.get_rect()
                TextRect.center = ((size - TextRect[2]/2), TextRect[3]/2)
                pygame.draw.rect(screen, pygame.Color("black"), TextRect, 0)
                screen.blit(TextSurf, TextRect)

                file.write(str(self.grelha.coordSEIR()) + "\n")

            else:
                ended = True
                file.close()

            pygame.display.update()

            time.delay(1)

        return [self.tempos, self.infetados, ended]


if __name__ == '__main__':
    obs = [[2, i] for i in range(-10, 11)]
    sim = Simulador(10, 96, 4, 50, 1, 10, 20, 0.6, 0.3, 0.5, 1, 1, 10, obs)
    plot_data = sim.runGraphic()
    if plot_data[2]:
        plt.plot(plot_data[0], plot_data[1])
        plt.title("Evolução do número de infetados ao longo do tempo")
        plt.xlabel("Tempo [s]")
        plt.ylabel("Número total de infetados")
        plt.savefig("resultado.png")
