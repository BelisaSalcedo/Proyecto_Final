
from  config import RUTA_BBDD
import sqlite3
import requests

from flask import flash, request

from balance import  URL_TASA_ESPECIFICA,app
from config import API_KEY
from balance.errors import APIError


ruta_db=app.config['RUTA_BBDD']

class ObtenerCambio:
    def obtener_cambio( self,origen, destino):
        self.origen=origen
        self.destino=destino
        
        
        respuesta=requests.get(URL_TASA_ESPECIFICA .format(self.origen,self.destino,API_KEY))
        if respuesta.status_code ==200:
            cambio=respuesta.json()["rate"]
            return cambio
        else:
            raise APIError
           

            
        

class ProcesaDatos:
    def recupera_datos(self) :
        oc=ObtenerCambio()
        
        con=sqlite3.connect(ruta_db)
        cur =con.cursor()
        cur.execute("""
                        select fecha, hora, divisa, cantidad,tipo_operacion ,cantidad*1, tasa, divisa_origen
                        from movimientos
                        order by fecha,hora,hora, tipo_operacion
                        """
            )
                        
            
        datos = []            
        dato= cur.fetchone()
        while dato:
            dato=list(dato)
            if dato[2] !='EUR':
                tasa=oc.obtener_cambio(dato[2],'EUR')
                dato[3]=round(float(dato[3]),9)
                dato[5]=round(dato[3]*tasa,9)
                dato[6]=round(dato[6],9)
              
            else:
                dato[3]=round(dato[3],9) 
                dato[5]=round(dato[3],9)
                dato[6]=round(dato[6],9)
           
            datos.append(dato)
            dato=cur.fetchone()
            
        
        con.close()
        return datos
    
    def inserta_datos (self,fecha,hora,divisa,cantidad,tipo_operacion,tasa,divisa_origen):
        con=sqlite3.connect(ruta_db)
        cur =con.cursor()

        cur.execute ("""
                    Insert into movimientos (fecha,hora,divisa,cantidad,tipo_operacion,tasa,divisa_origen)
                    values (?,?,?,?,?,?,?)
                    """ ,( fecha,hora,divisa,cantidad,tipo_operacion,tasa,divisa_origen))
        
        con.commit()
        con.close()
    
    def cantidad_divisa(self,divisa) :
        params=[1,divisa]
        con=sqlite3.connect(ruta_db)
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
            con=sqlite3.connect(ruta_db)
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

                return round(resultado,9)
            else: return round(sumresultado,9)
        else: resultado=-100
        return round (resultado,9)
    def valida_datos(self,divisa,moneda_origen_h,cantidad, cantidad_origen_h,divisa2,moneda_destino_h):
        cantidad_origen_h=float(cantidad_origen_h)
        cantidad=float(cantidad)

        if divisa==moneda_origen_h and cantidad==cantidad_origen_h and divisa2==moneda_destino_h:
            resultado=True
        else: resultado=False
        return resultado

    def estado_inversion(self):
        oc=ObtenerCambio()
        params=(1,'EUR')
        con=sqlite3.connect(ruta_db)
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
            con=sqlite3.connect(ruta_db)
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
           
    
        posicion_cripto_monedas=round(suma_cripto,9)
        con=sqlite3.connect(ruta_db)
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
        con=sqlite3.connect(ruta_db)
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
                poseur= round(venta_pos_eur[1]-compra_pos_eur[1],9)
            else: poseur=round(-compra_pos_eur[1],9)
        else: poseur=0

        con=sqlite3.connect(ruta_db)
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
        beneficio=round (poseur+posicion_cripto_monedas,9)

        datos=(origen_inv, posicion_cripto_monedas,poseur,beneficio)

        return datos


        