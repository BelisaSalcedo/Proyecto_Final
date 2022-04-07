import sqlite3
con=sqlite3.connect("data/proyecto_final.db")
cur =con.cursor()
cur.execute("""
                        select  divisa, sum(cantidad)
                        from movimientos
                        where tipo_operacion='1' and divisa=divisa)
                        """
            )       
sum=cur.fetchall
con.close()
con=sqlite3.connect("data/proyecto_final.db")
cur =con.cursor()
cur.execute("""
                        select  divisa, sum(cantidad)*(-1)
                        from movimientos
                        where tipo_operacion='0' and divisa=divisa)
                        """
            )       
resta=cur.fetchall
        

print( sum-resta)