

from sqlite3 import Time


from flask_wtf import FlaskForm
from wtforms import DateField, SelectField,FloatField,SubmitField
from wtforms.validators import DataRequired, NumberRange,ValidationError
from datetime import date

def cantidad_valida(formulario, field):
    
    if field.data < 0:
        raise ValidationError("Esa cantidad no es valida")


class MovimientosForm(FlaskForm):
    
   # fecha=DateField ("Fecha", validators=[DataRequired(message='Falta la hora')] )
   # hora=TimeField("Hora", validators=[DataRequired()])
    moneda_origen=SelectField ("Moneda Origen", validators=[DataRequired()],
                                choices=[(0,'EUR'), (1,'BTC'), (2,'ETH'), (3,'BNB'),(4,'LUNA'), (5,'SOL'), (6,'BCH'),(7,'LINK'),(8,'ATOM'),(9,'USDT') ])

    cantidad_origen=FloatField("Cantidad Origen",validators=[DataRequired(), cantidad_valida])
    moneda_destino=SelectField ("Moneda Origen", validators=[DataRequired()],
                                choices=[(0,'EUR'), (1,'BTC'), (2,'ETH'), (3,'BNB'),(4,'LUNA'), (5,'SOL'), (6,'BCH'),(7,'LINK'),(8,'ATOM'),(9,'USDT') ])

    cantidad_destino=FloatField("Cantidad Destino",validators=[DataRequired()])
    
    aceptar=SubmitField("Aceptar")



