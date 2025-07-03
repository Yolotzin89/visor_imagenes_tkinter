import tkinter as tk 
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageOps
import os

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visor de Imágenes")
        self.root.geometry("800x600")
        
        # Variables
        self.image_folder = ""
        self.image_list = []
        self.current_image = 0
        
        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para mostrar la imagen
        self.canvas = tk.Canvas(self.main_frame, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Frame para controles (botones)
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones
        self.btn_open = tk.Button(self.control_frame, text="Abrir Carpeta", command=self.open_folder)
        self.btn_prev = tk.Button(self.control_frame, text="Anterior", command=self.prev_image)
        self.btn_next = tk.Button(self.control_frame, text="Siguiente", command=self.next_image)
        
        # Efectos
        self.btn_bw = tk.Button(self.control_frame, text="Blanco/Negro", command=self.apply_black_white)
        self.btn_blur = tk.Button(self.control_frame, text="Desenfocar", command=self.apply_blur)
        self.btn_rotate = tk.Button(self.control_frame, text="Rotar 90°", command=self.rotate_image)
        
        # Posicionar botones
        self.btn_open.pack(side=tk.LEFT, padx=5)
        self.btn_prev.pack(side=tk.LEFT, padx=5)
        self.btn_next.pack(side=tk.LEFT, padx=5)
        self.btn_bw.pack(side=tk.LEFT, padx=5)
        self.btn_blur.pack(side=tk.LEFT, padx=5)
        self.btn_rotate.pack(side=tk.LEFT, padx=5)

    def open_folder(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta de imágenes")
        if folder:
            self.image_folder = folder
            self.image_list = [
                f for f in os.listdir(folder) 
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff"))
            ]
        if not self.image_list:
            messagebox.showerror("Error", "No hay imágenes en la carpeta seleccionada.")
            return
        self.current_image = 0
        self.load_image()





    def load_image(self):
        if not self.image_list:
            return
        
        image_path = os.path.join(self.image_folder, self.image_list[self.current_image])
        self.original_image = Image.open(image_path)
        self.display_image = ImageTk.PhotoImage(self.original_image)
        
        # Ajustar tamaño del canvas
        self.canvas.config(width=self.display_image.width(), height=self.display_image.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)
        
        # Actualizar título de la ventana
        self.root.title(f"Visor de Imágenes - {self.image_list[self.current_image]}")

    


    def next_image(self):
        if not self.image_list:
            return
        self.current_image = (self.current_image + 1) % len(self.image_list)
        self.load_image()

    def prev_image(self):
        if not self.image_list:
            return
        self.current_image = (self.current_image - 1) % len(self.image_list)
        self.load_image()


    def apply_black_white(self):
        if not self.image_list:
            return
        bw_image = ImageOps.grayscale(self.original_image)
        self.display_image = ImageTk.PhotoImage(bw_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)

    def apply_blur(self):
        if not self.image_list:
            return
        blur_image = self.original_image.filter(ImageFilter.BLUR)
        self.display_image = ImageTk.PhotoImage(blur_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)

    def rotate_image(self):
        if not self.image_list:
            return
        rotated_image = self.original_image.rotate(90, expand=True)
        self.display_image = ImageTk.PhotoImage(rotated_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)
        self.original_image = rotated_image  # Guardar cambios


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()