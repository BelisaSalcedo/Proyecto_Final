import sqlite3
con=sqlite3.connect('proyecto_final.bd')
cur=con.cursor()
cur.execute("select fecha, hora, divisa, cantidad, tipo_operacion from movimientos")