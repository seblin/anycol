class Column:
    def __init__(self, items):
        self.items = items

    @property
    def template(self):
        # Removed special handling for width 0
        return [str(item) for item in self.items]

    def __str__(self):
        return '\n'.join(str(item) for item in self.items)