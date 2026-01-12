from datetime import datetime

class Turno:
    def __init__(self, data):
        self.codigo = data["codigo"]
        self.descripcion = data["descripcion"]
        self.inicio = data["hora_inicio"]
        self.fin = data["hora_fin"]
        self.festivo = data["festivo"]

    def hora_inicio_obj(self):
        return datetime.strptime(self.inicio, "%H:%M")

    def hora_fin_obj(self):
        return datetime.strptime(self.fin, "%H:%M")
