# qomar: A markup language written in Python for QoLang
# This file can be imported and used as `compiler = QomarCompiler(text)` and `compiler.compile()` in Python
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

    def advance(self, characters=1):
        self.pos += characters
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
        while self.current_char is not None:
            if escaped:
                self.out += self.current_char
                escaped = False
            else:
                if self.current_char == '`':
                    break
                elif self.current_char == '\\':
                    escaped = True
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
        while self.current_char is not None:
            if escaped:
                self.out += self.current_char
                escaped = False
            else:
                if self.current_char == '`' and self.peek() == '`' and self.peek(2) == '`':
                    break
                elif self.current_char == '\\':
                    escaped = True
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

    def mention(self):
        self.advance()
        user = ""
        while self.current_char is not None:
            if self.current_char.isspace():
                    break
            else:
                user += self.current_char
            self.advance()

        self.out += f"<a href=\"/a/{user}\">@{user}</a>"

    def link(self):
        self.advance()
        linkntext = ""
        while self.current_char is not None:
            if self.current_char == ']':
                    break
            else:
                linkntext += self.current_char
            self.advance()
        self.advance()
        
        splitted = linkntext.split(' ')
        link = splitted[0]
        if len(splitted) > 1:
            text = ' '.join(splitted[1:])
        else:
            text = link

        self.out += f"<a href=\"{link}\">{text}</a>"

    def compile(self):
        escaped = False
        bold = False
        italic = False
        header = 0
        ulist = False
        olist = False
        blockquote = False
        while self.current_char is not None:
            if self.current_char == '\n' and self.peek() == '\n' and ulist:
                self.advance(2)
                self.out += "</ul>"
                ulist = False
                continue
            elif self.current_char == '\n' and self.peek() == '\n' and olist:
                self.advance(2)
                self.out += "</ol>"
                olist = False
                continue
            elif self.current_char == '\n' and (ulist or olist):
                self.advance(1)
                self.out += "</li>"
                continue
            if self.current_char == '\n' and header != 0:
                self.out += f"</h{str(header)}>"
                header = 0
                self.advance()
                continue
            if self.current_char == '\n' and self.peek() == '\n' and blockquote:
                self.out += f"</blockquote>"
                blockquote = False
                self.advance(2)
                continue
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
                    self.advance()
                    continue
                elif self.peek(-1) == '\n' and \
                    self.current_char == '-' and \
                    self.peek() == '>' and \
                    self.peek(2) == ' ':
                        self.out += "<h1>"
                        header = 1
                        self.advance(2)
                elif self.peek(-1) == '\n' and \
                    self.current_char == '-' and \
                    self.peek() == '-' and \
                    self.peek(2) == '>' and \
                    self.peek(3) == ' ':
                        self.out += "<h2>"
                        header = 2
                        self.advance(3)
                elif self.peek(-1) == '\n' and \
                    self.current_char == '-' and \
                    self.peek() == '-' and \
                    self.peek(2) == '-' and \
                    self.peek(3) == '>' and \
                    self.peek(4) == ' ':
                        self.out += "<h3>"
                        header = 3
                        self.advance(4)
                elif self.peek(-1) == '\n' and \
                    self.current_char == '-' and \
                    self.peek() == '-' and \
                    self.peek(2) == '-' and \
                    self.peek(3) == '-' and \
                    self.peek(4) == '>' and \
                    self.peek(5) == ' ':
                        self.out += "<h4>"
                        header = 4
                        self.advance(5)
                elif self.peek(-1) == '\n' and \
                    self.current_char == '-' and \
                    self.peek() == '-' and \
                    self.peek(2) == '-' and \
                    self.peek(3) == '-' and \
                    self.peek(4) == '-' and \
                    self.peek(5) == '>' and \
                    self.peek(6) == ' ':
                        self.out += "<h5>"
                        header = 5
                        self.advance(6)
                elif self.peek(-1) == '\n' and \
                    self.current_char == '-' and \
                    self.peek() == '-' and \
                    self.peek(2) == '-' and \
                    self.peek(3) == '-' and \
                    self.peek(4) == '-' and \
                    self.peek(5) == '-' and \
                    self.peek(6) == '>' and \
                    self.peek(7) == ' ':
                        self.out += "<h6>"
                        header = 6
                        self.advance(7)
                elif self.peek(-1) == '\n' and self.current_char == '*':
                    if not ulist:
                        if self.out[-4:] == "<br>":
                            self.out = self.out[:-4]
                        self.out += "<ul>"
                        ulist = True
                    self.out += "<li>"
                elif self.peek(-1) == '\n' and self.current_char == '#':
                    if not olist:
                        if self.out[-4:] == "<br>":
                            self.out = self.out[:-4]
                        self.out += "<ol>"
                        olist = True
                    self.out += "<li>"
                elif self.peek(-1) == '\n' and \
                    self.current_char == '>' and \
                    self.peek() == ' ':
                        self.out += "<blockquote>"
                        blockquote = True
                        self.advance()
                elif self.current_char == '@':
                    self.mention()
                    continue
                elif self.current_char == '[':
                    self.link()
                    continue
                else:
                    self.out += self.current_char
                escaped = False
            else:
                self.out += self.current_char
                escaped = False
            self.advance()
        
        if ulist:
            self.out += "</ul>"
        if olist:
            self.out += "</ol>"
        
        return self.out


def compiletohtml(Variables, args):
    """
    Compile qomar to HTML.
    """
    comp = QomarCompiler(args[0])
    return (Variables, comp.compile())
