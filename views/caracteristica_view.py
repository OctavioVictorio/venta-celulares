from flask import Blueprint, request, make_response, jsonify, render_template, redirect, url_for

from app import db
from models import Equipo, Modelo, Categoria, Marca, Stock, Fabricante, Caracteristica, Proveedor, Accesorio, EquipoAccesorio

from schemas import CaracteristicaSchema

caracteristica_bp = Blueprint('caracteristica', __name__)

# Rutas para Características
@caracteristica_bp.route('/caracteristicas', methods=['GET'])
def listar_caracteristicas():
    # Código para listar características
    caracteristicas = Caracteristica.query.all()
    equipos = Equipo.query.all()  # Obtener todos los equipos para la selección

    return render_template('caracteristicas.html', caracteristicas=caracteristicas, equipos=equipos)


@caracteristica_bp.route('/caracteristicas/nuevo', methods=['GET', 'POST'])
def agregar_caracteristica():
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
def editar_caracteristica(id):
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
