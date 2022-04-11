
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
            if dato[2] !='EUR':        
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
    
    def estado_inversion(self):
        oc=ObtenerCambio()
        params=(1,'EUR')
        con=sqlite3.connect("data/proyecto_final.db")
        cur =con.cursor()
        cur.execute("""
                        select divisa, sum(cantidad)
                        from movimientos
                        where tipo_operacion=? and divisa is not ?
                        group by divisa
                        
                        """,params)
        suma_resultado=cur.fetchone()
        datos= []
        while suma_resultado:
            divisa=suma_resultado[0]
            params=(0,'EUR',divisa)
            con=sqlite3.connect("data/proyecto_final.db")
            cur =con.cursor()
            cur.execute("""
                            
                        select ifnull(divisa,0), ifnull(sum(cantidad),0)
                        from movimientos
                        where tipo_operacion=? and divisa<>? and divisa=?
                        group by divisa
                        
                        """,params)
            resta_resultado=cur.fetchone()
            if resta_resultado:
                resta=resta_resultado[1]
            else: resta=0
            #con.close()
            total_divisa=suma_resultado[1]-resta
            datos.append((divisa,total_divisa))
            suma_resultado=cur.fetchone()
        #con.close()
        i=0
        suma_cripto=0
        oc=ObtenerCambio()
        for dato in datos:           
           divisa1=dato[0]
           
           tasa=oc.obtener_cambio(divisa1,'EUR')
           suma_cripto+=tasa*(datos[i][1])
           
    
        posicion_cripto_monedas=suma_cripto
        con=sqlite3.connect("data/proyecto_final.db")
        cur =con.cursor()
        params_c=(0,'EUR')
        cur.execute("""
                            
                        select divisa, ifnull(sum(cantidad),0)
                        from movimientos 
                        where tipo_operacion=? and divisa=?
                        group by 1
                        
                        """,params_c)
        compra_pos_eur=cur.fetchone()
        con.close()
        con=sqlite3.connect("data/proyecto_final.db")
        cur =con.cursor()
        params_v=(1,'EUR')
        cur.execute("""
                            
                        select ifnull(divisa,0), ifnull(sum(cantidad),0)
                        from movimientos 
                        where tipo_operacion=? and divisa=?
                        group by 1
                        
                        """,params_v)
        venta_pos_eur=cur.fetchone()
        con.close()
        if compra_pos_eur:
            if venta_pos_eur:
                poseur= compra_pos_eur[1]-venta_pos_eur[1]
            else: poseur=-compra_pos_eur[1]
        else: poseur=0

        con=sqlite3.connect("data/proyecto_final.db")
        cur =con.cursor()
        params=(0,'EUR')
        cur.execute("""
                            
                        select ifnull(cantidad,0)
                        from movimientos 
                        where tipo_operacion=? and divisa=?
                        order by fecha,hora
                        limit 1
                        """,params)
        origen=cur.fetchone()
        con.close()
        if origen:
            origen_inv=origen[0]
        else:origen_inv=0

        datos=(origen_inv, posicion_cripto_monedas,poseur)

        return datos


        