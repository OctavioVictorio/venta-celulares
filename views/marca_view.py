from flask import Blueprint, request, make_response, jsonify, render_template, redirect, url_for

from app import db
from models import Marca
from flask_jwt_extended import(
    jwt_required,               #para saber si el usuario esta autenticado
    get_jwt,                    #para saber si el usuario es admin
)
from schemas import MarcaSchema

from forms import MarcaForm

from services.marca_service import MarcaService
from repositories.marca_repository import MarcaRepository

from services.marca_service import MarcaService

marca_bp = Blueprint('marca', __name__)

# Rutas para Marcas
@marca_bp.route('/marcas', methods=['GET', 'POST'])
def marcas():
    # Código para gestionar marcas
    formulario = MarcaForm()
    
    services = MarcaService(MarcaRepository())
    marcas = services.get_all()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        services.create(nombre=nombre)
        return redirect(url_for('marcas'))
    
    return render_template(
        'marcas.html',
        marcas=marcas,
        formulario=formulario    
    )

@marca_bp.route('/marca/editar/<int:id>', methods=['GET', 'POST'])
@jwt_required()
def editar_marca(id):
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if administrador is False:
        return jsonify(Mensaje="Debes ser admin para poder editar una marca")
    
    # Código para editar una marca existente
    marca = Marca.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            marca.nombre = request.form['nombre']
            db.session.commit()
            return redirect(url_for('marcas'))
        except Exception as e:
            print(f"Error al actualizar la marca: {e}")
            return render_template('editar_marca.html', marca=marca, error="No se pudo actualizar la marca. Inténtalo de nuevo.")
    
    return render_template('editar_marca.html', marca=marca)


@marca_bp.route('/marca/nuevo', methods=['GET', 'POST'])
@jwt_required()
def nuevo_marca():
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if administrador is False:
        return jsonify(Mensaje="Debes ser admin para poder agregar nuevo marca")
    
    # Código para agregar una nueva marca
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            nueva_marca = Marca(nombre=nombre)
            db.session.add(nueva_marca)
            db.session.commit()
            return redirect(url_for('marcas'))
        except Exception as e:
            print(f"Error al agregar nueva marca: {e}")
            return render_template('nuevo_marca.html', error="No se pudo agregar la nueva marca. Inténtalo de nuevo.")
    
    return render_template('nuevo_marca.html')
