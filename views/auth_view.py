#para tiempo de vencimiento
from datetime import timedelta

from flask import Blueprint, request, jsonify, make_response, render_template

#crear token
from flask_jwt_extended import(
    create_access_token,
    jwt_required,               #para saber si el usuario esta autenticado
    get_jwt,                    #para saber si el usuario es admin
)

#encriptar password
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from app import db
from models import User, Equipo

#importar schemas
from schemas import UserSchema, UserMinimalSchema

#autorizaciones de rutas
auth_bp = Blueprint('auth', __name__)

#crear token de login con post
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.authorization        #para saber la informacion del usuario
    username = data.username
    password = data.password

    usuario = User.query.filter_by(username=username).first()        #para saber si el usuario existe

    # si el usuario existe y coincide las contraseñas
    if usuario and check_password_hash(    #recibe contraseña hasheada y la contraseña del usuario
        pwhash = usuario.password_hash,
        password = password
    ):
        access_token = create_access_token(                     #para crear el token
            identity = username,                                #identidad del usuario
            expires_delta = timedelta(minutes=30),              #tiempo de expiración
            additional_claims=dict(                             #para saber si el usuario es admin
                administrador = usuario.is_admin
            )
        )
        #una ves ya creado el token, lo devolvemos
        return jsonify({'Token':f'Bearer {access_token}'})

    return jsonify(Mensaje ="El nombre de usuario o la contraseña son incorrectos")

#listar todos los usuarios
@auth_bp.route('/users', methods=['GET', 'POST'])
@jwt_required()                                 # solo los usuarios autenticados pueden acceder
def users():
    addittionals_data = get_jwt()                      #para saber si el usuario es admin
    administrador = addittionals_data['administrador']

    if request.method == 'POST':
        if administrador is True:
            data = request.get_json()               #obtiene la informacion del usuario
            username = data.get('usuario')
            password = data.get('contrasenia')

            data_a_validar = dict(
                username = username,
                password_hash = password,
                is_admin = False
            )
            errors = UserSchema().validate(data_a_validar)
            if errors:
                return make_response(jsonify(errors))

            try:
                nuevo_usuario = User(
                    username=username,
                    password_hash=generate_password_hash(password),
                    is_admin=False,
                )
                db.session.add(nuevo_usuario)
                db.session.commit()
                return jsonify(
                    {
                    "Mensaje": "Usuario creado",
                    "Usuario": nuevo_usuario.to_dict()
                    }
                )
            except:
                return jsonify(
                    {
                    "Mensaje": "Fallo al crear el usuario",
                    }
                )
        else:
            return jsonify(Mensaje= "Solo el admin puede crear nuevos usuarios")

    usuarios = User.query.all()                 #trae todos los usuarios

    # si es administrador usa el schema con todos los datos, y si no solo el username
    if administrador is True:
        return UserSchema().dump(obj=usuarios, many=True)   #devuelve los usuarios
    else:
        return UserMinimalSchema().dump(obj=usuarios, many=True)
# Actualizar usuario
@auth_bp.route('/user/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if not administrador:
        return jsonify(Mensaje="Solo un administrador puede actualizar usuarios"), 403

    usuario = User.query.get_or_404(id)
    data = request.get_json()

    # Validamos y actualizamos datos del usuario
    username = data.get('usuario', usuario.username)  # Si no se pasa un nuevo username, se queda con el actual
    password = data.get('contrasenia')
    
    if password:
        usuario.password_hash = generate_password_hash(password)
    usuario.username = username

    # Guardar cambios
    db.session.commit()
    return jsonify(Mensaje="Usuario actualizado", Usuario=usuario.to_dict())

# Eliminar usuario
@auth_bp.route('/user/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if not administrador:
        return jsonify(Mensaje="Solo un administrador puede eliminar usuarios"), 403

    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify(Mensaje="Usuario eliminado exitosamente")

# Inicio
@auth_bp.route('/')
def index():
    equipos = Equipo.query.all()
    return render_template('index.html', equipos=equipos)


