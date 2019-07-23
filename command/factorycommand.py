from .abstract import AbstractCommand

class FactoryCommand(AbstractCommand):

    def __init__(self, factory):
        super(FactoryCommand, self).__init__()
        self.factory = factory

    def execute(self):
        commands = self.factory.create_commands()
        for command in commands:
            command.execute()