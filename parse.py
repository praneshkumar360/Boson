from token_types import *
from error import *
from parse_result import *
from nodes import *

######################
#####   PARSER  ######
######################

class Parser:
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_index = -1
        self.curr_tok = None
        self.register_count = 0
        self.increment()

    def increment(self):
        self.tok_index += 1
        self.register_count += 1
        if self.tok_index >=0 and self.tok_index < len(self.tokens):
            self.curr_tok = self.tokens[self.tok_index]

    def reverse(self):
        self.tok_index -= 1
        if self.tok_index >=0 and self.tok_index < len(self.tokens):
            self.curr_tok = self.tokens[self.tok_index]

    def parse(self):
        res = self.statements()
        if not res.error and self.curr_tok.type != TT_EOF:
            return res.failure(
                InvalidSyntaxError(self.curr_tok.pos_start, self.curr_tok.pos_end, "Expected '+', '-', '*', '/' or '%'")
            )

        return res

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.curr_tok.pos_start.copy()
        while self.curr_tok.type == TT_NEWLINE:
            self.increment()
        statement = res.register(self.statement())
        if res.error: return res
        if statement != None:
            statements.append(statement)
        more_statements = True

        while True:
            new_line = 0
            while self.curr_tok.type == TT_NEWLINE:
                self.increment()
                new_line += 1
            if new_line == 0:
                more_statements = False
            if not more_statements: break
            if self.curr_tok.type == TT_NEWLINE:
                self.increment()
            else:
                statement = res.register(self.statement())
                if statement != None:
                    statements.append(statement)
        return res.success(ListNode(
            statements,
            pos_start,
            self.curr_tok.pos_end.copy()
        ))

    def statement(self):
        res = ParseResult()
        pos_start = self.curr_tok.pos_start.copy()
        if self.curr_tok.matches(TT_KEYWORD, 'return'):
            self.increment()
            expr = res.register(self.expr())
            return res.success(ReturnNode(expr, pos_start, self.curr_tok.pos_start.copy()))

        if self.curr_tok.matches(TT_KEYWORD, 'continue'):
            self.increment()
            pos_start = self.curr_tok.pos_start.copy()
            return res.success(ContinueNode(pos_start, self.curr_tok.pos_start.copy()))

        if self.curr_tok.matches(TT_KEYWORD, 'break'):
            self.increment()
            pos_start = self.curr_tok.pos_start.copy()
            return res.success(BreakNode(pos_start, self.curr_tok.pos_start.copy()))
        expr = res.register(self.expr())
        if res.error: return res
        return res.success(expr)

    
    def func_def(self):
        res = ParseResult()
        if not self.curr_tok.matches(TT_KEYWORD, 'func'):
            return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected 'func' keyword"
            ))
        self.increment()
        
        if self.curr_tok.type == TT_IDENTIFIER:
            var_name_tok = self.curr_tok
            self.increment()
            if self.curr_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected '('"
            ))
        else:
            var_name_tok = None
            if self.curr_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected '('"
            ))
        self.increment()
        args_name_toks = []
        
        if self.curr_tok.type == TT_IDENTIFIER:
            args_name_toks.append(self.curr_tok)
            self.increment()
            
            while self.curr_tok.type == TT_COMMA:
                self.increment()
                if self.curr_tok.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                    self.curr_tok.pos_start, self.curr_tok.pos_end,
                    "Expected 'Identifier'"
                    ))
                args_name_toks.append(self.curr_tok)
                self.increment()
        

        if self.curr_tok.type != TT_RPAREN:
            return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected ',' or ')'"
            ))
        self.increment()
        if self.curr_tok.type == TT_ARROW:
            
            self.increment()
            
            node_to_return = res.register(self.expr())
            if res.error: return res

            return res.success(FuncDefNode(
                var_name_tok,
                args_name_toks,
                node_to_return,
                True
            ))

        if self.curr_tok.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected '->' or NEW LINE"
            ))
        self.increment()
        body = res.register(self.statements())
        if res.error: return res
        if not self.curr_tok.matches(TT_KEYWORD, 'end'):
            return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected 'end'"
            ))
        self.increment()

        return res.success(FuncDefNode(
            var_name_tok,
            args_name_toks,
            body,
            False
        ))

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.curr_tok.pos_start.copy()
        if self.curr_tok.type != TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected '['"
            ))
        self.increment()
        if self.curr_tok.type == TT_RSQUARE:
            self.increment()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(
                    InvalidSyntaxError( 
                    self.curr_tok.pos_start, self.curr_tok.pos_end, "Expected int, float, identifier, 'var'"
                    ))
            while self.curr_tok.type == TT_COMMA:
                self.increment()
                element_nodes.append(res.register(self.expr()))
                if res.error: return res
            if self.curr_tok.type != TT_RSQUARE:
                return  res.failure(
                        InvalidSyntaxError(
                        self.curr_tok.pos_start, self.curr_tok.pos_end, "Expected ',' or ']'"
                    ))
            self.increment()
        return res.success(ListNode(element_nodes, pos_start, self.curr_tok.pos_end.copy()))
        

    def for_expr(self):
        res = ParseResult()
        if not self.curr_tok.matches(TT_KEYWORD, 'for'):
            return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected 'for'"
            ))

        self.increment()
        if self.curr_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected 'identifier'"
            ))
        var_name = self.curr_tok
        self.increment()

        if self.curr_tok.type != TT_EQUAL:
            return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected '='"
            ))

        self.increment()
        start_value = res.register(self.expr())
        if res.error: return res

        if not self.curr_tok.matches(TT_KEYWORD, 'to'):
            return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected 'to'"
            ))
        
        self.increment()
        end_value = res.register(self.expr())
        if res.error: return res

        if self.curr_tok.matches(TT_KEYWORD, 'step'):
            self.increment()
            step_value = res.register(self.expr())
            if res.error: return res
        else:
            step_value = None
        
        if not self.curr_tok.matches(TT_KEYWORD, 'then'):
                return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected 'then'"
            ))

        self.increment()
        if self.curr_tok.type == TT_NEWLINE:
            self.increment()
            body = res.register(self.statements())
            if res.error: return res
            if not self.curr_tok.matches(TT_KEYWORD, 'end'):
                return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected 'end'"
                ))
            self.increment()
            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))
        body = res.register(self.statement())
        if res.error: return res
        return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))

    def while_expr(self):
        res = ParseResult()
        if not self.curr_tok.matches(TT_KEYWORD, 'while'):
            return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected 'while'"
            ))

        self.increment()
        condition = res.register(self.expr())
        if res.error: return res

        if not self.curr_tok.matches(TT_KEYWORD, 'then'):
                return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected 'then'"
            ))
           
        self.increment()
        if self.curr_tok.type == TT_NEWLINE:
            self.increment()
            body = res.register(self.statements())
            if res.error: return res
            if not self.curr_tok.matches(TT_KEYWORD, 'end'):
                return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                "Expected 'end'"
                ))
            self.increment()
            return res.success(WhileNode(condition, body, True))
        body = res.register(self.statement())
        if res.error: return res

        return res.success(WhileNode(condition, body, False))

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases('if'))
        if res.error: return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))

    def if_expr_b(self):
        return self.if_expr_cases('elif')

    def if_expr_c(self):
        res = ParseResult()
        else_case = None

        if self.curr_tok.matches(TT_KEYWORD, 'else'):
            self.increment()

            if self.curr_tok.type == TT_NEWLINE:
                self.increment()

                statements = res.register(self.statements())
                if res.error: return res
                else_case = (statements, True)

                if self.curr_tok.matches(TT_KEYWORD, 'end'):
                    self.increment()
                else:
                    return res.failure(InvalidSyntaxError(
                    self.curr_tok.pos_start, self.curr_tok.pos_end,
                    "Expected 'END'"
                    ))
            else:
                expr = res.register(self.statement())
                if res.error: return res
                else_case = (expr, False)
        return res.success(else_case)

    def if_expr_b_or_c(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.curr_tok.matches(TT_KEYWORD, 'elif'):
            all_cases = res.register(self.if_expr_b())
            if res.error: return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.if_expr_c())
            if res.error: return res
    
        return res.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.curr_tok.matches(TT_KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(
            self.curr_tok.pos_start, self.curr_tok.pos_end,
            f"Expected '{case_keyword}'"
            ))

        self.increment()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.curr_tok.matches(TT_KEYWORD, 'then'):
            return res.failure(InvalidSyntaxError(
            self.curr_tok.pos_start, self.curr_tok.pos_end,
            f"Expected 'then'"
            ))
        self.increment()
 
        if self.curr_tok.type == TT_NEWLINE:
            self.increment()

            statements = res.register(self.statements())
            if res.error: return res
            cases.append((condition, statements, True))

            if self.curr_tok.matches(TT_KEYWORD, 'end'):
                self.increment()
            else:
                all_cases = res.register(self.if_expr_b_or_c())
                if res.error: return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.statement())
            if res.error: return res
            cases.append((condition, expr, False))
            all_cases = res.register(self.if_expr_b_or_c())
            if res.error: return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)
        return res.success((cases, else_case))

    def atom(self):
        res = ParseResult()
        tok = self.curr_tok
        if tok.type in (TT_INT, TT_FLOAT):
            self.increment()
            return res.success(NumberNodes(tok))
        
        elif tok.type == TT_STRING:
            self.increment()
            return res.success(StringNodes(tok))

        elif tok.type == TT_IDENTIFIER:
            self.increment()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            self.increment()
            expr = res.register(self.expr())
            if res.error: return res
            if self.curr_tok.type == TT_RPAREN:
                self.increment()
                return res.success(expr)
            else:
                return res.failure(
                InvalidSyntaxError(
                    self.curr_tok.pos_start, self.curr_tok.pos_end, "Expected ')'"
                )
            )
        
        elif tok.type == TT_LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error: return res
            return res.success(list_expr)

        elif tok.matches(TT_KEYWORD, 'if'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        elif tok.matches(TT_KEYWORD, 'for'):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)

        elif tok.matches(TT_KEYWORD, 'while'):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)

        elif tok.matches(TT_KEYWORD, 'func'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        return res.failure(
            InvalidSyntaxError(
                tok.pos_start, tok.pos_end, "Expected int, float, identifier '+', '-' or '('"
            ), self.register_count
        )

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: return res
        if self.curr_tok.type == TT_LPAREN:
            self.increment()
            arg_nodes = []
            if self.curr_tok.type == TT_RPAREN:
                self.increment()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(
                    InvalidSyntaxError(
                    self.curr_tok.pos_start, self.curr_tok.pos_end, "Expected int, float, identifier, 'var', or ')'"
                    ))
                while self.curr_tok.type == TT_COMMA:
                    self.increment()
                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res
                if self.curr_tok.type != TT_RPAREN:
                    return  res.failure(
                        InvalidSyntaxError(
                        self.curr_tok.pos_start, self.curr_tok.pos_end, "Expected ')'"
                    ))
                self.increment()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)
    

    def power(self):
        return self.bin_op(self.call, (TT_POW, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.curr_tok
        if tok.type in (TT_PLUS, TT_MINUS):
            self.increment()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryNode(tok, factor))
        if tok.type == TT_NOT:
            self.increment()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryNode(tok, factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_MOD, TT_AT))

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bitwise_expr(self):
        return self.bin_op(self.arith_expr, (TT_AND, TT_OR, TT_XOR))

    def comp_expr(self):
        res = ParseResult()

        if self.curr_tok.matches(TT_KEYWORD, 'not'):
            op_tok = self.curr_tok
            self.increment()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryNode(op_tok, node))
		
        node = res.register(self.bin_op(self.bitwise_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
		
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.curr_tok.pos_start, self.curr_tok.pos_end,
                    "Expected int, float, identifier, '+', '-', '(' or 'not'"
            ), self.register_count)

        return res.success(node)

    def expr(self):
        res = ParseResult()
        if self.curr_tok.matches(TT_KEYWORD, 'assign'):
            self.increment()
            if self.curr_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(self.curr_tok.pos_start, self.curr_tok.pos_end, "Expected Identifier"))
            var_name = self.curr_tok
            self.increment()
            if self.curr_tok.type != TT_EQUAL:
                return res.failure(InvalidSyntaxError(self.curr_tok.pos_start, self.curr_tok.pos_end, "Expected '='"))
            self.increment()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        elif self.curr_tok.type == TT_DOL:
            self.increment()
            if self.curr_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(self.curr_tok.pos_start, self.curr_tok.pos_end, "Expected Identifier"))
            var_name = self.curr_tok
            self.increment()
            if self.curr_tok.type == TT_AT:
                self.increment()
                index = res.register(self.expr())
                if res.error: return res
                if self.curr_tok.type != TT_EQUAL:
                    return res.failure(InvalidSyntaxError(self.curr_tok.pos_start, self.curr_tok.pos_end, "Expected '='"))
                self.increment()
                expr = res.register(self.expr())
                if res.error: return res
                return res.success(ListReAssignNode(var_name, index, expr))

            if self.curr_tok.type != TT_EQUAL:
                return res.failure(InvalidSyntaxError(self.curr_tok.pos_start, self.curr_tok.pos_end, "Expected '='"))
            self.increment()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarReAssignNode(var_name, expr))


        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, 'and'), (TT_KEYWORD, 'or'))))
        if res.error:
            return res.failure(
                InvalidSyntaxError(self.curr_tok.pos_start, self.curr_tok.pos_end, "Expected 'assign', int, float, identifier, '+', '-', '(' or ')'"), self.register_count
                )
        return res.success(node)

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a
        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res
        while self.curr_tok.type in ops or ((self.curr_tok.type, self.curr_tok.value) in ops):
            op_tok = self.curr_tok
            self.increment()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)
        return res.success(left)