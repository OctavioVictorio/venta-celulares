from flask import Blueprint, request, jsonify, render_template, redirect, url_for

from app import db
from models import Accesorio, Proveedor

from schemas import AccesorioSchema

from flask_jwt_extended import(
    jwt_required,               #para saber si el usuario esta autenticado
    get_jwt,                    #para saber si el usuario es admin
)

accesorio_bp = Blueprint('accesorio', __name__)


# Rutas para Accesorios
@accesorio_bp.route('/accesorios')
def listar_accesorios():
    # Código para listar accesorios
    accesorios = Accesorio.query.all()
    return render_template('accesorios.html', accesorios=accesorios)

@accesorio_bp.route('/accesorios/nuevo', methods=['GET', 'POST'])
@jwt_required()
def nuevo_accesorio():
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if administrador is False:
        return jsonify(Mensaje="Debes ser admin para poder agregar nuevo accesorio")
    # Código para agregar un accesorio
    proveedores = Proveedor.query.all()  # Obtener todos los proveedores de la base de datos

    if request.method == 'POST':
        try:
            tipo = request.form.get('tipo')
            compatible_con = request.form.get('compatible_con')
            proveedor_id = request.form.get('proveedor')  # Obtener el ID del proveedor seleccionado

            nuevo_accesorio = Accesorio(tipo=tipo, compatible_con=compatible_con, proveedor_id=proveedor_id)
            db.session.add(nuevo_accesorio)
            db.session.commit()

            return redirect(url_for('listar_accesorios'))
        except Exception as e:
            print(f"Error al agregar nuevo accesorio: {e}")
            return render_template('nuevo_accesorio.html', proveedores=proveedores, error="No se pudo agregar el nuevo accesorio. Inténtalo de nuevo.")
    
    return render_template('nuevo_accesorio.html', proveedores=proveedores)

@accesorio_bp.route('/editar_accesorio/<int:id>', methods=['GET', 'POST'])
@jwt_required()
def editar_accesorio(id):
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if administrador is False:
        return jsonify(Mensaje="Debes ser admin para poder editar un accesorio")
    
    accesorio = Accesorio.query.get_or_404(id)
    proveedores = Proveedor.query.all()

    if request.method == 'POST':
        accesorio.tipo = request.form['tipo']
        accesorio.compatible_con = request.form['compatible_con']
        accesorio.proveedor_id = request.form['proveedor']  # Actualizar el proveedor
        db.session.commit()
        return redirect(url_for('lista_accesorios'))

    return render_template('editar_accesorio.html', accesorio=accesorio, proveedores=proveedores)