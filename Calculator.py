from Parser import Parser
from Postfix import Postfix
from ExpressionTree import ExpressionTree


class Calculator:
    def run(self, s):
        postfix = Postfix()
        parser = Parser(postfix)
        parser.parse(s)
        tokens = postfix.get()

        s = f'Postfix: [{postfix}]'
        print('=' * len(s))
        print(s)
        print('=' * len(s))
        tokens.reverse()
        tree = ExpressionTree(tokens)
        result = tree.calculate()
        print('RESULT:', result)




