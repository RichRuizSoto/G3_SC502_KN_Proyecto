from flask import Blueprint, request, redirect, url_for, session
from datetime import datetime

from config.database import db
from models.experiencia import Experiencia

experiencias_bp = Blueprint("experiencias_bp", __name__, url_prefix="/api")

@experiencias_bp.route("/experiencias", methods=["POST"])
def crear_experiencia():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    titulo = (request.form.get("titulo") or "").strip()
    ubicacion = (request.form.get("ubicacion") or "").strip()
    descripcion = (request.form.get("descripcion") or "").strip()
    duracion = (request.form.get("duracion") or "").strip()
    capacidad = (request.form.get("capacidad") or "").strip()
    precio = (request.form.get("precio") or "").strip()
    fecha_evento = (request.form.get("fecha_evento") or "").strip()

    if not all([titulo, ubicacion, descripcion, duracion, capacidad, precio, fecha_evento]):
        return redirect(url_for("publicar"))

    # datetime-local "YYYY-MM-DDTHH:MM"
    try:
        fecha_evento_dt = datetime.fromisoformat(fecha_evento)
        duracion_num = float(duracion)
        capacidad_num = int(capacidad)
        precio_num = float(precio)
    except ValueError:
        return redirect(url_for("publicar"))

    nueva = Experiencia(
        titulo=titulo,
        ubicacion=ubicacion,
        descripcion=descripcion,
        duracion_horas=duracion_num,
        capacidad_maxima=capacidad_num,
        precio_por_persona=precio_num,
        fecha_evento=fecha_evento_dt,
        id_usuario=user_id
    )

    db.session.add(nueva)
    db.session.commit()

    return redirect(url_for("experiencias", created="1"))