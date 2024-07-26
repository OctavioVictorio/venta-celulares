from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/venta_celulares'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Equipo, Modelo, Marca, Categoria, Stock

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
        
        print(f"Modelos: {modelos}")
        print(f"Categorías: {categorias}")
        print(f"Marcas: {marcas}")
        print(f"Stocks: {stocks}")
        
        return render_template('nuevo_equipo.html', modelos=modelos, categorias=categorias, marcas=marcas, stocks=stocks)
    
    if request.method == 'POST':
        try:
            data = request.form
            nombre = data.get('nombre')
            modelo_id = int(data.get('modelo_id'))
            categoria_id = int(data.get('categoria_id'))
            marca_id = int(data.get('marca_id'))
            costo = float(data.get('costo'))
            stock_id = int(data.get('stock_id'))

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

if __name__ == '__main__':
    app.run(debug=True)
