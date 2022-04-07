
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
    
    def estado_inversion (self) :
         con=sqlite3.connect("data/proyecto_final.db")
         cur =con.cursor()
         cur.execute("""
                        SELECT sum (cantidad)  from movimientos 
                        where tipo_operacion =? and divisa is not 'EUR'
                        
                        """
            )
         suma = cur.fetchall()
         con.close()
         cur=con.cursor()
         cur.execute("""
                        SELECT sum (cantidad)*-1  from movimientos 
                        where tipo_operacion =0 and divisa <>'EUR'
                        
                        """
            )
         resta = cur.fetchall()
         con.close()
         resultado=suma-resta
         cur=con.cursor()
         cur.execute("""
                        SELECT cantidad from movimientos 
                        WHERE tipo_operacion=0 AND divisa ='EUR' ORDER by fecha,hora LIMIT 1
                        
                        """
            )
         origen=cur.fetchall()
         cur=con.cursor()
         cur.execute("""
                        SELECT sum (cantidad)*-1  from movimientos 
                        where tipo_operacion =0 and divisa ='EUR'
                        
                        """
            )
         abs=cur.fetchall()
         datos=[origen,resultado, abs ]

         con.close()
         return datos
    

    def cantidad_divisa(self,divisa) :
        params=[1,divisa]
        con=sqlite3.connect("data/proyecto_final.db")
        cur =con.cursor()
        cur.execute("select * from movimientos"
        )
                  
        sum_resultado=cur.fetchone()
        con.close()
        if sum_resultado:
            sum_resultado[0][1]=float(sum_resultado[0][1])

            
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
                resta_resultado[0][1]=float(resta_resultado[0][1])
                resultado=sum_resultado[0][1]-resta_resultado[0][1]

                return resultado
            else: return sum_resultado
        else: resultado=-100
        return resultado