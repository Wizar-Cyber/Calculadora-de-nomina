from datetime import datetime

class Turno:
    """Representa un turno (código) cargado desde turnos.json.

    Espera un dict con:
    - codigo: str
    - descripcion: str
    - hora_inicio / hora_fin: str en formato HH:MM
    - festivo: bool (True si dominical/festivo)
    """

    def __init__(self, data):
        # El modelo solo almacena los valores y provee utilidades para convertir a datetime.
        self.codigo = data["codigo"]
        self.descripcion = data["descripcion"]
        self.inicio = data["hora_inicio"]
        self.fin = data["hora_fin"]
        self.festivo = data["festivo"]

    def hora_inicio_obj(self):
        # Convierte "HH:MM" a datetime (la fecha no se usa; solo interesa la hora).
        return datetime.strptime(self.inicio, "%H:%M")

    def hora_fin_obj(self):
        # Convierte "HH:MM" a datetime (la fecha no se usa; solo interesa la hora).
        return datetime.strptime(self.fin, "%H:%M")
