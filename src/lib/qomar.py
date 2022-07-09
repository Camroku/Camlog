# qomar: A markup language written in Python for QoLang
# This file can be imported and used as `function(None, [args])` in Python
qolang_export = {
    "compiletohtml": "compile.html",
}

# Some functions were taken from QoLang's lexer.
class QomarCompiler:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.out = ""

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self, characters=1):
        peek_pos = self.pos + characters
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

    def blockcode(self):
        self.advance()
        self.advance()
        self.advance()
        escaped = False
        self.out += "<pre>"
        while True:
            if escaped:
                self.out += self.current_char
            else:
                if self.current_char == '`' and self.peek() == '`' and self.peek(2) == '`':
                    break
                else:
                    self.out += self.current_char
            self.advance()
        
        self.advance()
        self.advance()
        self.out += "</pre>"

    def skipspace(self):
        while self.current_char != None and self.current_char.isspace():
            if self.current_char == '\n' and self.peek() == '\n':
                self.out += "</p><p>"
                self.advance()
            elif self.current_char == '\n':
                self.out += '<br>'
            self.advance()

        if self.peek(-1) != '\n':
            self.out += " "

    def compile(self):
        escaped = False
        bold = False
        italic = False
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skipspace()
                continue
            if not escaped:
                if self.current_char == '/' and self.peek() == '*':
                    self.skipcomment()
                elif self.current_char == '`' and self.peek() == '`' and self.peek(2) == '`':
                    self.blockcode()
                elif self.current_char == '`':
                    self.code()
                elif self.current_char == '\'' and self.peek() == '\'':
                    if bold:
                        self.out += "</b>"
                    else:
                        self.out += "<b>"
                    bold = not bold
                    self.advance()
                elif self.current_char == '\'':
                    if italic:
                        self.out += "</i>"
                    else:
                        self.out += "<i>"
                    italic = not italic
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
