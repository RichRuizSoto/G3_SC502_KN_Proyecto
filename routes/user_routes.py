from flask import Blueprint
from controllers.user_controller import register_user

user_bp = Blueprint("user_bp", __name__)

user_bp.post("/api/usuarios/registrar")(register_user)
