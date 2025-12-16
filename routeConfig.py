from flask import render_template
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.experiencias_routes import experiencias_bp
from routes.contacto_routes import contacto_bp
from flask import session, redirect, url_for
from models.usuario import Usuario
from models.experiencia import Experiencia
from models.reserva import Reserva
from models.estado_reserva import EstadoReserva
from models.contacto_experiencia import ContactoExperiencia
from flask import request
from flask import session
from config.database import db

def register_routes(app):
    print("[✔] Registrando rutas...")

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(experiencias_bp)
    app.register_blueprint(contacto_bp)

    @app.route('/header.html')
    def header_partial():
        return render_template('header.html')

    @app.route('/footer.html')
    def footer_partial():
        return render_template('footer.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/inicial')
    def index():
        experiencias = Experiencia.query.order_by(Experiencia.fecha_creacion.desc()).limit(12).all()
        return render_template('home.html', experiencias=experiencias)

    @app.route('/')
    def home():
        return render_template('login.html')

    @app.route('/dashboard')
    def dashboard():
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.home"))
        
        mis_experiencias = (
            Experiencia.query
            .filter_by(id_usuario=user_id)
            .order_by(Experiencia.fecha_creacion.desc())
            .all()
        )
        
        total_experiencias = len(mis_experiencias)
        
        estado_pendiente = EstadoReserva.query.filter_by(nombre="PENDIENTE").first()
        reservas_pendientes = 0
        
        if estado_pendiente:
            reservas_pendientes = (
                db.session.query(Reserva)
                .join(Experiencia, Reserva.id_experiencia == Experiencia.id_experiencia)
                .filter(Experiencia.id_usuario == user_id)
                .filter(Reserva.id_estado == estado_pendiente.id_estado)
                .count()
            )

        # Comunidad activa (cantidad de usuarios)
        comunidad_activa = Usuario.query.count()

        lista_reservas_pendientes = []

        if estado_pendiente:
            lista_reservas_pendientes = (
                db.session.query(Reserva, Experiencia, Usuario)
                .join(Experiencia, Reserva.id_experiencia == Experiencia.id_experiencia)
                .join(Usuario, Reserva.id_usuario == Usuario.id_usuario)
                .filter(Experiencia.id_usuario == user_id)  # mis experiencias
                .filter(Reserva.id_estado == estado_pendiente.id_estado)
                .order_by(Reserva.fecha_reserva.desc())
                .all()
            )
        
        return render_template('dashboard.html',
            experiencias=mis_experiencias,
            total_experiencias=total_experiencias,
            reservas_pendientes=reservas_pendientes,
            comunidad_activa=comunidad_activa,
            lista_reservas_pendientes=lista_reservas_pendientes
        )
    
    @app.post("/reservas/<int:id_reserva>/confirmar")
    def confirmar_reserva(id_reserva):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.home"))

        reserva = Reserva.query.get_or_404(id_reserva)

        exp = Experiencia.query.get_or_404(reserva.id_experiencia)
        if exp.id_usuario != user_id:
            return "No autorizado", 403

        estado_confirmada = EstadoReserva.query.filter_by(nombre="CONFIRMADA").first()
        if not estado_confirmada:
            return "Error: estado CONFIRMADA no existe", 500

        reserva.id_estado = estado_confirmada.id_estado
        db.session.commit()

        return redirect(url_for("dashboard"))


    @app.post("/reservas/<int:id_reserva>/cancelar")
    def cancelar_reserva(id_reserva):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.home"))

        reserva = Reserva.query.get_or_404(id_reserva)

        exp = Experiencia.query.get_or_404(reserva.id_experiencia)
        if exp.id_usuario != user_id:
            return "No autorizado", 403

        estado_cancelada = EstadoReserva.query.filter_by(nombre="CANCELADA").first()
        if not estado_cancelada:
            return "Error: estado CANCELADA no existe", 500

        reserva.id_estado = estado_cancelada.id_estado
        db.session.commit()

        return redirect(url_for("dashboard"))
    
    @app.route("/dashboard/mis-experiencias")
    def dashboard_mis_experiencias():
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.home"))
        
        mis_experiencias = (
            Experiencia.query
            .filter_by(id_usuario=user_id)
            .order_by(Experiencia.fecha_creacion.desc())
            .all()
    )
        return render_template("dashboard_mis_experiencias.html", experiencias=mis_experiencias)
    
    @app.route("/dashboard/mis-reservas")
    def dashboard_mis_reservas():
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.home"))

        mis_reservas = (
            db.session.query(Reserva, Experiencia, EstadoReserva)
            .join(Experiencia, Reserva.id_experiencia == Experiencia.id_experiencia)
            .join(EstadoReserva, Reserva.id_estado == EstadoReserva.id_estado)
            .filter(Reserva.id_usuario == user_id)
            .order_by(Reserva.fecha_reserva.desc())
            .all()
    )

        return render_template("dashboard_mis_reservas.html", mis_reservas=mis_reservas)

    @app.route('/contacto')
    def contacto():
        return render_template('contacto.html')
    
    @app.route('/experiencias')
    def experiencias():
        q = request.args.get("q", "").strip()

        query = Experiencia.query.order_by(Experiencia.fecha_creacion.desc())

        if q:
            like = f"%{q}%"
            query = query.filter(
                (Experiencia.titulo.like(like)) |
                (Experiencia.descripcion.like(like)) |
                (Experiencia.ubicacion.like(like))
            )

        experiencias = query.all()
        return render_template('experiencias.html', experiencias=experiencias)

    @app.route("/experiencias/<int:id_experiencia>")
    def experiencia_detalle(id_experiencia):
        e = Experiencia.query.get_or_404(id_experiencia)
        contacto = ContactoExperiencia.query.filter_by(id_experiencia=id_experiencia).first()
        
        # Procesar redes sociales si existen
        redes_sociales = None
        if contacto and contacto.redes_sociales:
            import json
            try:
                redes_sociales = json.loads(contacto.redes_sociales)
            except:
                redes_sociales = None
        
        return render_template("experiencia_detalle.html", e=e, contacto=contacto, redes_sociales=redes_sociales)
    
    @app.route("/experiencias/<int:id_experiencia>/contacto/editar")
    def editar_contacto(id_experiencia):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.home"))
        
        experiencia = Experiencia.query.get_or_404(id_experiencia)
        
        if experiencia.id_usuario != user_id:
            return "No autorizado", 403
        
        contacto = ContactoExperiencia.query.filter_by(id_experiencia=id_experiencia).first()
        
        # Procesar redes sociales si existen
        redes_sociales = None
        if contacto and contacto.redes_sociales:
            try:
                redes_sociales = json.loads(contacto.redes_sociales)
            except:
                redes_sociales = None
        
        return render_template("editar_contacto.html", experiencia=experiencia, contacto=contacto, redes_sociales=redes_sociales)
    
    @app.post("/experiencias/<int:id_experiencia>/eliminar")
    def eliminar_experiencia(id_experiencia):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.home"))
        
        e = Experiencia.query.get_or_404(id_experiencia)
        
        if e.id_usuario != user_id:
            return "No autorizado", 403
        
        db.session.delete(e)
        db.session.commit()
        
        return redirect(url_for("dashboard_mis_experiencias"))
    
    @app.route("/experiencias/<int:id_experiencia>/editar")
    def editar_experiencia_form(id_experiencia):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.home"))

        e = Experiencia.query.get_or_404(id_experiencia)

        if e.id_usuario != user_id:
            return "No autorizado", 403

        return render_template("editar.html", e=e)
    
    @app.post("/experiencias/<int:id_experiencia>/editar")
    def editar_experiencia_guardar(id_experiencia):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.home"))

        e = Experiencia.query.get_or_404(id_experiencia)

        if e.id_usuario != user_id:
            return "No autorizado", 403

    # Tomar datos del form
        e.titulo = request.form.get("titulo")
        e.ubicacion = request.form.get("ubicacion")
        e.descripcion = request.form.get("descripcion")
        e.duracion_horas = request.form.get("duracion")
        e.capacidad_maxima = request.form.get("capacidad")
        e.precio_por_persona = request.form.get("precio")

        fecha_evento = request.form.get("fecha_evento")
        if fecha_evento:
            from datetime import datetime
            e.fecha_evento = datetime.fromisoformat(fecha_evento)

        db.session.commit()

        return redirect(url_for("dashboard_mis_experiencias"))
    
    @app.post("/reservar/<int:id_experiencia>")
    def reservar_experiencia(id_experiencia):
        user_id = session.get("user_id")
        
        if not user_id:
            return redirect(url_for("auth.home"))
        
        estado_pendiente = EstadoReserva.query.filter_by(nombre="PENDIENTE").first()
        
        if not estado_pendiente:
            return "Error: estado PENDIENTE no existe", 500
        
        nueva_reserva = Reserva(
            id_usuario=user_id,
            id_experiencia=id_experiencia,
            id_estado=estado_pendiente.id_estado,
            cantidad_personas=1
            )
        
        db.session.add(nueva_reserva)
        db.session.commit()
        return redirect(url_for("dashboard"))


    @app.route('/publicar')
    def publicar():
        return render_template('publicar.html')

    print("[✔] Rutas registradas exitosamente")

    @app.route('/perfil')
    def perfil():
        user_id = session.get("user_id")

        if not user_id:
            return redirect(url_for("auth.home"))

        usuario = Usuario.query.get(user_id)

        return render_template("perfil.html", usuario=usuario)

    @app.post("/perfil/editar-telefono")
    def editar_telefono():
        user_id = session.get("user_id")

        if not user_id:
            return redirect(url_for("auth.home"))

        usuario = Usuario.query.get(user_id)
        nuevo_telefono = request.form.get("telefono")

        if nuevo_telefono:
            usuario.telefono = nuevo_telefono
            db.session.commit()

        return redirect(url_for("perfil"))
