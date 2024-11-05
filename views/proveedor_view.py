from flask import Blueprint, request, make_response, jsonify, render_template, redirect, url_for

from app import db
from models import Proveedor
from schemas import ProveedorSchema
from flask_jwt_extended import(
    jwt_required,               #para saber si el usuario esta autenticado
    get_jwt,                    #para saber si el usuario es admin
)
proveedor_bp = Blueprint('proveedor', __name__)

# Rutas para Proveedores
@proveedor_bp.route('/proveedores', methods=['GET'])
def listar_proveedores():
    # Código para listar proveedores
    proveedores = Proveedor.query.all()
    return render_template('proveedores.html', proveedores=proveedores)

@proveedor_bp.route('/proveedores/nuevo', methods=['GET', 'POST'])
@jwt_required()
def nuevo_proveedor():
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if administrador is False:
        return jsonify(Mensaje="Debes ser admin para poder agregar nuevo proveedor")
    
    # Código para agregar un nuevo proveedor
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            contacto = request.form.get('contacto')

            nuevo_proveedor = Proveedor(nombre=nombre, contacto=contacto)
            db.session.add(nuevo_proveedor)
            db.session.commit()

            return redirect(url_for('listar_proveedores'))
        except Exception as e:
            print(f"Error al agregar nuevo proveedor: {e}")
            return render_template('nuevo_proveedores.html', error="No se pudo agregar el nuevo proveedor. Inténtalo de nuevo.")
    return render_template('nuevo_proveedores.html')

@proveedor_bp.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
@jwt_required()
def editar_proveedor(id):
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if administrador is False:
        return jsonify(Mensaje="Debes ser admin para poder editar un proveedor")
    
    # Código para editar un proveedor existente
    proveedor = Proveedor.query.get_or_404(id)
    
    if request.method == 'POST':
        proveedor.nombre = request.form['nombre']
        proveedor.contacto = request.form['contacto']
        
        db.session.commit()
        return redirect(url_for('listar_proveedores'))
    
    return render_template('editar_proveedores.html', proveedor=proveedor)
