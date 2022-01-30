import tkinter as tk

from minitv.button_grid import ButtonGrid


def main():
    window = tk.Tk()
    window.attributes("-fullscreen", True)
    ButtonGrid(window, window.winfo_screenwidth(), window.winfo_screenheight())
    window.mainloop()


if __name__ == '__main__':
    main()
