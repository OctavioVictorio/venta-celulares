from app import db  # Importar la instancia de db desde app.py

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    is_admin = db.Column(db.Boolean)
    def to_dict(self):          #metodo para que devuelva el objeto(usuario) como un diccionario
        return dict(
            username = self.username,
            password = self.password_hash
        )
    

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

    accesorios = db.relationship('Accesorio', secondary='equipo_accesorio', backref=db.backref('equipos_accesorio', lazy=True), overlaps="equipo_relacionado")
    caracteristicas_relacionadas = db.relationship('Caracteristica', backref='equipo_relacionado', lazy=True, overlaps="caracteristicas, equipo")  

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "modelo": self.modelo_relacionado.nombre,
            "categoria": self.categoria_relacionado.nombre,
            "costo": self.costo,
            "marca": self.marca_relacionado.nombre,
            "stock": self.stock_relacionado.cantidad
        }

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

    equipo = db.relationship('Equipo', backref=db.backref('caracteristicas', lazy=True), overlaps="equipo_relacionado, caracteristicas_relacionadas")

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "equipo_id": self.equipo_id
        }

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    contacto = db.Column(db.String(50))

    accesorios = db.relationship('Accesorio', backref='proveedor_relacionado', lazy=True, overlaps="accesorios_relacionado")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "contacto": self.contacto
        }

class Accesorio(db.Model):
    __tablename__ = 'accesorio'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    compatible_con = db.Column(db.String(50))
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)

    proveedor = db.relationship('Proveedor', backref=db.backref('accesorios_relacionado', lazy=True), overlaps="accesorios")

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "compatible_con": self.compatible_con,
            "proveedor": self.proveedor.nombre
        }

class EquipoAccesorio(db.Model):
    __tablename__ = 'equipo_accesorio'
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), primary_key=True)
    accesorio_id = db.Column(db.Integer, db.ForeignKey('accesorio.id'), primary_key=True)

    equipo = db.relationship('Equipo', backref=db.backref('equipos_accesorios', lazy=True), overlaps="accesorios")
    accesorio = db.relationship('Accesorio', backref=db.backref('equipos_accesorios', lazy=True), overlaps="equipo_accesorios")


class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    
class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.String(50))

    def actualizar_stock(self, cantidad_nueva):
        self.cantidad = cantidad_nueva
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "cantidad": self.cantidad,
            "ubicacion": self.ubicacion
        }