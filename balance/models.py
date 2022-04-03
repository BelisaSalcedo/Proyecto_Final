
import sqlite3
class ProcesaDatos:
    def recupera_datos(self) :
        
        con=sqlite3.connect("data/proyecto_final.db")
        cur =con.cursor()
        cur.execute("""
                        select fecha, hora, divisa, cantidad,tipo_operacion ,cantidad*50
                        from movimientos
                        order by fecha, tipo_operacion
                        """
            )
                        
            
        ''''
        datos = []            
        dato= cur.fetchone()
        while dato:
            dato=list(dato)
           
            dato[4]='Compra' if dato[4] else 'Venta'
           
            datos.append(dato)
            dato=cur.fetchone()
            #hay que cambiar el ultimo campo haciendo la llamada a Apicoin y quietarlo del resultado de la qwery
        
        '''
        return cur.fetchall()
    
    def inserta_datos (self,fecha,hora,divisa,cantidad,tipo_operacion):
        con=sqlite3.connect("data/proyecto_final.db")
        cur =con.cursor()

        cur.execute ("""
                    Insert into movimientos (fecha,hora,divisa,cantidad,tipo_operacion)
                    values (?,?,?,?,?)
                    """ ,( fecha,hora,divisa,cantidad,tipo_operacion))
        
        con.commit()
        con.close()

