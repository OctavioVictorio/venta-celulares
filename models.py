from app import db  # Importar la instancia de db desde app.py

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    costo = db.Column(db.Float, nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)

    modelo_relacionado = db.relationship('Modelo', backref=db.backref('equipos', lazy=True))
    categoria_relacionado = db.relationship('Categoria', backref=db.backref('equipos', lazy=True))
    stock_relacionado = db.relationship('Stock', backref=db.backref('equipos', lazy=True))
    marca_relacionado = db.relationship('Marca', backref=db.backref('equipos', lazy=True))

    accesorios = db.relationship('Accesorio', secondary='equipo_accesorios', backref=db.backref('equipos', lazy=True))

class EquipoAccesorios(db.Model):
    __tablename__ = 'equipo_accesorios'
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), primary_key=True)
    accesorio_id = db.Column(db.Integer, db.ForeignKey('accesorio.id'), primary_key=True)

class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'), nullable=False)

    fabricante_relacionado = db.relationship('Fabricante', backref=db.backref('modelos', lazy=True))

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    pais_origen = db.Column(db.String(50))

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

class Caracteristica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    equipo_relacionado = db.relationship('Equipo', backref=db.backref('caracteristicas', lazy=True))

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.String(50))

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    contacto = db.Column(db.String(50))

    accesorios = db.relationship('Accesorio', backref='proveedor', lazy=True)

class Accesorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    compatible_con = db.Column(db.String(50))
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
