from flask import Blueprint, request, jsonify, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.usuario import Usuario
from config.database import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template("login.html")

@auth_bp.route("/api/register", methods=["POST"])
def register_api():
    data = request.get_json()
    nombre = data.get("nombre")
    correo = data.get("correo")
    contrasena = data.get("contrasena")

    existe = Usuario.query.filter_by(correo=correo).first()
    if existe:
        return jsonify({"error": "El correo ya está registrado"}), 400

    nuevo = Usuario(
        nombre=nombre,
        correo=correo,
        contrasena=generate_password_hash(contrasena),
        id_tipo_usuario=1
    )

    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"message": "Registro exitoso"}), 201

@auth_bp.route("/api/login", methods=["POST"])
def login_api():
    data = request.get_json()
    correo = data.get("correo")
    contrasena = data.get("contrasena")

    user = Usuario.query.filter_by(correo=correo).first()
    if not user:
        return jsonify({"error": "Correo no registrado"}), 400

    if not check_password_hash(user.contrasena, contrasena):
        return jsonify({"error": "Contraseña incorrecta"}), 400

    session["user_id"] = user.id_usuario

    return jsonify({"message": "Login exitoso"}), 200
