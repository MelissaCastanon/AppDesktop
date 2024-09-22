import tkinter as tk
from tkinter import messagebox, ttk
import requests
from datetime import datetime
import uuid

# URL de MockAPI
url = "https://66eb029a55ad32cda47b53b8.mockapi.io/IoTCarStatus"


# Función para enviar datos a la API
def enviar_datos():
    # Obtener datos de los campos de entrada
    status = entry_status.get()
    date = entry_date.get()
    ip_client = entry_ip_client.get()
    name = entry_name.get()

    # Generar automáticamente el ID único
    id_value = str(uuid.uuid4())

    # Validación básica
    if not status or not date or not ip_client or not name:
        messagebox.showerror("Error", "Todos los campos deben ser llenados.")
        return

    # Crear el payload con los datos
    payload = {
        "Status": status,
        "Date": date,
        "ipClient": ip_client,
        "name": name,
        "id": id_value  # Se genera automáticamente el ID
    }

    try:
        # Realizar la solicitud POST
        response = requests.post(url, json=payload)

        # Verificar si el registro fue exitoso
        if response.status_code == 201:
            messagebox.showinfo("Éxito", "Registro insertado correctamente.")
        else:
            messagebox.showerror("Error", f"Error al insertar registro: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


# Función para generar automáticamente la fecha actual
def generar_fecha_actual():
    fecha_actual = datetime.now().isoformat()
    entry_date.delete(0, tk.END)
    entry_date.insert(0, fecha_actual)


# Función para mostrar los últimos 10 registros
def mostrar_ultimos_registros():
    try:
        # Realizar la solicitud GET para obtener todos los registros
        response = requests.get(url)

        if response.status_code == 200:
            registros = response.json()

            # Ordenar los registros por la fecha más reciente
            registros_ordenados = sorted(registros, key=lambda x: x['Date'], reverse=True)

            # Limitar a los últimos 10 registros
            ultimos_registros = registros_ordenados[:10]

            # Crear una nueva ventana para mostrar los registros
            ventana_registros = tk.Toplevel(app)
            ventana_registros.title("Últimos 10 Registros")
            ventana_registros.geometry("600x400")

            # Crear tabla
            tree = ttk.Treeview(ventana_registros, columns=("ID", "Name", "Status", "Date", "IP"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Name", text="Name")
            tree.heading("Status", text="Status")
            tree.heading("Date", text="Date")
            tree.heading("IP", text="IP")

            tree.pack(fill=tk.BOTH, expand=True)

            # Insertar los registros en la tabla
            for registro in ultimos_registros:
                tree.insert("", tk.END, values=(
                registro["id"], registro["name"], registro["Status"], registro["Date"], registro["ipClient"]))

        else:
            messagebox.showerror("Error", f"No se pudieron obtener los registros: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al obtener los registros: {e}")


# Configuración de la aplicación de escritorio
app = tk.Tk()
app.title("Inyectar y Visualizar Registros de MockAPI")
app.geometry("400x400")

# Etiquetas y campos de entrada
label_status = tk.Label(app, text="Status")
label_status.pack(pady=5)
entry_status = tk.Entry(app)
entry_status.pack()

label_date = tk.Label(app, text="Fecha (YYYY-MM-DDTHH:MM:SS)")
label_date.pack(pady=5)
entry_date = tk.Entry(app)
entry_date.pack()

# Botón para generar automáticamente la fecha actual
btn_fecha_actual = tk.Button(app, text="Generar Fecha Actual", command=generar_fecha_actual)
btn_fecha_actual.pack(pady=5)

label_ip_client = tk.Label(app, text="IP del Cliente")
label_ip_client.pack(pady=5)
entry_ip_client = tk.Entry(app)
entry_ip_client.pack()

label_name = tk.Label(app, text="Nombre")
label_name.pack(pady=5)
entry_name = tk.Entry(app)
entry_name.pack()

# Botón para enviar los datos
btn_enviar = tk.Button(app, text="Enviar Registro", command=enviar_datos)
btn_enviar.pack(pady=20)

# Botón para mostrar los últimos 10 registros
btn_mostrar_registros = tk.Button(app, text="Últimos 10 Registros", command=mostrar_ultimos_registros)
btn_mostrar_registros.pack(pady=10)

# Ejecutar la aplicación
app.mainloop()
