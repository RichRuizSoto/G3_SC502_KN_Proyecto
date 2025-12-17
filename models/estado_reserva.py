from config.database import db

class EstadoReserva(db.Model):
    __tablename__ = "estado_reserva"

    id_estado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False, unique=True)