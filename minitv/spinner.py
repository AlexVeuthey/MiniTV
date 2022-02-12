from PIL import Image, ImageTk

from minitv.event_manager import manager


class Spinner:

    def __init__(self, canvas, position):
        self.canvas = canvas
        self.position = position
        self.visible = False

        self.update = self.draw().__next__
        canvas.after_idle(self.update)
        manager.add_handler('show_spinner', self.show)
        manager.add_handler('hide_spinner', self.hide)

    def show(self):
        print("Showing spinner")
        self.visible = True

    def hide(self):
        print("Hiding spinner")
        self.visible = False

    def draw(self):
        image = Image.open('minitv/assets/images/spinner.png').convert('RGBA')
        angle = 0
        canvas_obj = None
        while True:
            if self.visible:
                tkimage = ImageTk.PhotoImage(image.rotate(angle))
                canvas_obj = self.canvas.create_image(self.position[0],
                                                      self.position[1], image=tkimage)
            self.canvas.after(5, self.update)
            yield
            if self.visible or canvas_obj is not None:
                self.canvas.delete(canvas_obj)
                canvas_obj = None
                angle -= 1
                angle %= 360
