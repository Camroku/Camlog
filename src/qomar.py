# qomar: A markup language written in Python for QoLang
# This file can be imported and used as `function(None, [args])` in Python
qolang_export = {
    "compiletohtml": "compile.html"
}

# Some functions were taken from QoLang's lexer.
class QomarCompiler:
    def __init__(self, text):
        self.text = text.replace("\n\n", "</p><p>").replace("\n", "<br>")
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.out = ""

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skipcomment(self):
        self.advance()
        self.advance()
        while self.current_char != '*' and self.peek() != '/':
            self.advance()
        self.advance()
        self.advance()

    def code(self):
        self.advance()
        escaped = False
        self.out += "<code>"
        while True:
            if escaped:
                self.out += self.current_char
            else:
                if self.current_char == '`':
                    break
                else:
                    self.out += self.current_char
            self.advance()
        
        self.out += "</code>"

    def compile(self):
        escaped = False
        while self.current_char is not None:
            if not escaped:
                if self.current_char == '/' and self.peek() == '*':
                    self.skipcomment()
                elif self.current_char == '`':
                    self.code()
                elif self.current_char == '\\':
                    escaped = True
                    continue
                else:
                    self.out += self.current_char
                escaped = False
            else:
                self.out += self.current_char
            self.advance()
        
        return self.out


def compiletohtml(Variables, args):
    """
    Compile qomar to HTML.
    """
    comp = QomarCompiler(args[0])
    return (Variables, comp.compile())
