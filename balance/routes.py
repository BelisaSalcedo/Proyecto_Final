

import sqlite3
from balance import app
from flask import redirect, render_template,flash, request
from balance.errors import APIError

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
            flash ("Se ha producido un error en la bbdd.")
            return render_template("movimientos.html", movimientos=[]) 
    except APIError:
        flash ("Se ha producido un error con la conexion a la APICOIN, compruebe su API_KEY.")
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
                                    fecha=datetime.now().date()
                                    
                                # fecha= (date.today().year)*1000 + date.today().month*100+date.today().day
                                    hora=str(datetime.now().time().hour)+":" + str(datetime.now().time().minute) +":"+ str(datetime.now().time().second)
                                    divisa=form.moneda_origen.data                            
                                    cantidad=form.cantidad_origen.data
                                    divisa2=form.moneda_destino.data
                                    coherencia=data_manager.valida_datos(divisa,form.moneda_origen_h.data,cantidad, form.cantidad_origen_h.data,divisa2,form.moneda_destino_h.data)
                                    if coherencia:

                                        if form.cantidad_destino_h.data:
                                                data_manager.inserta_datos(fecha,hora,divisa,cantidad,0)
                                                cantidad2=form.cantidad_destino_h.data
                                                
                                                data_manager.inserta_datos(fecha,hora,divisa2,cantidad2,1)
                                                return redirect("/")
                                        else: 
                                                flash("No tenemos cantidad destino. Tienes que darle a clacular")
                                                return render_template("nuevo_movimiento.html", formulario=form)
                                    else:
                                        flash("has cambiado los datos sin dar a calcular")
                        
                                        return render_template("nuevo_movimiento.html", formulario=form)
                           

                        except sqlite3.Error as e:
                                flash("se ha producido un error en la bbdd")
                                return render_template ("movimientos.html", movimientos=[])
                        
               
        
        else:
                data_manager=ProcesaDatos()
                
                divisa=form.moneda_origen.data
                form.moneda_origen_h.data=divisa
     
                
                cantidad=form.cantidad_origen.data
                form.cantidad_origen_h.data=cantidad
                comprueba=data_manager.cantidad_divisa (divisa)
                resultado=comprueba-cantidad
                                
                if resultado <0 and divisa!='EUR':
                        flash("la cantidad origen no es correcta (no tienes suficientes monedas origen), si es la primera compra debe ser en EUR")
                        return render_template ("nuevo_movimiento.html", formulario=form)
                
                else:

                        divisa2=form.moneda_destino.data
                        form.moneda_destino_h.data=divisa2
                        if divisa2==divisa:
                            flash("la divisa origen es igual a la divisa destino")
                            return render_template ("nuevo_movimiento.html", formulario=form)
                        else:

                            co=ObtenerCambio()
                            try:
                                cambio=co.obtener_cambio(divisa,divisa2)
                            except:
                                flash("No se puede conectar a la APPI, comprueba tu API_KEY")
                                return render_template ("nuevo_movimiento.html", formulario=form)
                            cantidad2=cambio*cantidad
                            
                            form.cantidad_destino.data=cantidad2
                            form.cantidad_destino_h.data=cantidad2
                            return render_template("nuevo_movimiento.html", formulario=form)

                

@app.route("/posiciones", methods=['GET'])
def estado():
    data_manager=ProcesaDatos()
    oc=ObtenerCambio()
    
    try:
        datos=data_manager.estado_inversion()
       
        return render_template("posiciones.html", movimientos=datos)

    except sqlite3.Error as e:
        flash ("Se ha producido un error en la bbdd")
        return render_template("posiciones.html", movimientos=[]) 
    except APIError:
        flash ("No se puede conectar a la APPI, comprueba tu API_KEY")
        return render_template("posiciones.html", movimientos=[]) 
