from flask import Blueprint, request, jsonify, render_template, redirect, url_for

from app import db
from models import Categoria, Equipo, Modelo, Marca, Stock

from schemas import EquipoSchema

from flask_jwt_extended import(
    jwt_required,               #para saber si el usuario esta autenticado
    get_jwt,                    #para saber si el usuario es admin
)

equipo_bp = Blueprint('equipo', __name__)

# Rutas para Equipos
@equipo_bp.route('/equipos', methods=['GET'])
def listar_equipos():
    equipos = Equipo.query.all()
    return render_template('listar_equipos.html', equipos=equipos)
@equipo_bp.route('/equipo/nuevo', methods=['GET', 'POST'])
@jwt_required()
def nuevo_equipo():
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if administrador is False:
        return jsonify(Mensaje="Debes ser admin para poder agregar nuevo equipo")
    
    if request.method == 'GET':
        modelos = Modelo.query.all()
        categorias = Categoria.query.all()
        marcas = Marca.query.all()
        stocks = Stock.query.all()
        return render_template('nuevo_equipo.html', modelos=modelos, categorias=categorias, marcas=marcas, stocks=stocks)
    
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            modelo_id = request.form.get('modelo_id')
            categoria_id = request.form.get('categoria_id')
            marca_id = request.form.get('marca_id')
            costo = request.form.get('costo')
            stock_id = request.form.get('stock_id')

            if not nombre or not modelo_id or not categoria_id or not marca_id or not costo or not stock_id:
                raise ValueError("Todos los campos son necesarios.")
                
            nuevo_equipo = Equipo(
                nombre=nombre,
                modelo_id=int(modelo_id),
                categoria_id=int(categoria_id),
                marca_id=int(marca_id),
                costo=float(costo),
                stock_id=int(stock_id)
            )
            db.session.add(nuevo_equipo)
            db.session.commit()
            return redirect(url_for('listar_equipos'))
        except ValueError as ve:
            return render_template('nuevo_equipo.html', error=str(ve))
        except Exception as e:
            print(f"Error al agregar nuevo equipo: {e}")
            return render_template('nuevo_equipo.html', error="No se pudo agregar el nuevo equipo. Inténtalo de nuevo.")
        
@equipo_bp.route('/editar_equipo/<int:id>', methods=['GET', 'POST'])
@jwt_required()
def editar_equipo(id):
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if administrador is False:
        return jsonify(Mensaje="Debes ser admin para poder editar un equipo")
    
    # Código para editar un equipo existente
    equipo = Equipo.query.get_or_404(id)
    modelos = Modelo.query.all()
    categorias = Categoria.query.all()
    marcas = Marca.query.all()
    stocks = Stock.query.all()

    if request.method == 'POST':
        try:
            equipo.nombre = request.form['nombre']
            equipo.modelo_id = int(request.form['modelo_id'])
            equipo.categoria_id = int(request.form['categoria_id'])
            equipo.marca_id = int(request.form['marca_id'])
            equipo.costo = float(request.form['costo'])
            equipo.stock_id = int(request.form['stock_id'])
            
            db.session.commit()
            return redirect(url_for('listar_equipos'))
        except Exception as e:
            print(f"Error al actualizar el equipo: {e}")
            return render_template('editar_equipo.html', equipo=equipo, modelos=modelos, categorias=categorias, marcas=marcas, stocks=stocks, error="No se pudo actualizar el equipo. Inténtalo de nuevo.")

    return render_template('editar_equipo.html', equipo=equipo, modelos=modelos, categorias=categorias, marcas=marcas, stocks=stocks)

@equipo_bp.route('/equipo/eliminar/<int:id>', methods=['POST'])
@jwt_required()
def eliminar_equipo(id):
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if administrador is False:
        return jsonify(Mensaje="Debes ser admin para poder eliminar un equipo")
    
    # Código para eliminar un equipo
    equipo = Equipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    return redirect(url_for('listar_equipos'))