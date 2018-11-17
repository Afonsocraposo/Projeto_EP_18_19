class CAP:

    def __init__(self):
        self.eventos = []
        self.tamanho = 0

    def adicionar(self, evento):
        pos = 0
        for i in range(self.tamanho):
            if evento.tempo > self.pos(i).tempo:
                pos = i+1
        self.eventos.insert(pos, evento)
        self.tamanho += 1

    def pos(self, pos):
        return self.eventos[pos]

    def proximo(self):
        if self.tamanho > 0:
            return self.eventos[0]
        return -1

    def pop(self):
        if self.tamanho > 0:
            self.eventos = self.eventos[1:]
            self.tamanho -=1

    def eliminarID(self, ID):
        nova_lista = []
        for evento in self.eventos:
            if evento.ID != ID:
                nova_lista += [evento]
            else:
                self.tamanho -= 1
        self.eventos = nova_lista

    def mostrar(self):
        for evento in self.eventos:
            evento.mostrar()

if __name__ == '__main__':

    from Evento import *

    c = CAP()

    c.adicionar(Evento(0,"2",1))
    c.adicionar(Evento(0,"3",2))
    c.adicionar(Evento(0,"4",3))
    c.adicionar(Evento(0,"5",4))

    c.mostrar()

    print("---")

    c.eliminarID(0)

    c.mostrar()