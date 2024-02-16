import tkinter as tk
from tkinter import ttk
import pandas as pd
import re

class InicioSesion:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        
        ttk.Label(self.root, text="Usuario:").pack()
        self.entry_usuario = ttk.Entry(self.root)
        self.entry_usuario.pack()
        
        ttk.Label(self.root, text="Contraseña:").pack()
        self.entry_contrasena = ttk.Entry(self.root, show="*")
        self.entry_contrasena.pack()
        
        ttk.Button(self.root, text="Iniciar sesión", command=self.verificar_credenciales).pack()
        
    def verificar_credenciales(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        
        if usuario == "UliGaMi" and contrasena == "@Ulises123":
            self.root.destroy()  
            self.mostrar_buscador()
        else:
            ttk.Label(self.root, text="Credenciales incorrectas. Inténtalo de nuevo.").pack()
            self.entry_usuario.delete(0, tk.END)
            self.entry_contrasena.delete(0, tk.END)
        
    def mostrar_buscador(self):
        root = tk.Tk()
        app = Buscador(root)
        root.mainloop()


class Buscador:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscador")
        
        self.nuevos_encabezados = ['clave', 'nombre', 'correo', 'telefono']
        self.df = pd.read_excel('datospersonales.xlsx', names=self.nuevos_encabezados)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.columna_seleccionada = tk.StringVar()
        for columna in self.nuevos_encabezados:
            ttk.Radiobutton(self.root, text=columna, variable=self.columna_seleccionada, value=columna).pack()
        
        ttk.Label(self.root, text="Cadena a buscar:").pack()
        self.entry_busqueda = ttk.Entry(self.root)
        self.entry_busqueda.pack()
        
        self.mostrar_info = {columna: tk.BooleanVar() for columna in self.nuevos_encabezados}
        for columna, var in self.mostrar_info.items():
            ttk.Checkbutton(self.root, text=columna, variable=var).pack()
        
        ttk.Button(self.root, text="Buscar", command=self.buscar).pack()
        
        self.resultado_listbox = tk.Listbox(self.root, height=10, width=50)
        self.resultado_listbox.pack()
        
    def buscar(self):
        patron = self.entry_busqueda.get()
        columna = self.columna_seleccionada.get()
        
        self.resultado_listbox.delete(0, tk.END)
        
        if not patron or not columna:
            self.resultado_listbox.insert(tk.END, "Por favor ingresa un patrón de búsqueda y selecciona una columna.")
            return
        
        resultados = self.df[self.df[columna].apply(lambda x: bool(re.search(patron.lower(), str(x).lower())))]
        contador = 1
        for index, row in resultados.iterrows():
            info_mostrar = []
            for columna, var in self.mostrar_info.items():
                if var.get():
                    info_mostrar.append(f"{columna}: {row[columna]}")
            self.resultado_listbox.insert(tk.END, f"{contador}. "+", ".join(info_mostrar))
            contador += 1


if __name__ == "__main__":
    root = tk.Tk()
    app = InicioSesion(root)
    root.mainloop()


