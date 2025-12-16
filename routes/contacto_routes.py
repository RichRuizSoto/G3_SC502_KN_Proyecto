from flask import Blueprint, session, jsonify
from controllers.contacto_controller import (
    crear_contacto, obtener_contacto, actualizar_contacto, eliminar_contacto
)

contacto_bp = Blueprint("contacto_bp", __name__, url_prefix="/api")

@contacto_bp.route("/experiencias/<int:id_experiencia>/contacto", methods=["POST"])
def crear_contacto_route(id_experiencia):
    """Crear información de contacto para una experiencia"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "No autorizado"}), 401

    return crear_contacto(id_experiencia, user_id)


@contacto_bp.route("/experiencias/<int:id_experiencia>/contacto", methods=["GET"])
def obtener_contacto_route(id_experiencia):
    """Obtener información de contacto de una experiencia"""
    return obtener_contacto(id_experiencia)


@contacto_bp.route("/experiencias/<int:id_experiencia>/contacto", methods=["PUT"])
def actualizar_contacto_route(id_experiencia):
    """Actualizar información de contacto de una experiencia"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "No autorizado"}), 401

    return actualizar_contacto(id_experiencia, user_id)


@contacto_bp.route("/experiencias/<int:id_experiencia>/contacto", methods=["DELETE"])
def eliminar_contacto_route(id_experiencia):
    """Eliminar información de contacto de una experiencia"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "No autorizado"}), 401

    return eliminar_contacto(id_experiencia, user_id)
