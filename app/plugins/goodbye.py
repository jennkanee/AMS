from app.commands import Command

class GoodbyeCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "goodbye"
        self.description = "Say goodbye"

    def execute(self, *args, **kwargs):
        print("Goodbye!")