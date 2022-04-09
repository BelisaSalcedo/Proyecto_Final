
from fileinput import close
import sqlite3
import requests

from flask import flash, request

from balance import  URL_TASA_ESPECIFICA
from balance.config import API_KEY
from balance.errors import APIError
class ObtenerCambio:
    def obtener_cambio( self,origen, destino):
        self.origen=origen
        self.destino=destino
        try:
            respuesta=requests.get(URL_TASA_ESPECIFICA .format(self.origen,self.destino,API_KEY))
            cambio=respuesta.json()["rate"]
            return cambio
        except:
            raise APIError(respuesta.status_code)
        

class ProcesaDatos:
    def recupera_datos(self) :
        oc=ObtenerCambio()
        
        con=sqlite3.connect("data/proyecto_final.db")
        cur =con.cursor()
        cur.execute("""
                        select fecha, hora, divisa, cantidad,tipo_operacion ,cantidad*1
                        from movimientos
                        order by fecha,hora, tipo_operacion
                        """
            )
                        
            
        datos = []            
        dato= cur.fetchone()
        while dato:
            dato=list(dato)
            if dato[3] !='EUR':        
                tasa=oc.obtener_cambio(dato[2],'EUR')
                dato[3]=float(dato[3])
                dato[5]=dato[3]*tasa
            else: dato[5]=dato[3]
           
            datos.append(dato)
            dato=cur.fetchone()
            #hay que cambiar el ultimo campo haciendo la llamada a Apicoin y quietarlo del resultado de la qwery
        
        con.close()
        return datos
    
    def inserta_datos (self,fecha,hora,divisa,cantidad,tipo_operacion):
        con=sqlite3.connect("data/proyecto_final.db")
        cur =con.cursor()

        cur.execute ("""
                    Insert into movimientos (fecha,hora,divisa,cantidad,tipo_operacion)
                    values (?,?,?,?,?)
                    """ ,( fecha,hora,divisa,cantidad,tipo_operacion))
        
        con.commit()
        con.close()
    
    def cantidad_divisa(self,divisa) :
        params=[1,divisa]
        con=sqlite3.connect("data/proyecto_final.db")
        cur =con.cursor()
        cur.execute("""
                    select divisa, sum(cantidad)
                    from movimientos
                    where tipo_operacion=? and divisa=?
                    group by divisa
                    """,params)
                        
                  
        sum_resultado=cur.fetchall()
        con.close()
        
        if sum_resultado:
            sumresultado=sum_resultado[0][1]
            sumresultado=float(sumresultado)

            
            params=(0,divisa)
            con=sqlite3.connect("data/proyecto_final.db")
            cur =con.cursor()
            r=cur.execute("""
                            
                        select divisa, sum(cantidad)
                        from movimientos
                        where tipo_operacion=? and divisa=?
                        group by divisa
                        
                        """,params)
                    
            resta_resultado=cur.fetchall()
            con.close()
            if resta_resultado:
                restaresultado= resta_resultado[0][1]
                restaresultado=float(resta_resultado[0][1])
                resultado=sumresultado-restaresultado

                return resultado
            else: return sumresultado
        else: resultado=-100
        return resultado