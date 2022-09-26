class Parser:
    DIGITS    = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    OPERATORS = ['+', '-', '*', '/']

    def __init__(self, postfix):
        self.postfix = postfix
        self.s       = ''
        self.n       = 0
        self.temp    = []
        self.indent  = 0

    def parse(self, s):
        print('=' * len(s))
        print(s)
        print('=' * len(s))
        print('\nParsing Tree:')
        print('=============')

        self.s = s + ' '
        try:
            self._get_expression()
            self._error_unexpected('END OF FILE')
        except Exception as e:
            print(str(e))

    def _println(self, s):
        print('    ' * self.indent, s)

    def _error_unexpected(self, expected):
        raise Exception(f'ERROR: Expecting {expected}, found "{self._last()}"')

    def _next(self):
        if self.n < len(self.s):
            c = self.s[self.n]
            self.n += 1
            return c

        self.postfix.insert('EOF')
        raise Exception('\nEOF\n')

    def _last(self):
        return self.s[self.n]

    def _step_back(self):
        self.n -= 1

    def _get_char(self, char):
        c = self._next()
        if c == char:
            # self._println(f'char {c}')
            return True
        self._step_back()
        return False

    def _get_space(self):
        c = self._next()
        while c in [' ', '\t', '\n']:
            c = self._next()
        self._step_back()

    def _get_parenthesised_expression(self):
        self._get_space()
        if self._get_open_parentheses():
            self._get_expression(True)
            self._get_close_parentheses(True)
            return True
        return False

    def _get_expression(self, required=False):
        found = False

        self._get_space()
        if not (self._get_number() or self._get_parenthesised_expression()):
            if required:
                self._error_unexpected('NUMBER or (EXPRESSION)')
        else:
            found = True
            self._get_space()
            if self._get_operator():
                self._get_expression(True)

        if required and not found:
            self._error_unexpected('EXPRESSION')

        return found

    def _get_open_parentheses(self, required=False):
        if self._get_char('('):
            self._println('(')
            self.postfix.insert('(')
            self.indent += 1
            return True
        if required:
            self._error_unexpected('CLOSE_PARENTHESES')
        return False

    def _get_close_parentheses(self, required=False):
        if self._get_char(')'):
            self.indent -= 1
            self._println(')')
            self.postfix.insert(')')
            return True
        if required:
            self._error_unexpected('CLOSE_PARENTHESES')
        return False

    def _get_digits(self, required=False):
        s = ''
        c = self._next()
        while c in self.DIGITS:
            s += c
            c = self._next()
        self._step_back()

        found = len(s) > 0
        if found:
            self.temp.append(s)
        elif required:
            self._error_unexpected('DIGIT')
        return found

    def _get_number(self, required=False):
        self.temp = []
        s = ''
        if self._get_digits():
            s += self.temp.pop()
            if self._get_char('.'):
                self._get_digits(True)
                s += '.' + self.temp.pop()
        elif self._get_char('.'):
            self._get_digits(True)
            s += '0.' + self.temp.pop()

        found = len(s) > 0

        if found:
            self._println(f'Number({s})')
            self.postfix.insert(float(s))
        elif required:
            self._error_unexpected('NUMBER')

        return found

    def _get_operator(self):
        for c in self.OPERATORS:
            if self._get_char(c):
                self._println(f'Operator({c})')
                self.postfix.insert(c)
                return True
        return False