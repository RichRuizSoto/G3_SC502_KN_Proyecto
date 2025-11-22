from flask import Blueprint, render_template, session, redirect, url_for
from controllers.user_controller import register_user, obtener_usuario_por_id

user_bp = Blueprint("user_bp", __name__, url_prefix="/api")

user_bp.post("/register")(register_user)

@user_bp.route("/perfil")
def perfil():
    if "user_id" not in session:
        return redirect(url_for("auth.home"))

    usuario = obtener_usuario_por_id(session["user_id"])

    datos = {
        "id_usuario": usuario.id_usuario,
        "nombre": usuario.nombre,
        "correo": usuario.correo,
        "telefono": usuario.telefono,
        "fecha_creacion": usuario.fecha_creacion,
        "tipo": "Comunidad Local"
    }

    return render_template("perfil.html", usuario=datos)
