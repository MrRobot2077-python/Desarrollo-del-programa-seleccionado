import tkinter as tk
from PIL import Image, ImageTk
import random
import pygame
import os

class JuegoMemoria:
    def __init__(self, master):
        self.master = master
        self.master.title("Matheo Juego de Memoria")
        self.master.geometry("400x400")
        base_path = os.path.dirname(os.path.abspath(__file__))  # Ruta base del directorio actual
        self.dorso_archivo = os.path.join(base_path, "images/img9.jpg")
        self.imagenes_archivos = [
            os.path.join(base_path, "images/img1.jpg"),
            os.path.join(base_path, "images/img2.jpg"),
            os.path.join(base_path, "images/img3.jpg"),
            os.path.join(base_path, "images/img4.jpg"),
            os.path.join(base_path, "images/img5.jpg"),
            os.path.join(base_path, "images/img6.jpg"),
            os.path.join(base_path, "images/img7.jpg"),
            os.path.join(base_path, "images/img8.jpg")
        ]
        self.imagenes_archivos *= 2
        random.shuffle(self.imagenes_archivos)
        self.imagen_objs = []
        self.dorso_img = None
        self.botones = []
        self.primer_click = None
        self.cargar_imagenes()
        self.crear_tablero()

        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(base_path, "musica de fondo.mp3"))
        pygame.mixer.music.play(-1)

        self.sonido_win = pygame.mixer.Sound(os.path.join(base_path, "win.mp3"))

    def cargar_imagenes(self):
        for archivo in self.imagenes_archivos:
            img = Image.open(archivo)
            img = img.resize((80, 80), Image.LANCZOS)
            self.imagen_objs.append(ImageTk.PhotoImage(img))
        
        dorso = Image.open(self.dorso_archivo)
        dorso = dorso.resize((80, 80), Image.LANCZOS)
        self.dorso_img = ImageTk.PhotoImage(dorso)

    def crear_tablero(self):
        for i in range(4):
            fila = []
            for j in range(4):
                boton = tk.Button(self.master, width=100, height=100, image=self.dorso_img, command=lambda i=i, j=j: self.voltear_tarjeta(i, j))
                boton.grid(row=i, column=j)
                fila.append(boton)
            self.botones.append(fila)

    def voltear_tarjeta(self, i, j):
        boton = self.botones[i][j]
        indice = i * 4 + j
        if boton.cget('image') == str(self.dorso_img):
            boton.config(image=self.imagen_objs[indice])
            boton.image_ref = self.imagen_objs[indice]
            if self.primer_click is None:
                self.primer_click = (i, j)
            else:
                self.master.after(1000, self.verificar_emparejamiento, i, j)

    def verificar_emparejamiento(self, i, j):
        if self.primer_click is None:
            return
        i1, j1 = self.primer_click
        indice1 = i1 * 4 + j1
        indice2 = i * 4 + j
        if self.imagenes_archivos[indice1] == self.imagenes_archivos[indice2]:
            self.botones[i1][j1]["state"] = "disabled"
            self.botones[i][j]["state"] = "disabled"
            self.sonido_win.play()
        else:
            self.botones[i1][j1].config(image=self.dorso_img)
            self.botones[i][j].config(image=self.dorso_img)
            self.botones[i1][j1].image_ref = None
            self.botones[i][j].image_ref = None
        self.primer_click = None

if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoMemoria(root)
    root.mainloop()
    pygame.mixer.quit()
