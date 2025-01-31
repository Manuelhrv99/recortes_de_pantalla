import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk
import pyscreenshot as ImageGrab
import sys
import pyautogui # Importante no borrar esta linea, hace que se vean bien los recortes

import os
import pytesseract as tesseract

tesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Guarda el rectangualo creado adentro del canvas
images = []

class main:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Menu')
        self.window.attributes('-fullscreen', True)
        self.window.resizable(0,0)
        self.window.config(cursor="crosshair white")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Creacion del canvas
        self.C = tk.Canvas(self.window, height=screen_height, width=screen_width)

        self.C.pack()

        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        
        bg = tk.PhotoImage(file = "screenshot.png")
        self.C.create_image( 0, 0, image = bg, anchor = "nw")

        # Dar la transparencia al canvas creando un rectangulo
        self.window.bind(self.create_rectangle(self.C, 0, 0, screen_width, screen_height, fill='white', alpha=0.05)) # El alpha cambia la opasidad de la ventana

        # Propiedades del mouse
        exit_button = tk.Button(
            self.window, 
            text="x",
            relief="ridge",
            height=1,
            bd="0",
            bg="black",
            fg="white",
            width=3,
            cursor="hand1", 
            command=self.window.destroy)
        font_btn = tkFont.Font(family='Helvetica', size=20, weight='bold')
        exit_button['font'] = font_btn
        exit_button.place(x = (screen_width/2), y = 0)

        # Evento del click izquierdo
        self.window.bind("<ButtonPress-1>", self.on_button_press)
        self.window.bind("<B1-Motion>", self.on_move_press)
        self.window.bind("<ButtonRelease-1>", self.on_button_release)
        
        # Muestra la ventana
        self.window.mainloop()

    def on_button_press(self,event):
        # Posicion inicial del mouse
        self.start_x = self.C.canvasx(event.x)
        self.start_y = self.C.canvasy(event.y)

        # Crea el cuadro al arrastrar el mouse
        self.rect = self.C.create_rectangle(0, 0, 0, 0, outline='blue', width=2)

    def on_move_press(self,event):
        self.curX = self.C.canvasx(event.x)
        self.curY = self.C.canvasy(event.y)

        # Crear el rectangulo mientras se arrastra el mouse
        self.C.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def on_button_release(self, event):
        # Convertir todas las coordenadas a int
        first_x = int(self.start_x)
        first_y = int(self.start_y)
        final_x = int(self.curX)
        final_y = int(self.curY)

        try:
            # Validacion para ordenar las coordenadas

            # ↘↘↘↘↘ De arriba a la izquierda para abajo a la derecha
            if first_x < final_x and first_y < final_y:
                im = ImageGrab.grab(bbox=(first_x, first_y, final_x, final_y))
            # ↙↙↙↙↙ De arriba a la derecha a abajo a la izquierda
            elif first_x > final_x and first_y < final_y:
                im = ImageGrab.grab(bbox=(final_x, first_y, first_x, final_y))
            # ↗↗↗↗↗ De abajo a la izquierda a arriba a la derecha
            elif first_x < final_x and first_y > final_y: 
                im = ImageGrab.grab(bbox=(first_x, final_y, final_x, first_y))
            # ↖↖↖↖↖ De abajo a la derecha a arriba a la izquierda
            else:
                im = ImageGrab.grab(bbox=(final_x, final_y, first_x, first_y))

            self.resized_im = self.modify_image(im)

            self.img_to_text()       

            # Cierra el programa despues de hacer un recorte
            sys.exit()                                      
        except:
            # Cierra el programa si hay un fallo
            sys.exit()

    # Crea un rectangulo transparente y lo aplica en el canvas como imagen
    def create_rectangle(self, c, x1, y1, x2, y2, **kwargs):
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = self.window.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (x2-x1, y2-y1), fill)
        images.append(ImageTk.PhotoImage(image))
        c.create_image(x1, y1, image=images[-1], anchor='nw')

    # Cambiar el tamaño de la imagen
    def modify_image(self, im):
        w, h = im.size
        w = int(w * 2.5)
        h = int(h * 2.5)
        resized_im = im.resize((w, h))

        return resized_im

    def img_to_text(self):
        imageToText = tesseract.image_to_string(self.resized_im, config="--oem 1 --psm 4")    

        txtFile = open('ML_Text.txt', 'w+')
        txtFile.write(imageToText + '\n')
        txtFile.close()

        # Abre el bloc de notas
        os.startfile('ML_Text.txt')
        

if __name__ == '__main__':
    app = main()