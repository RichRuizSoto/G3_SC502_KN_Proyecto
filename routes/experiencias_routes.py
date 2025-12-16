from flask import Blueprint, request, redirect, url_for, session, jsonify
from datetime import datetime
from werkzeug.utils import secure_filename
import os

from config.database import db
from models.experiencia import Experiencia

experiencias_bp = Blueprint("experiencias_bp", __name__, url_prefix="/api")

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_upload_path():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    return UPLOAD_FOLDER

@experiencias_bp.route("/experiencias", methods=["POST"])
def crear_experiencia():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    titulo = (request.form.get("titulo") or "").strip()
    ubicacion = (request.form.get("ubicacion") or "").strip()
    descripcion = (request.form.get("descripcion") or "").strip()
    duracion = (request.form.get("duracion") or "").strip()
    capacidad = (request.form.get("capacidad") or "").strip()
    precio = (request.form.get("precio") or "").strip()
    fecha_evento = (request.form.get("fecha_evento") or "").strip()

    if not all([titulo, ubicacion, descripcion, duracion, capacidad, precio, fecha_evento]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        fecha_evento_dt = datetime.fromisoformat(fecha_evento)
        duracion_num = float(duracion)
        capacidad_num = int(capacidad)
        precio_num = float(precio)
    except ValueError:
        return jsonify({"error": "Invalid data format"}), 400

    imagen_filename = None
    if 'imagen' in request.files:
        file = request.files['imagen']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(f"{user_id}_{datetime.now().timestamp()}_{file.filename}")
            upload_path = get_upload_path()
            file.save(os.path.join(upload_path, filename))
            imagen_filename = filename

    nueva = Experiencia(
        titulo=titulo,
        ubicacion=ubicacion,
        descripcion=descripcion,
        duracion_horas=duracion_num,
        capacidad_maxima=capacidad_num,
        precio_por_persona=precio_num,
        fecha_evento=fecha_evento_dt,
        id_usuario=user_id,
        imagen=imagen_filename
    )

    db.session.add(nueva)
    db.session.commit()

    return jsonify({"message": "Experience created successfully", "id": nueva.id_experiencia}), 201

@experiencias_bp.route("/experiencias/<int:id_experiencia>", methods=["GET"])
def obtener_experiencia(id_experiencia):
    experiencia = Experiencia.query.get(id_experiencia)
    if not experiencia:
        return jsonify({"error": "Experience not found"}), 404
    
    return jsonify({
        "id_experiencia": experiencia.id_experiencia,
        "titulo": experiencia.titulo,
        "ubicacion": experiencia.ubicacion,
        "descripcion": experiencia.descripcion,
        "duracion_horas": float(experiencia.duracion_horas),
        "capacidad_maxima": experiencia.capacidad_maxima,
        "precio_por_persona": float(experiencia.precio_por_persona),
        "fecha_evento": experiencia.fecha_evento.isoformat(),
        "imagen": experiencia.imagen
    }), 200

@experiencias_bp.route("/experiencias/<int:id_experiencia>", methods=["PUT"])
def actualizar_experiencia(id_experiencia):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    experiencia = Experiencia.query.get(id_experiencia)
    if not experiencia:
        return jsonify({"error": "Experience not found"}), 404
    
    if experiencia.id_usuario != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    experiencia.titulo = (request.form.get("titulo") or experiencia.titulo).strip()
    experiencia.ubicacion = (request.form.get("ubicacion") or experiencia.ubicacion).strip()
    experiencia.descripcion = (request.form.get("descripcion") or experiencia.descripcion).strip()
    
    try:
        if request.form.get("duracion"):
            experiencia.duracion_horas = float(request.form.get("duracion"))
        if request.form.get("capacidad"):
            experiencia.capacidad_maxima = int(request.form.get("capacidad"))
        if request.form.get("precio"):
            experiencia.precio_por_persona = float(request.form.get("precio"))
        if request.form.get("fecha_evento"):
            experiencia.fecha_evento = datetime.fromisoformat(request.form.get("fecha_evento"))
    except ValueError:
        return jsonify({"error": "Invalid data format"}), 400

    if 'imagen' in request.files:
        file = request.files['imagen']
        if file and file.filename and allowed_file(file.filename):
            if experiencia.imagen:
                old_path = os.path.join(get_upload_path(), experiencia.imagen)
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            filename = secure_filename(f"{user_id}_{datetime.now().timestamp()}_{file.filename}")
            upload_path = get_upload_path()
            file.save(os.path.join(upload_path, filename))
            experiencia.imagen = filename

    db.session.commit()
    return jsonify({"message": "Experience updated successfully"}), 200

@experiencias_bp.route("/experiencias/<int:id_experiencia>", methods=["DELETE"])
def eliminar_experiencia(id_experiencia):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    experiencia = Experiencia.query.get(id_experiencia)
    if not experiencia:
        return jsonify({"error": "Experience not found"}), 404
    
    if experiencia.id_usuario != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    if experiencia.imagen:
        imagen_path = os.path.join(get_upload_path(), experiencia.imagen)
        if os.path.exists(imagen_path):
            os.remove(imagen_path)

    db.session.delete(experiencia)
    db.session.commit()
    return jsonify({"message": "Experience deleted successfully"}), 200