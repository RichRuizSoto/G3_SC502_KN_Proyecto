from flask import request, jsonify
from config.database import db
from models.usuario import Usuario

def obtener_usuario_por_id(id_usuario):
    return Usuario.query.filter_by(id_usuario=id_usuario).first()

def register_user():
    data = request.json

    nuevo_usuario = Usuario(
        nombre=data["nombre"],
        correo=data["correo"],
        contrasena=data["contrasena"],
        id_tipo_usuario=data.get("id_tipo_usuario", 1),
        telefono=data.get("telefono", None)
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
