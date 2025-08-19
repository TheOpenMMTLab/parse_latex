class Text:

    def __init__(self, content):
        self.content = content

    def append(self, text):
        self.content += text

    def __repr__(self):
        return f"Text(content={self.content})"
