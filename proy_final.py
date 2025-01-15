from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import font
import sqlite3
from sqlite3 import Error
from PIL import Image, ImageTk

# ##############################################
# MODELO
# ##############################################

def crear_base():
    con = sqlite3.connect('ventasperroslibres.db')
    return con

def crear_tabla(con):
    cursor = con.cursor()
    sql = "CREATE TABLE IF NOT EXISTS ventas(id integer PRIMARY KEY AUTOINCREMENT, Fecha text, Comprador text, Dirección text, Producto text, Cantidad text, Importe integer, Total integer, Entregado text)"
    cursor.execute(sql)
    con.commit()

def clean():
    blanco=''
    var_fecha.set(blanco)
    var_comprador.set(blanco)
    var_direccion.set(blanco)
    var_producto.set(blanco)
    var_cantidad.set(0)
    var_importe.set(0)
    var_total.set(0)
    var_entregado.set(blanco)
    var_baja.set(0)
    var_modificar.set(0)

def insertar_registro(con, fecha, comprador, dirección, producto, cantidad, importe, total, entregado):
    cursor = con.cursor()
    cantidad = int(cantidad)
    importe = int(importe)
    total = int(total)
    data = (fecha, comprador, dirección, producto, cantidad, importe, total, entregado)
    sql = "INSERT INTO ventas(fecha, comprador, dirección, producto, cantidad, importe, total, entregado) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    con.commit()

def eliminar_registro(con, mi_id):
    cursor = con.cursor()
    mi_id = int(mi_id)
    data = (mi_id, )
    sql = "DELETE FROM ventas WHERE id = ? "
    cursor.execute(sql, data)
    con.commit()

def modificar_registro(con, toma_modificar, toma_fecha,toma_comprador, toma_direccion, toma_producto, toma_cantidad, toma_importe, c, toma_entregado):
    cursor = con.cursor()
    mi_id = int(toma_modificar)
    data = (toma_fecha,toma_comprador, toma_direccion, toma_producto, toma_cantidad, toma_importe, c, toma_entregado, mi_id)
    sql = "UPDATE ventas SET fecha = ?, comprador = ?, dirección = ?, producto = ?, cantidad  = ?, importe  = ?, total = ?, entregado = ? WHERE id = ? "
    cursor.execute(sql, data)
    con.commit()

def alta(tree): 
    toma_fecha=var_fecha.get()
    toma_comprador=var_comprador.get()
    toma_direccion=var_direccion.get()
    toma_producto=var_producto.get()
    toma_cantidad=var_cantidad.get()
    toma_importe=var_importe.get()
    toma_entregado=var_entregado.get()
    c = var_cantidad.get()*var_importe.get()
    var_total.set(c)
    #tree.insert("", "end", text=str(id), values=(toma_fecha,toma_comprador,toma_direccion,toma_producto,toma_cantidad,toma_importe,c,toma_entregado))
     
    #Limpiar campos
    clean()
    #Guardar el registro en la tabla
    insertar_registro(con, toma_fecha, toma_comprador, toma_direccion, toma_producto, toma_cantidad, toma_importe, c, toma_entregado)
    actualizar_treeview(tree,con)


def baja(tree):
    global con
    toma_baja=var_baja.get()
    mensaje= '¿Desea borrar el registro ' + str(toma_baja) + '?'
    mensaje2='Se ha borrado el registro ' + str(toma_baja)
    if askyesno("Consulta de verificación", mensaje):
        eliminar_registro(con, toma_baja)
        showinfo("", mensaje2)
        actualizar_treeview(tree,con)
    else:
        showinfo("", "Regresamos al menú principal")


def modificar(tree):
    toma_fecha=var_fecha.get()
    toma_comprador=var_comprador.get()
    toma_direccion=var_direccion.get()
    toma_producto=var_producto.get()
    toma_cantidad=var_cantidad.get()
    toma_importe=var_importe.get()
    toma_entregado=var_entregado.get()
    toma_modificar=var_modificar.get()
    c = var_cantidad.get()*var_importe.get()
    var_total.set(c)
    mensaje= '¿Desea modificar el registro ' + str(toma_modificar) + '?'
    mensaje2='Se ha modificado el registro ' + str(toma_modificar)
    if askyesno("Consulta de verificación", mensaje):
        modificar_registro(con, toma_modificar, toma_fecha,toma_comprador, toma_direccion, toma_producto, toma_cantidad, toma_importe, c, toma_entregado )
        showinfo("", mensaje2)
        actualizar_treeview(tree,con)
        '''#update treeview
        selected_item = toma_modificar-1
        itemid = tree.get_children()[selected_item]
        new_values=[toma_fecha,toma_comprador, toma_direccion, toma_producto, toma_cantidad, toma_importe, c, toma_entregado]
        tree.item(itemid,values=new_values)
        #update db o dicc
        registro[toma_modificar]={'Codigo': toma_modificar, 'Fecha': toma_fecha, 'Comprador': toma_comprador, 'Direccion': toma_direccion, 'Producto': toma_producto, 'Cantidad': toma_cantidad, 'Total': c, 'Entregado': toma_entregado} 
        print(registro)'''
        showinfo("", mensaje2)
    else:
        showinfo("", "Regresamos al menú principal")

def actualizar_treeview(tree,con):
    records = tree.get_children()
    for element in records:
        tree.delete(element)

    sql = "SELECT * FROM ventas ORDER BY id ASC"
    cursor=con.cursor()
    datos=cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3],fila[4], fila[5], fila[6],fila[7], fila[8]))


# ##############################################
# VISTA 
# ##############################################

master = Tk()

master.title('Planilla de ventas')

photo = PhotoImage(file="backgroundimage.gif")
photo1= PhotoImage(file="fondo.gif")
smaller_image = photo.subsample(1,1)  

background_label = Label(master, image=photo1)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

foto_label = Label(master, image=smaller_image)
foto_label.grid(column=12, rowspan=15, columnspan=4)

fondo ='white'
fondo1="white"
fondo2="#DCC199"
fuente="Calibri"
titulo = font.Font(family='Calibri', size=16)
master.config(bg=fondo1)
master.geometry("1150x360")

#Colocamos labels con sus respectivos entrys a la derecha ubicados en columnas y filas


var_fecha=StringVar()
var_comprador=StringVar()
var_direccion=StringVar()
var_producto=StringVar()
var_cantidad=IntVar()
var_importe=IntVar()
var_total=IntVar()
var_entregado=StringVar()
var_baja=IntVar()
var_modificar=IntVar()

label_titulo = Label(master, text="Bienvenidos a Perros libres", font=titulo, bg=fondo2)
label_titulo.grid(row=0, column=5, columnspan=9)
horizontal_separador=Frame(master, height=20)
horizontal_separador.grid(row=1, column=1)
label_fecha = Label(master, text="Fecha:", font=fuente, bg=fondo)
label_fecha.grid(row=3, column=0, sticky=W)
label_comprador = Label(master, text="Comprador:", font=fuente, bg=fondo)
label_comprador.grid(row=4, column=0, sticky=W)
label_direccion = Label(master, text="Dirección:", font=fuente, bg=fondo)
label_direccion.grid(row=5, column=0, sticky=W)
label_producto = Label(master, text="Producto:", font=fuente, bg=fondo)
label_producto.grid(row=6, column=0, sticky=W)
label_cantidad = Label(master, text="Cantidad:", font=fuente, bg=fondo)
label_cantidad.grid(row=7, column=0, sticky=W)
label_importe = Label(master, text="Importe:", font=fuente, bg=fondo)
label_importe.grid(row=8, column=0, sticky=W)
label_total = Label(master, text="Total:", font=fuente, bg=fondo)
label_total.grid(row=9, column=0, sticky=W)
label_entregado = Label(master, text="Entregado:", font=fuente, bg=fondo)
label_entregado.grid(row=10, column=0, sticky=W)
label_baja = Label(master, text="Código a dar de baja:", font=fuente, bg=fondo)
label_baja.grid(row=10, column=6, sticky=W)
label_modificar = Label(master, text="Código a modificar:", font=fuente, bg=fondo)
label_modificar.grid(row=10, column=9, sticky=W)




entry_fecha = Entry(master, textvariable=var_fecha, font=fuente, bg=fondo1)
entry_fecha.grid(row=3, column=1, sticky=W)
entry_comprador = Entry(master, textvariable=var_comprador, font=fuente, bg=fondo1)
entry_comprador.grid(row=4, column=1, sticky=W)
entry_direccion = Entry(master, textvariable=var_direccion, font=fuente, bg=fondo1)
entry_direccion.grid(row=5, column=1, sticky=W)
entry_producto = Entry(master, textvariable=var_producto, font=fuente, bg=fondo1)
entry_producto.grid(row=6, column=1, sticky=W)
entry_cantidad = Entry(master, textvariable=var_cantidad, font=fuente, bg=fondo1)
entry_cantidad.grid(row=7, column=1, sticky=W)
entry_importe = Entry(master, textvariable=var_importe, font=fuente, bg=fondo1)
entry_importe.grid(row=8, column=1, sticky=W)
entry_total = Entry(master, textvariable=var_total, font=fuente, bg=fondo1)
entry_total.grid(row=9, column=1, sticky=W)
entry_entregado = Entry(master, textvariable=var_entregado, font=fuente, bg=fondo1)
entry_entregado.grid(row=10, column=1, sticky=W)
entry_baja = Entry(master, textvariable=var_baja, font=fuente, bg=fondo1, width=5)
entry_baja.grid(row=10, column=7, sticky=W)
entry_modificar = Entry(master, textvariable=var_modificar, font=fuente, bg=fondo1, width=5)
entry_modificar.grid(row=10, column=10, sticky=W)

#TREE

tree = ttk.Treeview(master)
tree["columns"]=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8" )
tree.column("#0", width=55, minwidth=40, anchor=W)
tree.column("col1", width=60, minwidth=25)
tree.column("col2", width=100, minwidth=25, anchor="center")
tree.column("col3", width=80, minwidth=25)
tree.column("col4", width=65, minwidth=25)
tree.column("col5", width=60, minwidth=25)
tree.column("col6", width=65, minwidth=25)
tree.column("col7", width=60, minwidth=25)
tree.column("col8", width=70, minwidth=25)
tree.heading("#0", text="Código")
tree.heading("col1", text="Fecha")
tree.heading("col2", text="Comprador")
tree.heading("col3", text="Dirección")
tree.heading("col4", text="Producto")
tree.heading("col5", text="Cantidad")
tree.heading("col6", text="Importe")
tree.heading("col7", text="Total")
tree.heading("col8", text="Entregado")

tree.grid(row=3, column=3, rowspan=7, columnspan=9)

# ##############################################
# CONTROL
# ##############################################
#Creamos la base de datos
con = crear_base()
crear_tabla(con)
#Actualizamos treeview
actualizar_treeview(tree,con)
#Agregamos los botones

horizontal_separador=Frame(master, height=20)
horizontal_separador.grid(row=11, column=1)
boton_alta = Button(master, text="Alta", command=lambda: alta(tree), width=15, bg=fondo2)
boton_alta.grid(row=12, column=1)

boton_baja = Button(master, text="Baja", command=lambda: baja(tree), width=15, bg=fondo2)
boton_baja.grid(row=12, column=6)

boton_modificar = Button(master, text="Modificar", command=lambda: modificar(tree), width=15, bg=fondo2)
boton_modificar.grid(row=12, column=9)




master.mainloop()



