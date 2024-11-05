from flask import Blueprint, request, make_response, jsonify, render_template, redirect, url_for

from app import db
from models import Fabricante
from schemas import FabricanteSchema

from flask_jwt_extended import(
    jwt_required,               #para saber si el usuario esta autenticado
    get_jwt,                    #para saber si el usuario es admin
)
fabricante_bp = Blueprint('fabricante', __name__)

# Rutas para Fabricantes
@fabricante_bp.route('/fabricantes')
def listar_fabricantes():
    fabricantes = Fabricante.query.all()
    return render_template('fabricantes.html', fabricantes=fabricantes)

@fabricante_bp.route('/fabricante/nuevo', methods=['GET', 'POST'])
@jwt_required()
def nuevo_fabricante():
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if administrador is False:
        return jsonify(Mensaje="Debes ser admin para poder agregar nuevo fabricante")
    # Código para agregar un nuevo fabricante
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            nuevo_fabricante = Fabricante(nombre=nombre)
            db.session.add(nuevo_fabricante)
            db.session.commit()
            return redirect(url_for('listar_fabricantes'))
        except Exception as e:
            print(f"Error al agregar nuevo fabricante: {e}")
            return render_template('nuevo_fabricante.html', error="No se pudo agregar el nuevo fabricante. Inténtalo de nuevo.")
    
    return render_template('nuevo_fabricante.html')

@fabricante_bp.route('/fabricante/editar/<int:id>', methods=['GET', 'POST'])
@jwt_required()
def editar_fabricante(id):
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if administrador is False:
        return jsonify(Mensaje="Debes ser admin para poder editar un fabricante")
    # Código para editar un fabricante existente
    fabricante = Fabricante.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            fabricante.nombre = request.form['nombre']
            db.session.commit()
            return redirect(url_for('listar_fabricantes'))
        except Exception as e:
            print(f"Error al actualizar el fabricante: {e}")
            return render_template('editar_fabricante.html', fabricante=fabricante, error="No se pudo actualizar el fabricante. Inténtalo de nuevo.")
    
    return render_template('editar_fabricante.html', fabricante=fabricante)

@fabricante_bp.route('/fabricante/eliminar/<int:id>', methods=['POST'])
@jwt_required()
def eliminar_fabricante(id):
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if administrador is False:
        return jsonify(Mensaje="Debes ser admin para poder eliminar un fabricante")
    # Código para eliminar un fabricante
    fabricante = Fabricante.query.get_or_404(id)
    db.session.delete(fabricante)
    db.session.commit()
    return redirect(url_for('listar_fabricantes'))
