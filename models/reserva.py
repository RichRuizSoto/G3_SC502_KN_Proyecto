from config.database import db

class Reserva(db.Model):
    __tablename__ = "reserva"

    id_reserva = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)
    id_experiencia = db.Column(db.Integer, db.ForeignKey("experiencia.id_experiencia"), nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey("estado_reserva.id_estado"), nullable=False)

    cantidad_personas = db.Column(db.Integer, nullable=False)
    fecha_reserva = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    comentario = db.Column(db.String(255))