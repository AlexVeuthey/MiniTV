import threading

from minitv.event_manager import manager
from minitv.image_button import ImageButton


class ChromeButton(ImageButton):

    def __init__(self, url, canvas, filename, size, position, offset):
        super().__init__(canvas, filename, size, position, offset)
        self.url = url
        self.driver = None

    def on_highlighted(self):
        super().on_highlighted()
        manager.emit('hide_text')

    def quit(self):
        super().quit()
        """Callback to quit the Chrome driver"""
        print("Quitting driver")
        if self.driver is not None:
            self.driver.quit()
            manager.remove_handler('quit', self.quit)

    def on_click(self):
        """Method callback for button click"""

        manager.emit('show_spinner')

        def start_website():
            """Function for starting web browsing, to be used in thread"""
            from selenium import webdriver
            opt = webdriver.ChromeOptions()
            opt.add_argument('--start-fullscreen')
            # keep user profile to save params
            opt.add_argument('--user-data-dir=~/.chrome/profile/')
            # remove flag warning about automation
            opt.add_experimental_option('excludeSwitches', ['enable-automation'])
            # start driver, keep a copy to prevent garbage collection
            driver = webdriver.Chrome(chrome_options=opt)
            self.driver = driver
            manager.add_handler('quit', self.quit)
            manager.emit('hide_spinner')
            self.driver.get(self.url)

        x = threading.Thread(target=start_website, daemon=True)
        x.start()
