import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import json

API_URL = "http://localhost:5000/data"

class DataSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Sender App")
        self.root.geometry("400x250")

        # Tipo de datos
        self.label_type = tk.Label(root, text="Seleccione el tipo de datos:")
        self.label_type.pack(pady=5)

        self.data_type = tk.StringVar()
        self.data_type.set("temperatura")
        self.dropdown = tk.OptionMenu(root, self.data_type, "temperatura", "saturacion_oxigeno", "posicion", "heart_rate", "binarios")
        self.dropdown.pack(pady=5)

        # Archivo JSON
        self.label_file = tk.Label(root, text="Seleccione el archivo JSON:")
        self.label_file.pack(pady=5)

        self.file_path = tk.Entry(root, width=40)
        self.file_path.pack(pady=5)

        self.browse_button = tk.Button(root, text="Examinar", command=self.browse_file)
        self.browse_button.pack(pady=5)

        # Botón para enviar
        self.send_button = tk.Button(root, text="Enviar Datos", command=self.send_data)
        self.send_button.pack(pady=10)

        # Resultado
        self.result_label = tk.Label(root, text="Resultado: ")
        self.result_label.pack(pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.file_path.delete(0, tk.END)
            self.file_path.insert(0, file_path)

    def send_data(self):
        data_type = self.data_type.get()
        file_path = self.file_path.get()

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            response = requests.post(f"{API_URL}?type={data_type}", json=data)
            if response.status_code == 200:
                message = f"Datos insertados correctamente: {response.json()['message']}"
            else:
                message = f"Error al insertar datos: {response.json().get('error', 'Error desconocido')}"
            self.result_label.config(text=f"Resultado: {message}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = DataSenderApp(root)
    root.mainloop()
