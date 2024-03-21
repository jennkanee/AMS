from app.commands import Command

class GreetCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "greet"
        self.description = "Greet the user"

    def execute(self, *args, **kwargs):
        print("Hello! How can I assist you today?")