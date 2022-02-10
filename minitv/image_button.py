import tkinter as tk

from PIL import ImageTk

from minitv.event_manager import manager
from minitv.utils import open_nothover_image, open_resize_image


class ImageButton():

    def __init__(self, canvas, filename, size, position):
        self.imgNormal = ImageTk.PhotoImage(open_nothover_image(filename, size))
        self.imgHover = ImageTk.PhotoImage(open_resize_image(filename, size))

        self.image = canvas.create_image(position[0], position[1], image=self.imgNormal, anchor=tk.NW)

        self.canvas = canvas
        self.canvas.tag_bind(self.image, '<Enter>', self.on_enter)
        self.canvas.tag_bind(self.image, '<Leave>', self.on_leave)
        self.canvas.tag_bind(self.image, '<Button-1>', self.on_click)

        self.driver = None

    def on_enter(self, event):
        self.canvas.itemconfig(self.image, image=self.imgHover)

    def on_leave(self, event):
        self.canvas.itemconfig(self.image, image=self.imgNormal)

    def on_click(self, event):

        def quit():
            print("Quitting driver")
            if self.driver is not None:
                self.driver.quit()
                manager.remove_handler('quit', quit)

        from selenium import webdriver
        opt = webdriver.ChromeOptions()
        opt.add_argument('--start-fullscreen')
        opt.add_argument('--user-data-dir=~/.chrome/profile/')
        opt.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(chrome_options=opt)
        self.driver = driver
        manager.add_handler('quit', quit)
        driver.get('https://www.youtube.com')
