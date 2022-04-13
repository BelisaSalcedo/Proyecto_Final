

from sqlite3 import Time


from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField,FloatField,SubmitField,TextAreaField
from wtforms.validators import DataRequired, NumberRange,ValidationError
from datetime import date

def cantidad_valida(formulario, field):
    
    if field.data < 0.000:
        raise ValidationError("Esa cantidad no es valida")


class MovimientosForm(FlaskForm):
    
   # fecha=DateField ("Fecha", validators=[DataRequired(message='Falta la hora')] )
   # hora=TimeField("Hora", validators=[DataRequired()])
    moneda_origen=SelectField ("Moneda Origen", validators=[DataRequired()],
                                choices=[('EUR','EUR'), ('BTC','BTC'), ('ETH','ETH'), ('BNB','BNB'),('LUNA','LUNA'), ('SOL','SOL'), ('BCH','BCH'),('LINK','LINK'),('ATOM','ATOM'),('USDT','USDT') ])
    moneda_origen_h=HiddenField("Moneda Origen H")
    cantidad_origen=FloatField("Cantidad Origen",validators=[DataRequired(), cantidad_valida])
    cantidad_origen_h=HiddenField("Cantidad Origen H")
    moneda_destino=SelectField ("Moneda Origen", validators=[DataRequired()],
                                choices=[('EUR','EUR'), ('BTC','BTC'), ('ETH','ETH'), ('BNB','BNB'),('LUNA','LUNA'), ('SOL','SOL'), ('BCH','BCH'),('LINK','LINK'),('ATOM','ATOM'),('USDT','USDT') ])
    moneda_destino_h=HiddenField("Moneda Destino H")
    cantidad_destino=TextAreaField("Cantidad Destino")
    cantidad_destino_h=HiddenField("cantidad_destino_h")
    
    aceptar=SubmitField("Aceptar")
    calcular=SubmitField("Calcular")



