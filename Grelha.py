#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 22:21:34 2018

@author: robot
"""
from Individuo import *
import random


class Grelha:

    def __init__(self, N):
        self.grelha = [[None for j in range(2 * N + 1)] for i in range(2 * N + 1)]
        self.N = N
        self.width = 2 * N + 1

    def mostrar(self):
        print("-----")
        for row in self.grelha:
            print("|", end=" ")
            for el in row:
                if el is None:
                    print("N", end=" | ")
                elif el == "!":
                    print("!", end=" | ")
                else:
                    print(el.ID, end=" | ")
            print()
        print("-----")

    def pos(self, pos):
        x = pos[0]
        y = pos[1]
        if x > self.N:
            return self.pos([x - self.width, y])

        elif x < -self.N:
            return self.pos([x + self.width, y])

        elif y > self.N:
            return self.pos([x, y - self.width])

        elif y < -self.N:
            return self.pos([x, y + self.width])

        else:
            return self.grelha[self.N - y][self.N + x]

    def adicionar(self, ind, pos):
        x = pos[0]
        y = pos[1]
        if x > self.N:
            self.adicionar(ind, [x - self.width, y])

        elif x < -self.N:
            self.adicionar(ind, [x + self.width, y])

        elif y > self.N:
            self.adicionar(ind, [x, y - self.width])

        elif y < -self.N:
            self.adicionar(ind, [x, y + self.width])

        else:
            if self.livreQ([x, y]):
                self.grelha[self.N - y][self.N + x] = ind
                return True
            else:
                return False

    def remover(self, pos):
        x = pos[0]
        y = pos[1]
        if x > self.N:
            self.remover([x - self.width, y])

        elif x < -self.N:
            self.remover([x + self.width, y])

        elif y > self.N:
            self.remover([x, y - self.width])

        elif y < -self.N:
            self.remover([x, y + self.width])

        else:
            self.grelha[self.N - y][self.N + x] = None

    def procura(self, ID):
        for x in range(-self.N, self.N + 1):
            for y in range(-self.N, self.N + 1):
                if not self.livreQ([x, y]) and self.individuoQ([x, y]) and self.pos([x, y]).ID == ID:
                    return [x, y]

    def adjOcupado(self, pos):
        x = pos[0]
        y = pos[1]
        res = []
        for a in range(-1, 2):
            for b in range(-1, 2):
                if (a != 0 or b != 0) and not self.livreQ([x + a, y + b]):
                    res += [[x + a, y + b]]
        return res

    def adjLivre(self, pos):
        x = pos[0]
        y = pos[1]
        res = []
        for a in range(-1, 2):
            for b in range(-1, 2):
                if (a != 0 or b != 0) and self.livreQ([x + a, y + b]):
                    res += [[x + a, y + b]]
        return res

    def livreQ(self, pos):
        x = pos[0]
        y = pos[1]
        if x > self.N:
            return self.livreQ([x - self.width, y])

        elif x < -self.N:
            return self.livreQ([x + self.width, y])

        elif y > self.N:
            return self.livreQ([x, y - self.width])

        elif y < -self.N:
            return self.livreQ([x, y + self.width])

        else:
            return self.pos([x, y]) is None

    def individuoQ(self, pos):
        if not self.livreQ(pos):
            if type(self.pos(pos)) is Individuo:
                return True
        return False

    def obstaculoQ(self, pos):
        if not self.livreQ(pos):
            if type(self.pos(pos)) is not Individuo:
                return True
        return False

    def infetadosTot(self):
        res = 0
        for x in range(-self.N, self.N + 1):
            for y in range(-self.N, self.N + 1):
                if self.individuoQ([x, y]):
                    ind = self.pos([x, y])
                    if ind.infetadoQ():
                        res += 1
        return res

    def coordSEIR(self):
        res = [[], [], [], []]
        for x in range(-self.N, self.N + 1):
            for y in range(-self.N, self.N + 1):
                if self.individuoQ([x, y]):
                    ind = self.pos([x, y])
                    if ind.suscetivelQ():
                        res[0] += [[x, y]]
                    elif ind.expostoQ():
                        res[1] += [[x, y]]
                    elif ind.infetadoQ():
                        res[2] += [[x, y]]
                    elif ind.recuperadoQ():
                        res[3] += [[x, y]]
        return res

    def infAdjQ(self, pos):
        x = pos[0]
        y = pos[1]
        infetados = []
        for a in range(-2, 3):
            for b in range(-2, 3):
                p = [x + a, y + b]
                if (a != 0 or b != 0) and not self.livreQ(p) and self.individuoQ(p) and self.pos(p).infetadoQ():
                    if abs(a) <= 1 and abs(b) <= 1:
                        return True
                    else:
                        infetados += [p]

        adjLivre = self.adjLivre(pos)
        for inf in infetados:
            adjInfLivre = self.adjLivre(inf)
            for pos in adjLivre:

                if pos in adjInfLivre:
                    return True

        return False

    def obstaculos(self, posicoes):
        for pos in posicoes:
            self.adicionar("!", pos)

    def popula(self, Ps, Pi):
        c = 0
        livres = []

        for x in range(-self.N, self.N + 1):
            for y in range(-self.N, self.N + 1):
                if self.livreQ([x, y]):
                    livres += [[x, y]]

        for i in range(Ps):
            pos = livres.pop(random.randrange(len(livres)))
            self.adicionar(Individuo(c, "S"), pos)
            c += 1

        for i in range(Pi):
            pos = livres.pop(random.randrange(len(livres)))
            self.adicionar(Individuo(c, "E"), pos)
            c += 1

    def n1n2(self, pos):
        x = pos[0]
        y = pos[1]
        n1 = 0
        n2 = 0
        infetados = []
        for a in range(-2, 3):
            for b in range(-2, 3):
                p = [x + a, y + b]
                if (a != 0 or b != 0) and not self.livreQ(p) and self.individuoQ(p) and self.pos(p).infetadoQ():
                    if abs(a) <= 1 and abs(b) <= 1:
                        n1 += 1
                    else:
                        infetados += [p]

        adjLivre = self.adjLivre(pos)
        for inf in infetados:
            adjInfLivre = self.adjLivre(inf)
            for pos in adjLivre:

                if pos in adjInfLivre:
                    n2 += 1
                    break

        return [n1, n2]


if __name__ == '__main__':
    g = Grelha(3)

    g.obstaculos([[1, 1], [0, 2]])
    g.popula(2, 2)

    g.mostrar()

