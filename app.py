from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/venta_celulares'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importa los modelos necesarios
from models import Equipo, Modelo, Marca, Fabricante, Caracteristica, Stock, Proveedor, Accesorio, Categoria

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
            modelo_id = int(request.form.get('modelo_id'))
            categoria_id = int(request.form.get('categoria_id'))
            marca_id = int(request.form.get('marca_id'))
            costo = float(request.form.get('costo'))
            stock_id = int(request.form.get('stock_id'))

            nuevo_equipo = Equipo(
                nombre=nombre,
                modelo_id=modelo_id,
                categoria_id=categoria_id,
                marca_id=marca_id,
                costo=costo,
                stock_id=stock_id
            )
            db.session.add(nuevo_equipo)
            db.session.commit()
            return redirect(url_for('listar_equipos'))
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

# Nuevas rutas para modelos y otros datos

@app.route('/modelos')
def listar_modelos():
    modelos = Modelo.query.all()
    return render_template('modelos.html', modelos=modelos)

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

@app.route('/modelo/eliminar/<int:id>', methods=['POST'])
def eliminar_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    db.session.delete(modelo)
    db.session.commit()
    return redirect(url_for('listar_modelos'))

@app.route('/marcas')
def listar_marcas():
    marcas = Marca.query.all()
    return render_template('marcas.html', marcas=marcas)

@app.route('/marca/editar/<int:id>', methods=['GET', 'POST'])
def editar_marca(id):
    marca = Marca.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            marca.nombre = request.form['nombre']
            db.session.commit()
            return redirect(url_for('listar_marcas'))
        except Exception as e:
            print(f"Error al actualizar la marca: {e}")
            return render_template('editar_marca.html', marca=marca, error="No se pudo actualizar la marca. Inténtalo de nuevo.")
    
    return render_template('editar_marca.html', marca=marca)

@app.route('/marca/eliminar/<int:id>', methods=['POST'])
def eliminar_marca(id):
    marca = Marca.query.get_or_404(id)
    db.session.delete(marca)
    db.session.commit()
    return redirect(url_for('listar_marcas'))

@app.route('/fabricantes')
def listar_fabricantes():
    fabricantes = Fabricante.query.all()
    return render_template('fabricantes.html', fabricantes=fabricantes)

@app.route('/caracteristicas')
def listar_caracteristicas():
    caracteristicas = Caracteristica.query.all()
    return render_template('caracteristicas.html', caracteristicas=caracteristicas)

@app.route('/stock')
def listar_stock():
    stock = Stock.query.all()
    return render_template('stock.html', stock=stock)

@app.route('/proveedores')
def listar_proveedores():
    proveedores = Proveedor.query.all()
    return render_template('proveedores.html', proveedores=proveedores)

@app.route('/accesorios')
def listar_accesorios():
    accesorios = Accesorio.query.all()
    return render_template('accesorios.html', accesorios=accesorios)

if __name__ == '__main__':
    app.run(debug=True)
