class Macro:

    def __init__(self, name):
        self.name = name
        self.options = {}
        self.arguments = []

    def setOptions(self, options):
        self.options = options

    def addArgument(self, arg):
        self.arguments.append(arg)

    def __repr__(self):
        return f"Macro(name={self.name}, options={self.options}, arguments={self.arguments})"
