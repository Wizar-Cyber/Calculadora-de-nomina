class GestorEventos:
    def __init__(self):
        self.eventos = []

    def agregar(self, evento):
        self.eventos.append(evento)

    def eliminar(self, index):
        self.eventos.pop(index)
