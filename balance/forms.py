from datetime import datetime

from sqlite3 import Time

from flask_wtf import FlaskForm
from wtforms import DateField, SelectField,FloatField,SubmitField,TimeField
from wtforms.validators import DataRequired, NumberRange

class MovimientosForm(FlaskForm):
    fecha=DateField ("Fecha", validators=[DataRequired(message='Falta la hora')] )
    hora=TimeField("Hora", validators=[DataRequired()])
    moneda_origen=SelectField ("Moneda Origen", validators=[DataRequired()],
                                choices=[(0,'EUR'), (1,'BTC'), (2,'ETH'), (3,'BNB'),(4,'LUNA'), (5,'SOL'), (6,'BCH'),(7,'LINK'),(8,'ATOM'),(9,'USDT') ])

    cantidad_origen=FloatField("Cantidad Origen",validators=[DataRequired(), NumberRange(message="Debe ser una cantidad positivo",min=0.0000000000001)])
    moneda_destino=SelectField ("Moneda Origen", validators=[DataRequired()],
                                choices=[(0,'EUR'), (1,'BTC'), (2,'ETH'), (3,'BNB'),(4,'LUNA'), (5,'SOL'), (6,'BCH'),(7,'LINK'),(8,'ATOM'),(9,'USDT') ])

    cantidad_destino=FloatField("Cantidad Destino",validators=[DataRequired(), NumberRange(message="Debe ser una cantidad positivo",min=0.0000000000001)])

    aceptar=SubmitField("Aceptar")



