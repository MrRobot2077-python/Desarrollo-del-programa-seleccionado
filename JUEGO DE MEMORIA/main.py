import tkinter as tk
from PIL import Image, ImageTk
import random
from functools import partial

class JuegoMemoria:
    def __init__(self, master):
        self.master = master
        self.master.title("Matheo Juego de Memoria")
        self.master.geometry("400x400")
        self.imagenes_archivos = [
            r"C:\Users\Mathe\OneDrive\Escritorio\UNIVERSIDAD\deberes\JUEGO DE MEMORIA\images\img1.jpg",
            r"C:\Users\Mathe\OneDrive\Escritorio\UNIVERSIDAD\deberes\JUEGO DE MEMORIA\images\img2.jpg",
            r"C:\Users\Mathe\OneDrive\Escritorio\UNIVERSIDAD\deberes\JUEGO DE MEMORIA\images\img3.jpg",
            r"C:\Users\Mathe\OneDrive\Escritorio\UNIVERSIDAD\deberes\JUEGO DE MEMORIA\images\img4.jpg",
            r"C:\Users\Mathe\OneDrive\Escritorio\UNIVERSIDAD\deberes\JUEGO DE MEMORIA\images\img5.jpg",
            r"C:\Users\Mathe\OneDrive\Escritorio\UNIVERSIDAD\deberes\JUEGO DE MEMORIA\images\img6.jpg",
            r"C:\Users\Mathe\OneDrive\Escritorio\UNIVERSIDAD\deberes\JUEGO DE MEMORIA\images\img7.jpg",
            r"C:\Users\Mathe\OneDrive\Escritorio\UNIVERSIDAD\deberes\JUEGO DE MEMORIA\images\img8.jpg"
        ] * 2
        random.shuffle(self.imagenes_archivos)
        self.imagen_objs = []
        self.botones = []
        self.primer_click = None
        self.cargar_imagenes()
        self.crear_tablero()

    def cargar_imagenes(self):
        for archivo in self.imagenes_archivos:
            img = Image.open(archivo)
            img = img.resize((80, 80), Image.Resampling.LANCZOS)
            self.imagen_objs.append(ImageTk.PhotoImage(img))

    def crear_tablero(self):
        for i in range(4):
            fila = []
            for j in range(4):
                boton = tk.Button(self.master, width=100, height=100, command=partial(self.voltear_tarjeta, i, j))
                boton.grid(row=i, column=j)
                fila.append(boton)
            self.botones.append(fila)

    def voltear_tarjeta(self, i, j):
        boton = self.botones[i][j]
        indice = i * 4 + j
        if not boton["image"]:
            boton["image"] = self.imagen_objs[indice]
            if self.primer_click is None:
                self.primer_click = (i, j)
            else:
                self.master.after(1000, self.verificar_emparejamiento, i, j)

    def verificar_emparejamiento(self, i, j):
        i1, j1 = self.primer_click
        indice1 = i1 * 4 + j1
        indice2 = i * 4 + j
        if self.imagenes_archivos[indice1] == self.imagenes_archivos[indice2]:
            self.botones[i1][j1]["state"] = "disabled"
            self.botones[i][j]["state"] = "disabled"
        else:
            self.botones[i1][j1]["image"] = ""
            self.botones[i][j]["image"] = ""
        self.primer_click = None

if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoMemoria(root)
    root.mainloop()
