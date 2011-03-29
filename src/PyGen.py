from py2 import ast


class PyGenState(object):
    
    def __init__(self, **kwargs):
        self.kw = kwargs.keys()
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

class PyGen(object):

    def __init__(self, options=None, **kwargs):
        if options is None:
            self.opts = object()
        else:
            self.opts = options
        for k, v in kwargs.iteritems():
            setattr(self.opts, k, v)
        self.indent = 0
        self.code = []
        self.state_stack = []
        self.comment_stack = []
    
    def getCode(self):
        return "\n".join(self.code)

    def getIndent(self):
        return '    ' * self.indent

    def pushState(self):
        self.state_stack.append(PyGenState(
            code=self.code,
            indent=self.indent,
        ))
        self.code = []
        self.indent = 0

    def popState(self):
        self.pushState()
        old_state = self.state_stack.pop()
        state = self.state_stack.pop()
        for k in state.kw:
            setattr(self, k, getattr(state, k))
        return old_state

    def pushComment(self, node):
        if isinstance(node, ast.Node):
            if node.comments:
                comment = node.comments
                node.comments = None
                if isinstance(comment, basestring):
                    self.comment_stack.append(comment)
                else:
                    self.comment_stack += comment
        else:
            if isinstance(node, basestring):
                self.comment_stack.append(node)
            else:
                self.comment_stack += node

    def popComment(self, idx=0):
        # FIFO by default
        return self.comment_stack.pop(idx)

    def dispatch(self, node, add_comment=False):
        if node is None:
            return None
        if isinstance(node, ast.EmptyNode):
            self.addComment(node)
            return None
        method = "ast%s" % node.__class__.__name__
        if not hasattr(self, method):
            print 'dispatch:', method, node
        code = getattr(self, method)(node)
        if add_comment:
            self.addComment(node)
        return code

    def addCode(self, code, newline=True, checkComment=True):
        if checkComment:
            self.addComment()
        if code is not None:
            if isinstance(code, basestring):
                if newline:
                    if code.strip() == '':
                        self.code.append('')
                    else:
                        self.code.append("%s%s" % (self.getIndent(), code))
                else:
                    self.code[-1] += code
            else:
                for c in code:
                    self.addCode(c, checkComment=checkComment)

    def addDocCode(self, doc):
        if doc:
            lines = doc.split("\n")
            if len(lines) == 1:
                self.addCode('"""%s"""' % doc.strip(), checkComment=False)
            elif len(lines) > 1:
                self.addCode('"""%s' % lines[0].strip(), checkComment=False)
                for line in lines[1:-1]:
                    self.addCode(line.rstrip(), checkComment=False)
                self.addCode("%s" % lines[-1].rstrip(), checkComment=False)
                self.addCode('"""', checkComment=False)
        self.addComment()


    def addCommentCode(self, comment):
        if isinstance(comment, list):
            for c in comment:
                self.addCommentCode(c)
            return
        if isinstance(comment, basestring):
            lines = comment.split("\n")
            if len(lines) == 1:
                self.addCode('# %s' % comment.strip(), checkComment=False)
            elif len(lines) > 1:
                self.addCode('# %s' % lines[0].strip(), checkComment=False)
                for line in lines[1:-1]:
                    self.addCode('# %s' % line.rstrip(), checkComment=False)
                self.addCode('# %s' % lines[-1].rstrip(), checkComment=False)
                self.addCode('', checkComment=False)

    def addComment(self, *nodes):
        while len(self.comment_stack) > 0:
            self.addCommentCode(self.popComment())
        for node in nodes:
            if node.comments is not None:
                while len(node.comments):
                    comment = node.comments.pop(0)
                    self.addCommentCode(comment)

    def par_expr(self, node, code, cls=None):
        if (
            isinstance(node, ast.Name)
            or isinstance(node, ast.Const)
            or isinstance(node, ast.UnaryAdd)
            or isinstance(node, ast.UnarySub)
            or isinstance(node, ast.CallFunc)
            or isinstance(node, ast.Getattr)
            or isinstance(node, ast.Subscript)
        ):
            return code
        if ast is not None:
            if node.__class__ is cls:
                return code
        return "(%s)" % code

    def astAdd(self, node):
        left = self.par_expr(node.left, self.dispatch(node.left), ast.Add)
        right = self.par_expr(node.right, self.dispatch(node.right), ast.Add)
        return '%s + %s' % (left, right)

    def astAnd(self, node):
        code = []
        for n in node.nodes:
            code.append(self.dispatch(n))
        return ' and '.join(code)

    def astAssert(self, node):
        test = self.dispatch(node.test)
        fail = self.dispatch(node.fail)
        if fail is None:
            self.addCode('assert %s' % (test, ))
        else:
            self.addCode('assert %s, %s' % (test, fail))

    def astAssign(self, node):
        idx = len(self.code)
        line = []
        for dst in node.nodes:
            code = self.dispatch(dst)
            if code is None:
                raise TypeError("astAssign code is None for %s" % dst)
            self.addCode(code)
        self.addCode(self.dispatch(node.expr))
        # Glue the first two lines
        first_line = self.code[idx] + self.code[idx + 1].lstrip()
        self.code[idx] = first_line
        self.code.pop(idx + 1)
        self.addComment(node, *node.nodes)

    def astAssAttr(self, node):
        op = None
        if node.flags == 'OP_ASSIGN':
            op = '='
        if op is None:
            raise TypeError("astAssAttr '%s'" % op)
        expr = self.dispatch(node.expr)
        if isinstance(node.attrname, basestring):
            attrname = node.attrname
        else:
            attrname = self.dispatch(node.attrname)
        return "%s.%s %s " % (expr, attrname, op)

    def astAssName(self, node):
        op = None
        if node.flags == 'OP_ASSIGN':
            op = '='
        if op is None:
            raise TypeError("astAssName '%s'" % op)
        return "%s %s " % (node.name, op)

    def astAssTuple(self, node):
        nodes = [n.name for n in node.nodes]
        if len(nodes) == 1:
            return "%s, = " % nodes[0]
        return "%s = " % ", ".join(nodes)

    def astAugAssign(self, node):
        dst = self.dispatch(node.node)
        src = self.dispatch(node.expr)
        return "%s %s %s" % (dst, node.op, src)

    def astBitand(self, node):
        code = [self.par_expr(n, self.dispatch(n)) for n in node.nodes]
        return " & ".join(code)

    def astBitor(self, node):
        code = [self.par_expr(n, self.dispatch(n)) for n in node.nodes]
        return " | ".join(code)

    def astBitxor(self, node):
        code = [self.par_expr(n, self.dispatch(n)) for n in node.nodes]
        return " ^ ".join(code)

    def astBreak(self, node):
        return "break"

    def astCallFunc(self, node):
        indent = self.indent
        self.pushState()
        self.addCode(self.dispatch(node.node))
        self.addCode("(", False)
        idx = 0
        for arg in node.args:
            idx += 1
            code = self.dispatch(arg)
            if code is not None:
                self.addCode(code, False)
                if idx != len(node.args):
                    self.addCode(", ", False)
        if node.star_args:
            self.addCode(", *", False)
            self.addCode(self.dispatch(node.star_args), False)
        if node.dstar_args:
            self.addCode(", **", False)
            self.addCode(self.dispatch(node.dstar_args), False)
        self.addCode(")", False)
        state = self.popState()
        if len(state.code) == 0:
            return state.code[0]
        for line in state.code:
            if line and line[-1] == ':':
                return state.code
        return "".join(state.code)

    def astClass(self, node):
        bases = tuple(node.bases)
        if len(bases) == 1:
            bases = "(%s)" % bases[0]
        else:
            bases = "(%s)" % ', '.join(list(bases))
        self.addCode("")
        self.addCode("")
        self.addCode(
            "class %s%s:" % (
                node.name,
                bases,
            ),
        )
        self.indent += 1
        self.addDocCode(node.doc)
        self.addComment(node)
        self.dispatch(node.code)
        self.indent -= 1

    def astCompare(self, node):
        self.pushState()
        self.addCode(self.dispatch(node.expr))
        for op in node.ops:
            self.addCode(" %s " % op[0], False)
            self.addCode(self.dispatch(op[1]), False)
        state = self.popState()
        code = self.par_expr(state.code, "%s" % " ".join(state.code))
        return " ".join(state.code)

    def astConst(self, node):
        return repr(node.value)

    def astContinue(self, node):
        return "continue"

    def astDiscard(self, node):
        self.addCode(self.dispatch(node.expr))
        self.addComment(node)

    def astDiv(self, node):
        left = self.par_expr(node.left, self.dispatch(node.left), ast.Div)
        right = self.par_expr(node.right, self.dispatch(node.right), ast.Div)
        return '%s / %s' % (left, right)

    def astFor(self, node):
        self.addCode(
            "for %s in %s:" % (
                node.assign.name,
                self.dispatch(node.list),
            ),
        )
        self.indent += 1
        if node.comments:
            self.pushComment(node.comments[0])
        self.addCode(self.dispatch(node.body))
        self.addComment(node.body)
        self.indent -= 1
        if node.else_:
            self.addCode("else:")
            self.indent += 1
            if node.comments:
                self.pushComment(node.comments[1])
            self.addCode(self.dispatch(node.else_))
            self.addComment(node.else_)
            self.indent -= 1
        if node.comments:
            self.pushComment(node.comments[2])

    def astFrom(self, node):
        self.addCode(
            "from %s import (%s,)" % (
                node.modname,
                ', '.join(node.names),
            ),
        )
        self.addComment(node)

    def astFunction(self, node):
        args = [self.dispatch(a) for a in node.argnames]
        idx = len(args)
        if node.defaults:
            defaults = [self.dispatch(d) for d in node.defaults]
        else:
            defaults = []
        if node.flags & ast.CO_VARKEYWORDS:
            args[-1] = '**%s' % args[-1]
            idx -= 1
        if node.flags & ast.CO_VARARGS:
            args[-1] = '*%s' % args[-1]
            idx -= 1
        while defaults:
            idx -= 1
            args[idx]  = "%s=%s" % (args[idx], defaults.pop())
        args = ', '.join(args)
        self.addCode("")
        self.addCode(
            "def %s(%s):" % (
                node.name,
                args,
            ),
        )
        self.indent += 1
        self.addDocCode(node.doc)
        self.addComment(node)
        self.dispatch(node.code)
        self.addComment(node.code)
        self.indent -= 1

    def astGetattr(self, node):
        if isinstance(node.attrname, basestring):
            attrname = node.attrname
        else:
            attrname = self.dispatch(node.attrname)
        return "%s.%s" % (
            self.dispatch(node.expr), 
            attrname,
        )

    def astIf(self, node):
        ifstr = 'if'
        for test in node.tests:
            condition, code = test
            idx = len(self.code)
            self.addCode("%s (" % ifstr)
            self.indent += 1
            self.addCode(self.dispatch(condition))
            self.indent -= 1
            self.addCode("):")
            if node.comments:
                comment = node.comments.pop(0)
                self.pushComment(comment[0])
                self.pushComment(comment[1])
            elif idx == len(self.code) - 3:
                # Just one line
                line = "%s %s:" % (
                    ifstr,
                    self.code[-2].strip(),
                )
                if len(line) < 80:
                    self.code.pop()
                    self.code.pop()
                    self.code.pop()
                    self.addCode(line.lstrip())
            self.indent += 1
            self.addComment(condition)
            self.addCode(self.dispatch(code))
            self.addComment(code)
            self.indent -= 1
            ifstr = 'elif'
        if node.else_:
            self.addCode("else:")
            if node.comments:
                comment = node.comments.pop(0)
                self.pushComment(comment)
            self.indent += 1
            self.addCode(self.dispatch(node.else_))
            self.addComment(node.else_)
            self.indent -= 1
        while node.comments:
            comment = node.comments.pop(0)
            self.pushComment(comment)

    def astIfExp(self, node):
        test = self.dispatch(node.test)
        then = self.dispatch(node.then)
        else_ = self.dispatch(node.else_)
        return "%s if %s else %s" % (test, then, else_)

    def astInvert(self, node):
        return "~%s" % self.par_expr(node.expr, self.dispatch(node.expr))

    def astLeftShift(self, node):
        left = self.par_expr(node.left, self.dispatch(node.left))
        right = self.par_expr(node.right, self.dispatch(node.right))
        return '%s << %s' % (left, right)

    def astList(self, node):
        return "[%s]" % ', '.join([str(self.dispatch(i)) for i in node.nodes])

    def astMod(self, node):
        left = self.par_expr(node.left, self.dispatch(node.left))
        right = self.par_expr(node.right, self.dispatch(node.right))
        return '%s %% %s' % (left, right)

    def astModule(self, node):
        self.addDocCode(node.doc)
        self.addComment(node)
        self.dispatch(node.node)

    def astMul(self, node):
        left = self.par_expr(node.left, self.dispatch(node.left), ast.Mul)
        right = self.par_expr(node.right, self.dispatch(node.right), ast.Mul)
        return '%s * %s' % (left, right)

    def astName(self, node):
        self.pushComment(node)
        return node.name

    def astNot(self, node):
        return "not %s" % self.par_expr(node.expr, self.dispatch(node.expr))

    def astOr(self, node):
        code = []
        for n in node.nodes:
            code.append(self.par_expr(n, self.dispatch(n)))
        return ' or '.join(code)

    def astPass(self, node):
        return 'pass'

    def astRaise(self, node):
        expr1 = self.dispatch(node.expr1)
        expr2 = self.dispatch(node.expr2)
        expr3 = self.dispatch(node.expr3)
        if node.expr3 is not None:
            return "raise %s, %s, %s" % (expr1, expr2, expr3)
        if node.expr2 is not None:
            return "raise %s, %s" % (expr1, expr2)
        return "raise %s" % (expr1, )

    def astReturn(self, node):
        if node.value is None:
            self.addCode("return")
        else:
            self.addCode("return ")
            self.addCode(self.dispatch(node.value), False)

    def astRightShift(self, node):
        left = self.par_expr(node.left, self.dispatch(node.left))
        right = self.par_expr(node.right, self.dispatch(node.right))
        return '%s >> %s' % (left, right)

    def astStmt(self, node):
        self.addComment(node)
        if len(node.nodes) == 0:
            self.addCode("pass # astStmt: %r" % [node, node.lineno])
            return
        for n in node.nodes:
            if n is not None:
                #if isinstance(n, list):
                #    print node
                #    assert False
                self.addCode(self.dispatch(n))
                self.addComment(n)

    def astSub(self, node):
        left = self.par_expr(node.left, self.dispatch(node.left), ast.Sub)
        right = self.par_expr(node.right, self.dispatch(node.right), ast.Sub)
        return '%s - %s' % (left, right)

    def astSubscript(self, node):
        expr = self.dispatch(node.expr)
        subs = [self.dispatch(s) for s in node.subs]
        if node.flags == 'OP_APPLY':
            sub = "".join(["[%s]" % s for s in subs])
            return "%s%s" % (expr, sub)
        elif node.flags == 'OP_ASSIGN':
            sub = "".join(["[%s]" % s for s in subs])
            return "%s%s = " % (expr, sub)
        raise TypeError("Cannot handle flag %s" % node.flags)

    def astTryExcept(self, node):
        self.addComment(node)
        self.addCode("try:")
        self.indent += 1
        self.addCode(self.dispatch(node.body))
        self.addComment(node.body)
        self.indent -= 1
        if node.handlers:
            for cls, name, stmt in node.handlers:
                self.addCode("except %s, %s:" % (cls.name, name.name))
                self.indent += 1
                self.addCode(self.dispatch(stmt))
                self.indent -= 1
        if node.else_:
            self.addCode("else:")
            self.indent += 1
            self.addCode(self.dispatch(node.else_))
            self.addComment(node.else_)
            self.indent -= 1

    def astTryFinally(self, node):
        self.dispatch(node.body)
        if node.final:
            self.addCode("finally:")
            self.indent += 1
            self.addCode(self.dispatch(node.final))
            self.addComment(node.final)
            self.indent -= 1

    def astTuple(self, node):
        code = []
        for n in node.nodes:
            code.append(self.dispatch(n))
        return '(%s)' % ', '.join(code)

    def astUnaryAdd(self, node):
        return '+%s' % self.par_expr(node.expr, self.dispatch(node.expr))

    def astUnarySub(self, node):
        return '-%s' % self.par_expr(node.expr, self.dispatch(node.expr))

    def astWhile(self, node):
        idx = len(self.code)
        self.addCode("while (")
        self.indent += 1
        self.addCode(self.dispatch(node.test))
        self.indent -= 1
        self.addCode("):")
        if idx == len(self.code) - 3:
            # Just one line
            line = "while %s:" % (
                self.code[-2].strip(),
            )
            if len(line) < 80:
                self.code.pop()
                self.code.pop()
                self.code.pop()
                self.addCode(line.lstrip())
        self.indent += 1
        self.addCode(self.dispatch(node.body))
        self.indent -= 1
        if node.else_ is not None:
            self.addCode("else:")
            self.indent += 1
            self.addCode(self.dispatch(node.else_))
            self.indent -= 1

    def astXor(self, node):
        left = self.par_expr(node.left, self.dispatch(node.left))
        right = self.par_expr(node.right, self.dispatch(node.right))
        return '%s ^ %s' % (left, right)
