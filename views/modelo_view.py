from flask import Blueprint, request, make_response, jsonify, render_template, redirect, url_for

from app import db
from models import Equipo, Modelo, Categoria, Marca, Stock, Fabricante, Caracteristica, Proveedor, Accesorio, EquipoAccesorio

from schemas import ModeloSchema

modelo_bp = Blueprint('modelo', __name__)
# Rutas para Modelos
@modelo_bp.route('/modelos/<int:marca_id>')
def modelos_por_marca(marca_id):
    # Código para listar modelos por marca
    marca = Marca.query.get_or_404(marca_id)
    modelos = Modelo.query.filter_by(marca_id=marca_id).all()
    return render_template('modelos_por_marca.html', marca=marca, modelos=modelos)

@modelo_bp.route('/modelos')
def listar_modelos():
    modelos = Modelo.query.all()
    return render_template('modelos.html', modelos=modelos)

@modelo_bp.route('/modelo/nuevo', methods=['GET', 'POST'])
def nuevo_modelo():
    # Código para agregar un nuevo modelo
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            fabricante_id = request.form.get('fabricante_id')
            marca_id = request.form.get('marca_id')

            if fabricante_id:
                fabricante_id = int(fabricante_id)
            else:
                fabricante_id = None

            if marca_id:
                marca_id = int(marca_id)
            else:
                marca_id = None

            nuevo_modelo = Modelo(
                nombre=nombre,
                fabricante_id=fabricante_id,
                marca_id=marca_id
            )
            db.session.add(nuevo_modelo)
            db.session.commit()
            return redirect(url_for('listar_modelos'))
        except Exception as e:
            print(f"Error al agregar nuevo modelo: {e}")
            return render_template('nuevo_modelo.html', error="No se pudo agregar el nuevo modelo. Inténtalo de nuevo.")

    fabricantes = Fabricante.query.all()
    marcas = Marca.query.all()
    return render_template('nuevo_modelo.html', fabricantes=fabricantes, marcas=marcas)

@modelo_bp.route('/modelo/editar/<int:id>', methods=['GET', 'POST'])
def editar_modelo(id):
    # Código para editar un modelo existente
    modelo = Modelo.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            modelo.nombre = request.form['nombre']
            db.session.commit()
            return redirect(url_for('listar_modelos'))
        except Exception as e:
            print(f"Error al actualizar el modelo: {e}")
            return render_template('editar_modelo.html', modelo=modelo, error="No se pudo actualizar el modelo. Inténtalo de nuevo.")
    
    return render_template('editar_modelo.html', modelo=modelo)
