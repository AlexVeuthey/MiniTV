from minitv.event_manager import manager

class AppState:
    def __init__(self):
        self.in_app = True
        
        manager.add_handler('proceed', self.set_polling_inactive)
        manager.add_handler('quit', self.set_polling_active)

        
    def set_polling_active(self):
        self.in_app = True


    def set_polling_inactive(self):
        self.in_app = False
        

app_state = AppState()