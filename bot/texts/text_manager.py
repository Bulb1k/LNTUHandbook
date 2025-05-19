from texts import start, validation, services, asking, keyboards

class TextManager:
    def __init__(self):
        self.validation = validation
        self.asking = asking
        self.start = start
        self.services = services
        self.keyboards = keyboards

texts = TextManager()