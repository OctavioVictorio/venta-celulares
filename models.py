from app import db  # Importar la instancia de db desde app.py

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Equipo(db.Model):
    __tablename__ = 'equipo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    costo = db.Column(db.Float, nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)

    modelo_relacionado = db.relationship('Modelo', backref=db.backref('equipos_modelo', lazy=True))
    categoria_relacionado = db.relationship('Categoria', backref=db.backref('equipos_categoria', lazy=True))
    stock_relacionado = db.relationship('Stock', backref=db.backref('equipos_stock', lazy=True))
    marca_relacionado = db.relationship('Marca', backref=db.backref('equipos_marca', lazy=True))

    accesorios = db.relationship('Accesorio', secondary='equipo_accesorio', backref=db.backref('equipos_accesorio', lazy=True))
    caracteristicas_relacionadas = db.relationship('Caracteristica', backref='equipo_relacionado', lazy=True)  

class Fabricante(db.Model):
    __tablename__ = 'fabricante'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    pais_origen = db.Column(db.String(50))

class Marca(db.Model):
    __tablename__ = 'marca'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return self.nombre

class Modelo(db.Model):
    __tablename__ = 'modelo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'), nullable=False)

    fabricante_relacionado = db.relationship('Fabricante', backref=db.backref('modelos', lazy=True))
class Caracteristica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(120), nullable=False)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False) 

    equipo = db.relationship('Equipo', backref=db.backref('caracteristicas', lazy=True))

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    contacto = db.Column(db.String(50))

    accesorios = db.relationship('Accesorio', backref='proveedor_relacionado', lazy=True)

class Accesorio(db.Model):
    __tablename__ = 'accesorio'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    compatible_con = db.Column(db.String(50))
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)

    proveedor = db.relationship('Proveedor', backref=db.backref('accesorios_relacionado', lazy=True))

class EquipoAccesorio(db.Model):
    __tablename__ = 'equipo_accesorio'
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), primary_key=True)
    accesorio_id = db.Column(db.Integer, db.ForeignKey('accesorio.id'), primary_key=True)

    equipo = db.relationship('Equipo', backref=db.backref('equipos_accesorios', lazy=True))
    accesorio = db.relationship('Accesorio', backref=db.backref('equipos_accesorios', lazy=True))


class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.String(50))
