from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, IntegerField

class MarcaForm(FlaskForm):
        nombre = StringField('Nombre')
        submit = SubmitField('Guardar')
        


    