#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 22:17:26 2018

@author: robot
"""

class Individuo:
    
    def __init__(self, ID, estado):
        self.ID = ID
        self.estado = estado

    def suscetivelQ(self):
        return self.estado == "S"

    def expostoQ(self):
        return self.estado == "E"

    def infetadoQ(self):
        return self.estado == "I"

    def recuperadoQ(self):
        return self.estado == "R"

