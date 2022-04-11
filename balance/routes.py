

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
        if form.aceptar.data:

                        try:
                        
                        #recuperar los datos de form y pasarselos al model a grabar
                                data_manager=ProcesaDatos()
                                fecha= (date.today().year)*1000 + date.today().month*100+date.today().day
                                hora=datetime.now().time().hour *10000  + datetime.now().time().minute *100 + datetime.now().time().second 
                                divisa=form.moneda_origen.data
                                
                                cantidad=form.cantidad_origen.data
                                #comprueba=data_manager.cantidad_divisa (divisa)
                                
                                #if comprueba <0 and divisa!='EUR':
                                        #flash("la cantidad origen no es correcta")
                                        #return render_template ("nuevo_movimiento.html", formulario=form)
                                
                                data_manager.inserta_datos(fecha,hora,divisa,cantidad,0)
                        
                        
                        
                                
                                divisa2=form.moneda_destino.data
                               
                                if form.cantidad_destino_h.data:
                                        cantidad2=form.cantidad_destino_h.data
                                        
                                        data_manager.inserta_datos(fecha,hora,divisa2,cantidad2,1)
                                        return redirect("/")
                                else: 
                                        flash("No tenemos cantidad destino. Tienes que darle a clacular")
                                        return render_template("nuevo_movimiento.html", formulario=form)
                        except sqlite3.Error as e:
                                flash("se ha producido un error en la bbdd")
                                return render_template ("movimientos.html", movimientos=[])
               
        
        else:
                data_manager=ProcesaDatos()
                
                divisa=form.moneda_origen.data
     
                
                cantidad=form.cantidad_origen.data
                comprueba=data_manager.cantidad_divisa (divisa)
                resultado=comprueba-cantidad
                                
                if resultado <0 and divisa!='EUR':
                        flash("la cantidad origen no es correcta (no tienes suficientes monedas origen), si es la primera compra debe ser en EUR")
                        return render_template ("nuevo_movimiento.html", formulario=form)
                else:
                        divisa2=form.moneda_destino.data
                        co=ObtenerCambio()
                        cambio=co.obtener_cambio(divisa,divisa2)
                        cantidad2=cambio*cantidad
                        form.cantidad_destino.data=cantidad2
                        form.cantidad_destino_h.data=cantidad2
                        return render_template("nuevo_movimiento.html", formulario=form)

                

@app.route("/posiciones", methods=['GET'])
def estado():
    data_manager=ProcesaDatos()
    try:
        datos=data_manager.estado_inversion()
        return render_template("posiciones.html", movimientos=datos)
    except sqlite3.Error as e:
        flash ("Se ha producido un error en la bbdd.Intentelo de nuevo")
        return render_template("posiciones.html", movimientos=[]) 
   