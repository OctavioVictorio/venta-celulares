from flask import Blueprint, request, make_response, jsonify, render_template, redirect, url_for

from app import db
from models import Caracteristica, Equipo 
from schemas import CaracteristicaSchema
from flask_jwt_extended import(
    jwt_required,               #para saber si el usuario esta autenticado
    get_jwt,                    #para saber si el usuario es admin
)
caracteristica_bp = Blueprint('caracteristica', __name__)

# Rutas para Características
@caracteristica_bp.route('/caracteristicas', methods=['GET'])
def listar_caracteristicas():
    # Código para listar características
    caracteristicas = Caracteristica.query.all()
    equipos = Equipo.query.all()  # Obtener todos los equipos para la selección

    return render_template('caracteristicas.html', caracteristicas=caracteristicas, equipos=equipos)


@caracteristica_bp.route('/caracteristicas/nuevo', methods=['GET', 'POST'])
@jwt_required()
def agregar_caracteristica():
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if administrador is False:
        return jsonify(Mensaje="Debes ser admin para poder agregar nueva característica")
    # Código para agregar una característica
    if request.method == 'POST':
        try:
            tipo = request.form.get('tipo')
            descripcion = request.form.get('descripcion')
            equipo_id = request.form.get('equipo_id')

            nuevo_equipo = Caracteristica(tipo=tipo, descripcion=descripcion, equipo_id=equipo_id)
            db.session.add(nuevo_equipo)
            db.session.commit()

            return redirect(url_for('listar_caracteristicas'))
        except Exception as e:
            print(f"Error al agregar nueva característica: {e}")
            return render_template('agregar_caracteristicas.html', error="No se pudo agregar la característica. Inténtalo de nuevo.")
    equipos = Equipo.query.all()
    return render_template('agregar_caracteristicas.html', equipos=equipos)

@caracteristica_bp.route('/caracteristicas/<int:id>/editar', methods=['GET', 'POST'])
@jwt_required()
def editar_caracteristica(id):
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if administrador is False:
        return jsonify(Mensaje="Debes ser admin para poder editar una característica")
    # Código para editar una característica
    caracteristica = Caracteristica.query.get_or_404(id)

    if request.method == 'POST':
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']

        caracteristica.tipo = tipo
        caracteristica.descripcion = descripcion
        db.session.commit()

        return redirect(url_for('listar_caracteristicas'))

    return render_template('editar_caracteristicas.html', caracteristica=caracteristica)
