

import sqlite3
from balance import app
from flask import redirect, render_template,flash, request

from balance.models import  ObtenerCambio, ProcesaDatos
from balance.forms import MovimientosForm
from datetime import datetime,date



@app.route("/")
def inicio():
    data_manager=ProcesaDatos()
    
 
    
    try:
        datos=data_manager.recupera_datos()
        return render_template("movimientos.html", movimientos=datos)
    except sqlite3.Error as e:
        flash ("Se ha producido un error en la bbdd.Intentelo de nuevo")
        return render_template("movimientos.html", movimientos=[])      

@app.route("/nuevo_movimiento", methods=['GET','POST'])

def nuevo_movimiento():
    form=MovimientosForm()
    if request.method =='GET':
        return render_template("nuevo_movimiento.html", formulario=form)
    else:
        #validar
        try:
            
            #recuperar los datos de form y pasarselos al model a grabar
            data_manager=ProcesaDatos()
            fecha= (date.today().year)*1000 + date.today().month*100+date.today().day
            hora=datetime.now().time().hour *10000  + datetime.now().time().minute *100 + datetime.now().time().second 
            if form.moneda_origen.data =='0':
                    divisa='EUR'
            elif form.moneda_origen.data =='1':
                    divisa='BTC'
            elif form.moneda_origen.data =='2':
                    divisa='ETH'
            elif form.moneda_origen.data =='3':
                    divisa='BNB'
            elif form.moneda_origen.data =='4':
                    divisa='LUNA'
            elif form.moneda_origen.data =='5':
                    divisa='SOL'
            elif form.moneda_origen.data =='6':
                    divisa='BCH'
            elif form.moneda_origen.data =='7':
                    divisa='LINK'
            elif form.moneda_origen.data =='8':
                    divisa='ATOM'
            else: divisa='USDT'
            cantidad=form.cantidad_origen.data
            comprueba=data_manager.cantidad_divisa (divisa)
            if comprueba <0:
                flash("la cantidad origen no es correcta")
                return render_template ("nuevo_movimiento.html", formulario=form)
            else:

                data_manager.inserta_datos(fecha,hora,divisa,cantidad,0)
            
                
            
                if form.moneda_destino.data =='0':
                        divisa2='EUR'
                elif form.moneda_destino.data =='1':
                        divisa2='BTC'
                elif form.moneda_destino.data =='2':
                        divisa2='ETH'
                elif form.moneda_destino.data =='3':
                        divisa2='BNB'
                elif form.moneda_destino.data =='4':
                        divisa2='LUNA'
                elif form.moneda_destino.data =='5':
                        divisa2='SOL'
                elif form.moneda_destino.data =='6':
                        divisa2='BCH'
                elif form.moneda_destino.data =='7':
                        divisa2='LINK'
                elif form.moneda_destino.data =='8':
                        divisa2='ATOM'
                else: divisa2='USDT'
                co=ObtenerCambio()
                cambio=co.obtener_cambio(divisa,divisa2)
                cantidad2=cambio*cantidad
                    
                data_manager.inserta_datos(fecha,hora,divisa2,cantidad2,1)
                return redirect("/")
            

        
        except sqlite3.Error as e:
            flash("se ha producido un error en la bbdd")
            return render_template ("movimientos.html", movimientos=[])

@app.route("/posiciones", methods=['GET'])
def estado():
    data_manager=ProcesaDatos()
    try:
        datos=data_manager.estado_inversion()
        return render_template("posiciones.html", movimientos=datos)
    except sqlite3.Error as e:
        flash ("Se ha producido un error en la bbdd.Intentelo de nuevo")
        return render_template("posiciones.html", movimientos=[]) 
   