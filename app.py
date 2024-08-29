import os

from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, url_for, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI'
    )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY'
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Equipo, Modelo, Marca, Fabricante, Caracteristica, Stock, Proveedor, Accesorio, Categoria
from forms import MarcaForm
from services.marca_service import MarcaService
from repositories.marca_repository import MarcaRepository

@app.route("/users", methods = ['POST'])
def user():
    # informacion que recibe el metodo
    data = request.get_json()
    username = data.get('nombre_usuario')
    password = data.get('password')
    
    try:
        nuevo_usuario = User(
            username=username, 
            password=password
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({"usuario creado": username}), 201
    except:
        return jsonify({"Error": "algo salio mal" })

@app.route('/')
def index():
    equipos = Equipo.query.all()
    return render_template('index.html', equipos=equipos)

@app.route('/equipos')
def listar_equipos():
    equipos = Equipo.query.all()
    return render_template('listar_equipos.html', equipos=equipos)

@app.route('/equipo/nuevo', methods=['GET', 'POST'])
def nuevo_equipo():
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

@app.route('/editar_equipo/<int:id>', methods=['GET', 'POST'])
def editar_equipo(id):
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

@app.route('/equipo/eliminar/<int:id>', methods=['POST'])
def eliminar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    return redirect(url_for('listar_equipos'))

@app.route('/fabricantes')
def listar_fabricantes():
    fabricantes = Fabricante.query.all()
    return render_template('fabricantes.html', fabricantes=fabricantes)

@app.route('/fabricante/nuevo', methods=['GET', 'POST'])
def nuevo_fabricante():
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

@app.route('/fabricante/editar/<int:id>', methods=['GET', 'POST'])
def editar_fabricante(id):
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

@app.route('/fabricante/eliminar/<int:id>', methods=['POST'])
def eliminar_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)
    db.session.delete(fabricante)
    db.session.commit()
    return redirect(url_for('listar_fabricantes'))

@app.route('/marcas', methods=['GET', 'POST'])
def marcas():
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

@app.route('/marca/editar/<int:id>', methods=['GET', 'POST'])
def editar_marca(id):
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

@app.route('/marca/nuevo', methods=['GET', 'POST'])
def nuevo_marca():
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

@app.route('/modelos/<int:marca_id>')
def modelos_por_marca(marca_id):
    marca = Marca.query.get_or_404(marca_id)
    modelos = Modelo.query.filter_by(marca_id=marca_id).all()
    return render_template('modelos_por_marca.html', marca=marca, modelos=modelos)

@app.route('/modelos')
def listar_modelos():
    modelos = Modelo.query.all()
    return render_template('modelos.html', modelos=modelos)

@app.route('/modelo/nuevo', methods=['GET', 'POST'])
def nuevo_modelo():
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

@app.route('/modelo/editar/<int:id>', methods=['GET', 'POST'])
def editar_modelo(id):
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

@app.route('/caracteristicas', methods=['GET'])
def listar_caracteristicas():
    caracteristicas = Caracteristica.query.all()
    equipos = Equipo.query.all()  # Obtener todos los equipos para la selección

    return render_template('caracteristicas.html', caracteristicas=caracteristicas, equipos=equipos)

@app.route('/caracteristicas/nuevo', methods=['GET', 'POST'])
def agregar_caracteristica():
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

@app.route('/caracteristicas/<int:id>/editar', methods=['GET', 'POST'])
def editar_caracteristica(id):
    caracteristica = Caracteristica.query.get_or_404(id)

    if request.method == 'POST':
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']

        caracteristica.tipo = tipo
        caracteristica.descripcion = descripcion
        db.session.commit()

        return redirect(url_for('listar_caracteristicas'))

    return render_template('editar_caracteristicas.html', caracteristica=caracteristica)


@app.route('/proveedores', methods=['GET'])
def listar_proveedores():
    proveedores = Proveedor.query.all()
    return render_template('proveedores.html', proveedores=proveedores)

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():
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

@app.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    
    if request.method == 'POST':
        proveedor.nombre = request.form['nombre']
        proveedor.contacto = request.form['contacto']
        
        db.session.commit()
        return redirect(url_for('listar_proveedores'))
    
    return render_template('editar_proveedores.html', proveedor=proveedor)

@app.route('/accesorios')
def listar_accesorios():
    accesorios = Accesorio.query.all()
    return render_template('accesorios.html', accesorios=accesorios)

@app.route('/accesorios/nuevo', methods=['GET', 'POST'])
def nuevo_accesorio():
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

@app.route('/editar_accesorio/<int:id>', methods=['GET', 'POST'])
def editar_accesorio(id):
    accesorio = Accesorio.query.get_or_404(id)
    proveedores = Proveedor.query.all()

    if request.method == 'POST':
        accesorio.tipo = request.form['tipo']
        accesorio.compatible_con = request.form['compatible_con']
        accesorio.proveedor_id = request.form['proveedor']  # Actualizar el proveedor
        db.session.commit()
        return redirect(url_for('lista_accesorios'))

    return render_template('editar_accesorio.html', accesorio=accesorio, proveedores=proveedores)

if __name__ == '__main__':
    app.run(debug=True)

