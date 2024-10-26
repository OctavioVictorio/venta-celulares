from flask import Blueprint, request, make_response, jsonify, render_template, redirect, url_for

from app import db
from models import Marca, Modelo, Categoria, Marca, Stock

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
def editar_marca(id):
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
def nuevo_marca():
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
