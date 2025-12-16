from flask import request, jsonify
from config.database import db
from models.contacto_experiencia import ContactoExperiencia
from models.experiencia import Experiencia
import json

def validar_permisos_experiencia(id_experiencia, user_id):
    """Valida que la experiencia existe y pertenece al usuario"""
    experiencia = Experiencia.query.filter_by(id_experiencia=id_experiencia).first()
    if not experiencia:
        return None, {"error": "Experiencia no encontrada"}
    
    if experiencia.id_usuario != user_id:
        return None, {"error": "No tienes permiso para modificar esta experiencia"}
    
    return experiencia, None


def obtener_contacto_por_experiencia(id_experiencia):
    """Obtiene el contacto asociado a una experiencia"""
    return ContactoExperiencia.query.filter_by(id_experiencia=id_experiencia).first()


def crear_contacto(id_experiencia, user_id):
    """Crea información de contacto para una experiencia"""
    # Validar permisos
    experiencia, error = validar_permisos_experiencia(id_experiencia, user_id)
    if error:
        return jsonify(error), 403 if "permiso" in error["error"] else 404

    # Verificar si ya existe un contacto
    contacto_existente = obtener_contacto_por_experiencia(id_experiencia)
    if contacto_existente:
        return jsonify({"error": "Ya existe información de contacto para esta experiencia"}), 400

    # Obtener datos del formulario
    nombre_contacto = request.form.get("nombre_contacto", "").strip()
    telefono = request.form.get("telefono", "").strip()
    email = request.form.get("email", "").strip()
    direccion = request.form.get("direccion", "").strip()
    horario_atencion = request.form.get("horario_atencion", "").strip()
    sitio_web = request.form.get("sitio_web", "").strip()
    
    # Procesar redes sociales
    redes_sociales = procesar_redes_sociales(request.form)

    # Validación básica
    if not all([nombre_contacto, telefono, email]):
        return jsonify({"error": "Nombre, teléfono y email son obligatorios"}), 400

    nuevo_contacto = ContactoExperiencia(
        id_experiencia=id_experiencia,
        nombre_contacto=nombre_contacto,
        telefono=telefono,
        email=email,
        direccion=direccion or None,
        horario_atencion=horario_atencion or None,
        sitio_web=sitio_web or None,
        redes_sociales=redes_sociales
    )

    db.session.add(nuevo_contacto)
    db.session.commit()

    return jsonify({
        "mensaje": "Información de contacto creada exitosamente",
        "id_contacto": nuevo_contacto.id_contacto
    }), 201


def obtener_contacto(id_experiencia):
    """Obtiene la información de contacto de una experiencia"""
    contacto = obtener_contacto_por_experiencia(id_experiencia)
    
    if not contacto:
        return jsonify({"error": "No se encontró información de contacto"}), 404

    redes = None
    if contacto.redes_sociales:
        try:
            redes = json.loads(contacto.redes_sociales)
        except:
            redes = None

    return jsonify({
        "id_contacto": contacto.id_contacto,
        "nombre_contacto": contacto.nombre_contacto,
        "telefono": contacto.telefono,
        "email": contacto.email,
        "direccion": contacto.direccion,
        "horario_atencion": contacto.horario_atencion,
        "sitio_web": contacto.sitio_web,
        "redes_sociales": redes
    }), 200


def actualizar_contacto(id_experiencia, user_id):
    """Actualiza la información de contacto de una experiencia"""
    # Validar permisos
    experiencia, error = validar_permisos_experiencia(id_experiencia, user_id)
    if error:
        return jsonify(error), 403 if "permiso" in error["error"] else 404

    contacto = obtener_contacto_por_experiencia(id_experiencia)
    if not contacto:
        return jsonify({"error": "No existe información de contacto para actualizar"}), 404

    # Actualizar campos si vienen en el request
    if request.form.get("nombre_contacto"):
        contacto.nombre_contacto = request.form.get("nombre_contacto").strip()
    if request.form.get("telefono"):
        contacto.telefono = request.form.get("telefono").strip()
    if request.form.get("email"):
        contacto.email = request.form.get("email").strip()
    if request.form.get("direccion") is not None:
        contacto.direccion = request.form.get("direccion").strip() or None
    if request.form.get("horario_atencion") is not None:
        contacto.horario_atencion = request.form.get("horario_atencion").strip() or None
    if request.form.get("sitio_web") is not None:
        contacto.sitio_web = request.form.get("sitio_web").strip() or None
    
    # Actualizar redes sociales
    redes_sociales = procesar_redes_sociales(request.form)
    if redes_sociales is not None:
        contacto.redes_sociales = redes_sociales

    db.session.commit()

    return jsonify({"mensaje": "Información de contacto actualizada exitosamente"}), 200


def eliminar_contacto(id_experiencia, user_id):
    """Elimina la información de contacto de una experiencia"""
    # Validar permisos
    experiencia, error = validar_permisos_experiencia(id_experiencia, user_id)
    if error:
        return jsonify(error), 403 if "permiso" in error["error"] else 404

    contacto = obtener_contacto_por_experiencia(id_experiencia)
    if not contacto:
        return jsonify({"error": "No existe información de contacto para eliminar"}), 404

    db.session.delete(contacto)
    db.session.commit()

    return jsonify({"mensaje": "Información de contacto eliminada exitosamente"}), 200


def procesar_redes_sociales(form_data):
    """Procesa las redes sociales desde el formulario"""
    redes_sociales = form_data.get("redes_sociales")
    
    if redes_sociales:
        return redes_sociales
    
    # Si no viene como JSON, construir desde campos individuales
    redes = {}
    if form_data.get("facebook"):
        redes["facebook"] = form_data.get("facebook")
    if form_data.get("instagram"):
        redes["instagram"] = form_data.get("instagram")
    if form_data.get("whatsapp"):
        redes["whatsapp"] = form_data.get("whatsapp")
    if form_data.get("twitter"):
        redes["twitter"] = form_data.get("twitter")
    if form_data.get("tiktok"):
        redes["tiktok"] = form_data.get("tiktok")
    
    return json.dumps(redes) if redes else None
