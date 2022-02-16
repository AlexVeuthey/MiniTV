from minitv.event_manager import manager


class Infotext:

    def __init__(self, canvas, position, size):
        self.canvas = canvas
        self.position = position
        self.size = size
        self.visible = False
        self.rectangle = None
        self.text = None
        manager.add_handler('show_text', self.show)
        manager.add_handler('hide_text', self.hide)

    def show(self, text):

        self.hide()

        self.rectangle = self.canvas.create_rectangle(self.position[0], self.position[1],
                                                      self.size[0], self.size[1], fill='black')
        self.text = self.canvas.create_text(self.position[0]+25, self.position[1]+25,
                                            text=text, anchor="nw", fill='white', font=('Helvetica', '40', 'bold'))
        self.visible = True

    def hide(self):

        if (self.rectangle):
            self.canvas.delete(self.rectangle)

        if (self.text):
            self.canvas.delete(self.text)

        self.visible = False
        self.rectangle = None
        self.text = None
