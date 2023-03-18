from enum import IntEnum
from dataclasses import dataclass
from collections import deque
from copy import deepcopy

class LEX_TYPES(IntEnum):
    NONE = 0
    OPERATOR = 1
    NUMBER = 2

class Token:
    def __init__(self, value : str, ttype : LEX_TYPES):
        self.value = value
        self.type = ttype

    def __repr__(self):
        type_str = ["none", "operator", "number"]
        return f"<{type_str[self.type]}: {self.value}>"

class MathLexer:
    def __init__(self):
        self.nums = {str(x) for x in range(10)}
        self.operators = {'(', ')', '+', '*', '-', '/', '.'}
        self.whitespace = {' ', '\n', '\r', '\t'}

    def first_pass(self, input : str) -> list[Token]:
        token_list = deque()
        cur_token = ""
        cur_type = LEX_TYPES.NONE
        lexing_number = False
        for char in input:
            if char in self.nums:
                if not lexing_number and len(cur_token) > 0:
                    token_list.append( Token(cur_token, cur_type) )
                    cur_token = ""
                cur_token += char
                cur_type = LEX_TYPES.NUMBER
                lexing_number = True
            elif char in self.operators:
                lexing_number = False
                if len(cur_token) > 0:
                    token_list.append( Token(cur_token, cur_type))
                    cur_token = ""
                cur_token += char
                cur_type = LEX_TYPES.OPERATOR
            elif char in self.whitespace:
                if len(cur_token) > 0:
                    token_list.append( Token(cur_token, cur_type))
                    cur_token = ""
                    lexing_number = False
            else:
                raise ValueError()
        if len(cur_token) > 0:
            token_list.append( Token(cur_token, cur_type))
        return token_list
    
    def second_pass(self, input : list[Token]) -> list[Token]:
        pass

    def lex_string(self, input) -> list[Token]:
        split_numbers = self.first_pass(input)
        print(split_numbers)
        tokenised = self.second_pass(split_numbers)
        print(tokenised)
        return split_numbers

# Formal grammar: all tokens must evaluate to either a single number OR two
# numbers separated by an operation
# A number is one of the following:
# 1. A single number token separated by preceding and succeeding tokens by an
# operation such as +,-,/,* (ie a real operation, not syntax)
# 2. A number token preceded by . - this is equivalent to 0.x
# 3. Two number tokens separated by . ; parsed into a single floating point
# number
# - is ambiguous; if it falls at the start of a sequence or after an operator 
# and is followed by a number, it is part of that number (i.e. the number is 
# negative) If it falls between two numbers then it is an operation
# ( resets the parser state and pushes the previous state onto the stack
# ) pops the previous state from the stack

class ParseTreeNode():
    def __init__(self, token):
        self.token = token
        self.left = None
        self.right = None

class State(IntEnum):
    START = 0
    PARSE_DOT = 1
    PARSE_NUMBER = 2
    PARSE_OPERATOR = 3
    PARSE_MINUS = 4
    COMPLETE = 5

class MathParser:
    def __init__(self):
        self.parse_tree = None
        self.cur_node = None
        self.state_fns = [
            self.state_start,
            self.state_dot,
            self.state_number,
            self.state_operator,
            self.state_minus
        ]
        self.index = 0
        self.tokens = []
        self.state = State.START

    def parse(self, in_tokens: deque[Token]):
        if len(in_tokens) == 0:
            self.parse_tree = None
            return
                
        self.state = State.START
        self.tokens = deepcopy(in_tokens)
        self.parse_tree = None
        self.index = 0

        self.state_number(self.tokens)
        # while(self.state != State.COMPLETE and self.index < len(self.tokens)):
        #     self.state_fns[self.state]()

    def state_start(self):
        cur = self.tokens[self.index]
        if cur.type == LEX_TYPES.NUMBER:
            self.state = State.PARSE_NUMBER
        elif cur.type == LEX_TYPES.OPERATOR and (cur.value == "." or cur.value == "-"):
            self.state = State.PARSE_NUMBER
        else:
            # first input must always be a number
            raise ValueError()

    def state_dot(self):
        pass

    def state_number(self, tokens: list[Token]):
        # three valid inputs to this state
        # .# ; -# ; #.# ; -#.# ; #
        allowDot = True
        allowNegative = True
        prevWasNumber = False
        aggregate_val = ""
        index = 0
        
        tokens_out = []
        cur = tokens[index]
        # first set of tokens must evaluate to number
        if not (cur.type == LEX_TYPES.NUMBER or (cur.type == LEX_TYPES.OPERATOR and (cur.value == "." or cur.value == "-"))):
            raise ValueError() 

        while index < len(tokens):
            cur = tokens[index]
            if cur.type == LEX_TYPES.OPERATOR:
                prevWasNumber = False
                if cur.value == ".":
                    if allowDot:
                        # dot can be in any position but only once
                        aggregate_val += "."
                        allowDot = False
                    else:
                        raise ValueError()
                elif cur.value == "-" and len(aggregate_val) == 0:
                    aggregate_val += "-"
                    allowNegative = False
                elif cur.value == "-" and aggregate_val == ".":
                    raise ValueError()
                    # this will ignore negatives in weird places (after decimal point) but not raise an error
                    # 3.1-.5 OK 3.1-1 OK .-3 not ok
                else:
                    # all other operators are valid, but end the number lex
                    if len(aggregate_val) > 0:
                        if aggregate_val[-1] == "." or aggregate_val[-1] == "-":
                            raise ValueError()
                        tokens_out.append(Token(aggregate_val, LEX_TYPES.NUMBER))
                    tokens_out.append(cur)
                    aggregate_val = ""
                    allowNegative = True
                    allowDot = True
                    print(tokens_out)
            elif cur.type == LEX_TYPES.NUMBER:
                if prevWasNumber:
                    raise ValueError()
                aggregate_val += cur.value
                prevWasNumber = True
            index += 1
            # only allow negative on first character
            # allowNegative = False
        
        # must end with number
        if aggregate_val[-1] not in {str(x) for x in range(10)}:
            raise ValueError
        
        tokens_out.append(Token(aggregate_val, LEX_TYPES.NUMBER))
        
        print(tokens_out)

    def state_operator(self):
        pass

    def state_minus(self):
        pass

    def execute(self):
        pass



lex = MathLexer()
lex_list = lex.lex_string("-10 + .5. + -5 - 100.7 + 5")
print(lex_list)

parser = MathParser()
parser.parse(lex_list)