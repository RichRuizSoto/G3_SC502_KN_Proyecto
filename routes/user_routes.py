from flask import Blueprint
from controllers.user_controller import register_user

user_bp = Blueprint("user_bp", __name__)

user_bp = Blueprint("user_bp", __name__, url_prefix="/api")

user_bp.post("/register")(register_user)
