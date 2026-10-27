
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# COLORES DE PINKY PAPER
ROSA = "#F6C8D8"
ROSA_OSCURO = "#D98EAD"
AMARILLO = "#FFF0B3"
CREMA = "#FFF9F3"
BLANCO = "#FFFFFF"
TEXTO = "#594653"
VERDE = "#D9EAD3"

# DATOS EN MEMORIA
productos = []
clientes = []
ventas = []
carrito = []
usuario_actual = ""

# VENTANA PRINCIPAL
ventana = tk.Tk()
ventana.title("Pinky Paper - Sistema de ventas")
ventana.geometry("1050x680")
ventana.minsize(900, 600)
ventana.configure(bg=CREMA)

estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure(
    "Treeview",
    background=BLANCO,
    fieldbackground=BLANCO,
    foreground=TEXTO,
    rowheight=27
)
estilo.configure(
    "Treeview.Heading",
    background=ROSA,
    foreground=TEXTO,
    font=("Arial", 10, "bold")
)

# ENCABEZADO
encabezado = tk.Frame(ventana, bg=ROSA, height=85)
encabezado.pack(fill="x")
encabezado.pack_propagate(False)

tk.Label(
    encabezado,
    text="Pinky Paper",
    font=("Arial", 25, "bold"),
    bg=ROSA,
    fg=TEXTO
).pack(pady=(10, 0))

tk.Label(
    encabezado,
    text="Papeleria y detalles bonitos",
    font=("Arial", 10),
    bg=ROSA,
    fg=TEXTO
).pack()

# CUERPO PRINCIPAL
cuerpo = tk.Frame(ventana, bg=CREMA)
cuerpo.pack(fill="both", expand=True)

menu = tk.Frame(cuerpo, bg=AMARILLO, width=180)
menu.pack(side="left", fill="y")
menu.pack_propagate(False)

contenido = tk.Frame(cuerpo, bg=CREMA)
contenido.pack(side="left", fill="both", expand=True, padx=15, pady=15)


def limpiar_contenido():
    for widget in contenido.winfo_children():
        widget.destroy()


def titulo_pagina(texto):
    tk.Label(
        contenido,
        text=texto,
        font=("Arial", 20, "bold"),
        bg=CREMA,
        fg=TEXTO
    ).pack(anchor="w", pady=(0, 15))


def crear_etiqueta(parent, texto):
    return tk.Label(
        parent,
        text=texto,
        bg=CREMA,
        fg=TEXTO,
        font=("Arial", 10)
    )


# INICIO
def mostrar_inicio():
    limpiar_contenido()
    titulo_pagina("Bienvenida")

    tk.Label(
        contenido,
        text="Bienvenida a Pinky Paper",
        font=("Arial", 22, "bold"),
        bg=CREMA,
        fg=ROSA_OSCURO
    ).pack(anchor="w", pady=10)

    tk.Label(
        contenido,
        text="Administra tus productos, clientes y ventas\n"
             "desde un solo lugar.",
        font=("Arial", 13),
        bg=CREMA,
        fg=TEXTO,
        justify="left"
    ).pack(anchor="w", pady=5)

    resumen = tk.Frame(contenido, bg=CREMA)
    resumen.pack(fill="x", pady=25)

    datos = [
        ("Productos registrados", lambda: len(productos)),
        ("Clientes registrados", lambda: len(clientes)),
        ("Ventas realizadas", lambda: len(ventas))
    ]

    for texto, obtener in datos:
        color = ROSA if texto != "Clientes registrados" else AMARILLO
        tarjeta = tk.Frame(
            resumen, bg=color, padx=15, pady=20
        )
        tarjeta.pack(side="left", fill="x", expand=True, padx=5)

        tk.Label(
            tarjeta, text=texto, bg=color, fg=TEXTO,
            font=("Arial", 10)
        ).pack()

        tk.Label(
            tarjeta, text=str(obtener()), bg=color, fg=TEXTO,
            font=("Arial", 22, "bold")
        ).pack(pady=5)

    tk.Label(
        contenido,
        text="Selecciona una opcion del menu para comenzar.",
        bg=CREMA, fg=TEXTO, font=("Arial", 11)
    ).pack(anchor="w", pady=10)


# PRODUCTOS
def mostrar_productos():
    limpiar_contenido()
    titulo_pagina("Administracion de productos")

    formulario = tk.Frame(contenido, bg=CREMA)
    formulario.pack(fill="x", pady=5)

    crear_etiqueta(formulario, "Codigo:").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    entrada_codigo = tk.Entry(formulario, width=18)
    entrada_codigo.grid(row=0, column=1, padx=5, pady=5)

    crear_etiqueta(formulario, "Nombre:").grid(
        row=0, column=2, sticky="w", padx=5, pady=5
    )
    entrada_nombre = tk.Entry(formulario, width=22)
    entrada_nombre.grid(row=0, column=3, padx=5, pady=5)

    crear_etiqueta(formulario, "Precio:").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )
    entrada_precio = tk.Entry(formulario, width=18)
    entrada_precio.grid(row=1, column=1, padx=5, pady=5)

    crear_etiqueta(formulario, "Existencias:").grid(
        row=1, column=2, sticky="w", padx=5, pady=5
    )
    entrada_stock = tk.Entry(formulario, width=22)
    entrada_stock.grid(row=1, column=3, padx=5, pady=5)

    tabla = ttk.Treeview(
        contenido,
        columns=("codigo", "nombre", "precio", "stock"),
        show="headings",
        height=13
    )

    for columna, texto in [
        ("codigo", "Codigo"),
        ("nombre", "Producto"),
        ("precio", "Precio"),
        ("stock", "Existencias")
    ]:
        tabla.heading(columna, text=texto)

    tabla.column("codigo", width=100)
    tabla.column("nombre", width=250)
    tabla.column("precio", width=120)
    tabla.column("stock", width=120)
    tabla.pack(fill="both", expand=True, pady=15)

    def actualizar_tabla():
        for fila in tabla.get_children():
            tabla.delete(fila)

        for producto in productos:
            tabla.insert(
                "", "end",
                values=(
                    producto["codigo"],
                    producto["nombre"],
                    f'${producto["precio"]:.2f}',
                    producto["stock"]
                )
            )

    def registrar_producto():
        codigo = entrada_codigo.get().strip()
        nombre = entrada_nombre.get().strip()

        if not codigo or not nombre:
            messagebox.showwarning(
                "Datos incompletos",
                "Escribe el codigo y el nombre del producto."
            )
            return

        try:
            precio = float(entrada_precio.get())
            stock = int(entrada_stock.get())

            if precio <= 0 or stock < 0:
                messagebox.showwarning(
                    "Datos incorrectos",
                    "El precio debe ser mayor a cero y las existencias no pueden ser negativas."
                )
                return

            if any(p["codigo"] == codigo for p in productos):
                messagebox.showwarning(
                    "Codigo repetido",
                    "Ese codigo ya existe. Escribe otro."
                )
                return

            productos.append({
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "stock": stock
            })

            actualizar_tabla()

            for entrada in (
                entrada_codigo, entrada_nombre,
                entrada_precio, entrada_stock
            ):
                entrada.delete(0, tk.END)

            messagebox.showinfo(
                "Producto registrado",
                "El producto se registro correctamente."
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Escribe un precio valido y las existencias en numeros enteros."
            )

    tk.Button(
        formulario,
        text="Registrar producto",
        command=registrar_producto,
        bg=ROSA, fg=TEXTO, relief="flat",
        font=("Arial", 10, "bold"), padx=10, pady=7
    ).grid(row=2, column=0, columnspan=2, pady=10)

    actualizar_tabla()


# CLIENTES
def mostrar_clientes():
    limpiar_contenido()
    titulo_pagina("Registro de clientes")

    formulario = tk.Frame(contenido, bg=CREMA)
    formulario.pack(fill="x", pady=5)

    crear_etiqueta(formulario, "Nombre:").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    entrada_nombre = tk.Entry(formulario, width=25)
    entrada_nombre.grid(row=0, column=1, padx=5, pady=5)

    crear_etiqueta(formulario, "Telefono:").grid(
        row=0, column=2, sticky="w", padx=5, pady=5
    )
    entrada_telefono = tk.Entry(formulario, width=22)
    entrada_telefono.grid(row=0, column=3, padx=5, pady=5)

    crear_etiqueta(formulario, "Correo:").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )
    entrada_correo = tk.Entry(formulario, width=25)
    entrada_correo.grid(row=1, column=1, padx=5, pady=5)

    tabla = ttk.Treeview(
        contenido,
        columns=("nombre", "telefono", "correo"),
        show="headings",
        height=13
    )

    for columna, texto in [
        ("nombre", "Nombre"),
        ("telefono", "Telefono"),
        ("correo", "Correo electronico")
    ]:
        tabla.heading(columna, text=texto)

    tabla.column("nombre", width=220)
    tabla.column("telefono", width=150)
    tabla.column("correo", width=250)
    tabla.pack(fill="both", expand=True, pady=15)

    def actualizar_tabla():
        for fila in tabla.get_children():
            tabla.delete(fila)

        for cliente in clientes:
            tabla.insert(
                "", "end",
                values=(
                    cliente["nombre"],
                    cliente["telefono"],
                    cliente["correo"]
                )
            )

    def registrar_cliente():
        nombre = entrada_nombre.get().strip()
        telefono = entrada_telefono.get().strip()
        correo = entrada_correo.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Falta el nombre",
                "Escribe el nombre del cliente."
            )
            return

        clientes.append({
            "nombre": nombre,
            "telefono": telefono,
            "correo": correo
        })

        actualizar_tabla()

        entrada_nombre.delete(0, tk.END)
        entrada_telefono.delete(0, tk.END)
        entrada_correo.delete(0, tk.END)

        messagebox.showinfo(
            "Cliente registrado",
            "El cliente se registro correctamente."
        )

    tk.Button(
        formulario,
        text="Registrar cliente",
        command=registrar_cliente,
        bg=ROSA, fg=TEXTO, relief="flat",
        font=("Arial", 10, "bold"), padx=10, pady=7
    ).grid(row=2, column=0, columnspan=2, pady=10)

    actualizar_tabla()


# VENTAS
def mostrar_ventas():
    global carrito

    limpiar_contenido()
    carrito = []
    titulo_pagina("Registro de ventas")

    if not productos:
        tk.Label(
            contenido,
            text="Primero registra productos en la seccion Productos.",
            bg=CREMA, fg=TEXTO, font=("Arial", 12)
        ).pack(anchor="w")
        return

    formulario = tk.Frame(contenido, bg=CREMA)
    formulario.pack(fill="x", pady=5)

    crear_etiqueta(formulario, "Cliente:").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )

    combo_cliente = ttk.Combobox(
        formulario,
        values=[c["nombre"] for c in clientes],
        state="readonly",
        width=28
    )
    combo_cliente.grid(row=0, column=1, padx=5, pady=5)

    crear_etiqueta(formulario, "Codigo de producto:").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )

    combo_producto = ttk.Combobox(
        formulario,
        values=[p["codigo"] for p in productos],
        state="readonly",
        width=28
    )
    combo_producto.grid(row=1, column=1, padx=5, pady=5)

    crear_etiqueta(formulario, "Cantidad:").grid(
        row=2, column=0, sticky="w", padx=5, pady=5
    )

    entrada_cantidad = tk.Entry(formulario, width=12)
    entrada_cantidad.grid(row=2, column=1, sticky="w", padx=5, pady=5)
    entrada_cantidad.insert(0, "1")

    tabla = ttk.Treeview(
        contenido,
        columns=("codigo", "producto", "cantidad", "precio", "importe"),
        show="headings",
        height=9
    )

    encabezados = {
        "codigo": "Codigo",
        "producto": "Producto",
        "cantidad": "Cantidad",
        "precio": "Precio unitario",
        "importe": "Importe"
    }

    for columna, texto in encabezados.items():
        tabla.heading(columna, text=texto)

    tabla.column("codigo", width=80)
    tabla.column("producto", width=190)
    tabla.column("cantidad", width=80)
    tabla.column("precio", width=110)
    tabla.column("importe", width=110)
    tabla.pack(fill="both", expand=True, pady=12)

    resumen = tk.Label(
        contenido,
        text="Subtotal: $0.00    Total: $0.00",
        bg=AMARILLO, fg=TEXTO,
        font=("Arial", 13, "bold"), pady=10
    )
    resumen.pack(fill="x", pady=5)

    def actualizar_resumen():
        subtotal = sum(
            item["cantidad"] * item["precio"] for item in carrito
        )
        resumen.config(
            text=f"Subtotal: ${subtotal:.2f}    Total: ${subtotal:.2f}"
        )

    def actualizar_tabla():
        for fila in tabla.get_children():
            tabla.delete(fila)

        for item in carrito:
            importe = item["cantidad"] * item["precio"]
            tabla.insert(
                "", "end",
                values=(
                    item["codigo"],
                    item["nombre"],
                    item["cantidad"],
                    f'${item["precio"]:.2f}',
                    f'${importe:.2f}'
                )
            )

    def agregar_producto():
        codigo = combo_producto.get()

        if not codigo:
            messagebox.showwarning(
                "Selecciona un producto",
                "Elige un codigo de producto."
            )
            return

        try:
            cantidad = int(entrada_cantidad.get())

            if cantidad <= 0:
                messagebox.showwarning(
                    "Cantidad incorrecta",
                    "La cantidad debe ser mayor que cero."
                )
                return
        except ValueError:
            messagebox.showerror(
                "Cantidad incorrecta",
                "Escribe una cantidad entera."
            )
            return

        producto = next(
            (p for p in productos if p["codigo"] == codigo), None
        )

        if producto is None:
            messagebox.showerror("Error", "No se encontro el producto.")
            return

        cantidad_actual = sum(
            item["cantidad"] for item in carrito
            if item["codigo"] == codigo
        )

        if cantidad_actual + cantidad > producto["stock"]:
            messagebox.showwarning(
                "Existencias insuficientes",
                f"Solo hay {producto['stock']} unidades de {producto['nombre']}."
            )
            return

        item_existente = next(
            (item for item in carrito if item["codigo"] == codigo), None
        )

        if item_existente:
            item_existente["cantidad"] += cantidad
        else:
            carrito.append({
                "codigo": producto["codigo"],
                "nombre": producto["nombre"],
                "precio": producto["precio"],
                "cantidad": cantidad
            })

        actualizar_tabla()
        actualizar_resumen()
        entrada_cantidad.delete(0, tk.END)
        entrada_cantidad.insert(0, "1")

    def finalizar_venta():
        if not carrito:
            messagebox.showwarning(
                "Venta vacia",
                "Agrega al menos un producto."
            )
            return

        nombre_cliente = combo_cliente.get()

        if not nombre_cliente:
            messagebox.showwarning(
                "Selecciona un cliente",
                "Selecciona un cliente registrado antes de finalizar."
            )
            return

        for item in carrito:
            producto = next(
                p for p in productos if p["codigo"] == item["codigo"]
            )
            if item["cantidad"] > producto["stock"]:
                messagebox.showerror(
                    "Existencias insuficientes",
                    f"No hay suficientes unidades de {item['nombre']}."
                )
                return

        lineas = [item.copy() for item in carrito]
        subtotal = sum(
            item["cantidad"] * item["precio"] for item in lineas
        )
        total = subtotal

        for item in lineas:
            producto = next(
                p for p in productos if p["codigo"] == item["codigo"]
            )
            producto["stock"] -= item["cantidad"]

        venta = {
            "folio": len(ventas) + 1,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "cliente": nombre_cliente,
            "productos": lineas,
            "subtotal": subtotal,
            "total": total
        }

        ventas.append(venta)
        mostrar_ticket(venta)

        messagebox.showinfo(
            "Venta registrada",
            f"Venta registrada correctamente.\nTotal: ${total:.2f}"
        )

        mostrar_ventas()

    tk.Button(
        formulario,
        text="Agregar producto",
        command=agregar_producto,
        bg=ROSA, fg=TEXTO, relief="flat",
        font=("Arial", 10, "bold"), padx=10, pady=7
    ).grid(row=1, column=2, padx=10, pady=5)

    tk.Button(
        contenido,
        text="Finalizar venta y generar ticket",
        command=finalizar_venta,
        bg=ROSA_OSCURO, fg=BLANCO, relief="flat",
        font=("Arial", 11, "bold"), padx=12, pady=10
    ).pack(pady=8)


# TICKETS
def mostrar_ticket(venta):
    ventana_ticket = tk.Toplevel(ventana)
    ventana_ticket.title(f"Ticket - Venta {venta['folio']}")
    ventana_ticket.geometry("470x550")
    ventana_ticket.configure(bg=BLANCO)

    area = tk.Text(
        ventana_ticket,
        font=("Courier New", 10),
        bg=BLANCO,
        fg="#333333",
        wrap="none"
    )
    area.pack(fill="both", expand=True, padx=12, pady=12)

    area.insert(tk.END, "             PINKY PAPER\n")
    area.insert(tk.END, "       Papeleria y detalles bonitos\n")
    area.insert(tk.END, "-" * 40 + "\n")
    area.insert(tk.END, f"Ticket: {venta['folio']}\n")
    area.insert(tk.END, f"Fecha: {venta['fecha']}\n")
    area.insert(tk.END, f"Cliente: {venta['cliente']}\n")
    area.insert(tk.END, "-" * 40 + "\n")
    area.insert(tk.END, "Producto        Cant.  Precio  Importe\n")
    area.insert(tk.END, "-" * 40 + "\n")

    for item in venta["productos"]:
        nombre = item["nombre"][:15]
        cantidad = item["cantidad"]
        precio = item["precio"]
        importe = cantidad * precio

        area.insert(
            tk.END,
            f"{nombre:<15} {cantidad:>4} ${precio:>6.2f} ${importe:>7.2f}\n"
        )

    area.insert(tk.END, "-" * 40 + "\n")
    area.insert(tk.END, f"Subtotal:              ${venta['subtotal']:.2f}\n")
    area.insert(tk.END, f"TOTAL:                 ${venta['total']:.2f}\n")
    area.insert(tk.END, "-" * 40 + "\n")
    area.insert(tk.END, "Gracias por comprar en Pinky Paper\n")
    area.config(state="disabled")


def mostrar_tickets():
    limpiar_contenido()
    titulo_pagina("Historial de tickets")

    if not ventas:
        tk.Label(
            contenido,
            text="Todavia no se han registrado ventas.",
            bg=CREMA, fg=TEXTO, font=("Arial", 12)
        ).pack(anchor="w")
        return

    tabla = ttk.Treeview(
        contenido,
        columns=("folio", "fecha", "cliente", "total"),
        show="headings",
        height=15
    )

    for columna, texto in [
        ("folio", "Folio"),
        ("fecha", "Fecha"),
        ("cliente", "Cliente"),
        ("total", "Total")
    ]:
        tabla.heading(columna, text=texto)

    tabla.column("folio", width=70)
    tabla.column("fecha", width=150)
    tabla.column("cliente", width=220)
    tabla.column("total", width=120)
    tabla.pack(fill="both", expand=True, pady=10)

    for venta in ventas:
        tabla.insert(
            "", "end",
            values=(
                venta["folio"],
                venta["fecha"],
                venta["cliente"],
                f'${venta["total"]:.2f}'
            )
        )

    def abrir_ticket():
        seleccion = tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Selecciona una venta",
                "Selecciona un ticket de la tabla."
            )
            return

        folio = tabla.item(seleccion[0], "values")[0]
        venta = next(
            v for v in ventas if str(v["folio"]) == str(folio)
        )
        mostrar_ticket(venta)

    tk.Button(
        contenido,
        text="Ver ticket seleccionado",
        command=abrir_ticket,
        bg=ROSA, fg=TEXTO, relief="flat",
        font=("Arial", 10, "bold"), padx=12, pady=8
    ).pack(pady=8)


# INICIO DE SESION
def iniciar_sesion():
    global usuario_actual

    usuario = entrada_usuario.get().strip()
    contrasena = entrada_contrasena.get()
    rol = combo_rol.get()

    if not usuario or not contrasena:
        messagebox.showwarning(
            "Datos incompletos",
            "Escribe el usuario y la contrasena."
        )
        return

    cuentas = {
        "admin": {"contrasena": "1234", "rol": "Administrador"},
        "vendedor": {"contrasena": "1234", "rol": "Vendedor"}
    }

    if usuario not in cuentas:
        messagebox.showerror("Acceso denegado", "El usuario no existe.")
        return

    cuenta = cuentas[usuario]

    if contrasena != cuenta["contrasena"] or rol != cuenta["rol"]:
        messagebox.showerror(
            "Acceso denegado",
            "Usuario, contrasena o rol incorrectos."
        )
        return

    usuario_actual = usuario
    ventana_login.destroy()
    ventana.deiconify()

    btn_productos.config(state="disabled" if rol == "Vendedor" else "normal")
    btn_clientes.config(state="normal")
    btn_ventas.config(state="normal")
    btn_tickets.config(state="normal")

    mostrar_inicio()


def cerrar_sesion():
    respuesta = messagebox.askyesno(
        "Cerrar sesion",
        "Quieres cerrar la sesion actual?"
    )
    if respuesta:
        ventana.destroy()


# MENU LATERAL
btn_inicio = tk.Button(
    menu, text="Inicio", command=mostrar_inicio,
    font=("Arial", 11, "bold"), bg=AMARILLO, fg=TEXTO,
    relief="flat", cursor="hand2", width=17, pady=12
)
btn_inicio.pack(pady=3, padx=5)

btn_productos = tk.Button(
    menu, text="Productos", command=mostrar_productos,
    font=("Arial", 11, "bold"), bg=AMARILLO, fg=TEXTO,
    relief="flat", cursor="hand2", width=17, pady=12
)
btn_productos.pack(pady=3, padx=5)

btn_clientes = tk.Button(
    menu, text="Clientes", command=mostrar_clientes,
    font=("Arial", 11, "bold"), bg=AMARILLO, fg=TEXTO,
    relief="flat", cursor="hand2", width=17, pady=12
)
btn_clientes.pack(pady=3, padx=5)

btn_ventas = tk.Button(
    menu, text="Ventas", command=mostrar_ventas,
    font=("Arial", 11, "bold"), bg=AMARILLO, fg=TEXTO,
    relief="flat", cursor="hand2", width=17, pady=12
)
btn_ventas.pack(pady=3, padx=5)

btn_tickets = tk.Button(
    menu, text="Tickets", command=mostrar_tickets,
    font=("Arial", 11, "bold"), bg=AMARILLO, fg=TEXTO,
    relief="flat", cursor="hand2", width=17, pady=12
)
btn_tickets.pack(pady=3, padx=5)

tk.Button(
    menu, text="Cerrar sesion", command=cerrar_sesion,
    font=("Arial", 10), bg=ROSA, fg=TEXTO,
    relief="flat", cursor="hand2", width=17, pady=9
).pack(side="bottom", pady=12, padx=5)

# PANTALLA DE INICIO DE SESION
ventana.withdraw()

ventana_login = tk.Toplevel(ventana)
ventana_login.title("Acceso - Pinky Paper")
ventana_login.geometry("390x360")
ventana_login.configure(bg=CREMA)
ventana_login.resizable(False, False)

tk.Label(
    ventana_login, text="Pinky Paper",
    font=("Arial", 25, "bold"), bg=ROSA,
    fg=TEXTO, pady=15
).pack(fill="x")

tk.Label(
    ventana_login, text="Inicio de sesion",
    font=("Arial", 15, "bold"), bg=CREMA, fg=TEXTO
).pack(pady=(18, 8))

tk.Label(
    ventana_login, text="Usuario", bg=CREMA, fg=TEXTO
).pack()

entrada_usuario = tk.Entry(ventana_login, width=28)
entrada_usuario.pack(pady=4)
entrada_usuario.insert(0, "admin")

tk.Label(
    ventana_login, text="Contrasena", bg=CREMA, fg=TEXTO
).pack()

entrada_contrasena = tk.Entry(
    ventana_login, width=28, show="*"
)
entrada_contrasena.pack(pady=4)
entrada_contrasena.insert(0, "1234")

tk.Label(
    ventana_login, text="Rol", bg=CREMA, fg=TEXTO
).pack()

combo_rol = ttk.Combobox(
    ventana_login,
    values=["Administrador", "Vendedor"],
    state="readonly",
    width=25
)
combo_rol.pack(pady=4)
combo_rol.set("Administrador")

tk.Button(
    ventana_login, text="Entrar",
    command=iniciar_sesion, bg=ROSA, fg=TEXTO,
    font=("Arial", 11, "bold"), relief="flat",
    padx=25, pady=7
).pack(pady=12)

ventana_login.protocol("WM_DELETE_WINDOW", ventana.destroy)

ventana.mainloop()
