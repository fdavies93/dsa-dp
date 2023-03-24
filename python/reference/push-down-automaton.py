from enum import IntEnum
from dataclasses import dataclass
from collections import deque
from copy import deepcopy
from typing import Union

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


    def second_pass(self, tokens: list[Token]):
        # three valid inputs to this state
        # .# ; -# ; #.# ; -#.# ; #
        allowDot = True
        prevWasNumber = False
        aggregate_val = ""
        index = 0
        
        tokens_out = []
        cur = tokens[index]
        # first set of tokens must evaluate to number
        # amend so that it's first set of tokens AFTER OPENING BRACES later
        if not (cur.type == LEX_TYPES.NUMBER or (cur.type == LEX_TYPES.OPERATOR and (cur.value == "." or cur.value == "-")) or cur.value == "("):
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
                elif cur.value == "-" and aggregate_val == ".":
                    raise ValueError()
                    # this will ignore negatives in weird places (after decimal point) but not raise an error
                    # 3.1-.5 OK 3.1-1 OK .-3 not ok
                else:
                    # all other operators are valid, but end the number lex
                    if len(aggregate_val) > 0:
                        if aggregate_val[-1] == "." or aggregate_val[-1] == "-":
                            raise ValueError()
                        tokens_out.append(Token(float(aggregate_val), LEX_TYPES.NUMBER))
                    tokens_out.append(cur)
                    aggregate_val = ""
                    allowDot = True
            elif cur.type == LEX_TYPES.NUMBER:
                if prevWasNumber:
                    raise ValueError()
                aggregate_val += cur.value
                prevWasNumber = True
            index += 1
        
        # must end with number or bracket
        if not tokens_out[-1].value == ')' and aggregate_val[-1] not in {str(x) for x in range(10)}:
            raise ValueError
        
        if len(aggregate_val) > 0:
            tokens_out.append(Token(float(aggregate_val), LEX_TYPES.NUMBER))

        return tokens_out

    def lex_string(self, input) -> list[Token]:
        split_numbers = self.first_pass(input)
        print(split_numbers)
        tokenised = self.second_pass(split_numbers)
        # print(tokenised)
        return tokenised

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

class ParseTree():
    def __init__(self):
        self.root = None
    
    def insert_at_root(self, node : ParseTreeNode):
        if self.root is None:
            self.root = node
            return


class State(IntEnum):
    START = 0
    PARSE_DOT = 1
    PARSE_NUMBER = 2
    PARSE_OPERATOR = 3
    PARSE_MINUS = 4
    COMPLETE = 5

class MathParser:

    def __init__(self):
        self.operation_precedence = ['/','*','+','-']

    def get_first_operator_index(self, tokens : list[Union[Token, list]], operator : str):
        for i, token in enumerate(tokens):
            if isinstance(token, Token) and token.value == operator:
                return i
        return None
    
    def parse_inner(self, tokens: list[Token]):
        cur_list = deepcopy(tokens)
        for operation in self.operation_precedence:
            # get the next operation of this type in the list
            next_operation = self.get_first_operator_index(cur_list, operation)
            while next_operation != None:
                next_list = []
                # combine left and right-hand elements
                combined_elements = cur_list[next_operation-1:next_operation+2]
                next_list = cur_list[:next_operation-1]
                next_list.append(combined_elements)
                next_list.extend(cur_list[next_operation+2:])
                cur_list = next_list
                # print(f"Operator {operation} found at index {next_operation}")
                next_operation = self.get_first_operator_index(cur_list, operation)
        
        return cur_list[0]

    def parse(self, tokens: list[Token]):
        if len(tokens) == 0:
            return None

        before_stack : list[list] = []
        cur_list : list[Token] = deepcopy(tokens)

        cur_i = 0
        while cur_i < len(cur_list):
            token = cur_list[cur_i]
            if isinstance(token, Token) and token.value == '(':
                before = cur_list[:cur_i]
                if len(before) == 0:
                    before = None
                before_stack.append(before)
                cur_list = cur_list[cur_i+1:]
                cur_i = 0
            elif isinstance(token, Token) and token.value == ')':
                before = before_stack.pop()
                if before == None:
                    before = []
                # print(f"Before: {before}")
                inner = self.parse_inner(cur_list[:cur_i])
                # print(f"Inner: {inner}")
                after = cur_list[cur_i+1:]
                # print(f"After: {after}")
                cur_list = before
                cur_list.append(inner)
                cur_list.extend(after)
                cur_i = 0
            else:
                cur_i += 1

        print(cur_list)
        return self.parse_inner(cur_list)

    def evaluate(self, parse_tree : list):
        # fetch / calculate left and right values
        if isinstance(parse_tree[0], list):
            left = self.evaluate(parse_tree[0])
        elif isinstance(parse_tree[0], Token):
            left = parse_tree[0].value
        if isinstance(parse_tree[2], list):
            right = self.evaluate(parse_tree[2])
        elif isinstance(parse_tree[2], Token):
            right = parse_tree[2].value
        # evaluate the values wrt operator
        operator = parse_tree[1].value
        if operator == '*':
            return left * right
        elif operator == '/':
            return left / right
        elif operator == '+':
            return left + right
        elif operator == '-':
            return left - right


# NOTE: Lexer still allows putting 2 operators next to each other; this is fine for brackets 
# but not valid for regular operations.

lex = MathLexer()
parser = MathParser()

print("Welcome to Del's great calculator.")
print("Enter an equation or type q to quit.")
cmd = ''
while (True):
    cmd = input('> ')
    if cmd == 'q':
        break
    lex_list = lex.lex_string(cmd) # answer is 125 of course
    print(lex_list)
    parse_tree = parser.parse(lex_list)
    result = parser.evaluate(parse_tree)

    print(result)