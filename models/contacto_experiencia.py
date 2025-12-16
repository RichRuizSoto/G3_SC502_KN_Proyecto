from config.database import db

class ContactoExperiencia(db.Model):
    __tablename__ = "contacto_experiencia"

    id_contacto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_experiencia = db.Column(db.Integer, db.ForeignKey("experiencia.id_experiencia"), nullable=False)
    nombre_contacto = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(255))
    horario_atencion = db.Column(db.String(100))
    sitio_web = db.Column(db.String(255))
    redes_sociales = db.Column(db.Text)  # JSON string con redes sociales
    fecha_creacion = db.Column(db.DateTime, server_default=db.func.now())
    fecha_actualizacion = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relación con Experiencia
    experiencia = db.relationship("Experiencia", backref=db.backref("contacto", uselist=False, lazy=True))
