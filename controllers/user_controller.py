from flask import request, jsonify
from config.database import db
from models.usuario import Usuario

def register_user():
    data = request.json

    nuevo_usuario = Usuario(
        nombre=data["nombre"],
        correo=data["correo"],
        contrasena=data["contrasena"], 
        id_tipo_usuario=data["id_tipo_usuario"],
        telefono=data["telefono"]
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
