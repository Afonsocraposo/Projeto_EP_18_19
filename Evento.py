class Evento:

    def __init__(self, ID, tipo, tempo):
        self.ID = ID
        self.tipo = tipo
        self.tempo = tempo

    def mostrar(self):
        print("Ind: ", self.ID, "Tipo: ", self.tipo, 'Tempo: ', self.tempo)