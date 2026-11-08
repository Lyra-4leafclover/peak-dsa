"""Plain-English meaning of every line of Python, built from the syntax tree.

line_meanings(src) -> {"12": {"say": str, "order": [str], "tip": str}, ...}
Code inside `backticks` is shown as code by the page.
"""
import ast
import re


def _c(x, n=44):
    s = x if isinstance(x, str) else ast.unparse(x)
    s = ' '.join(s.split()).replace('`', "'")
    if len(s) > n:
        s = s[:n - 1] + '…'
    return f'`{s}`'


def _cap(s):
    return s[:1].upper() + s[1:] if s else s


def _and(items):
    items = list(items)
    if len(items) <= 1:
        return ''.join(items)
    return ', '.join(items[:-1]) + ' and ' + items[-1]


def _fname(f):
    if isinstance(f, ast.Name):
        return None, f.id
    if isinstance(f, ast.Attribute):
        return f.value, f.attr
    return None, None


ERRORS = {
    'ValueError': 'a value of the right type but the wrong kind, like `int("hello")`',
    'KeyError': 'looking up a key that isn\'t in the dictionary',
    'IndexError': 'asking for a position past the end of a list',
    'ZeroDivisionError': 'dividing by zero',
    'TypeError': 'mixing things that don\'t fit together, like adding text to a number',
    'AttributeError': 'using something the object doesn\'t have',
    'NameError': 'using a variable that doesn\'t exist yet',
    'Exception': 'almost any kind of error',
    'RecursionError': 'a function calling itself too many times',
    'StopIteration': 'asking for the next item when there are none left',
}

OPS = {ast.Eq: 'is equal to', ast.NotEq: 'is not equal to', ast.Lt: 'is less than', ast.LtE: 'is less than or equal to',
       ast.Gt: 'is greater than', ast.GtE: 'is greater than or equal to', ast.In: 'is in', ast.NotIn: 'is not in',
       ast.Is: 'is', ast.IsNot: 'is not'}


class Explainer:
    def __init__(self, tree):
        self.funcs, self.classes, self.seen = set(), set(), set()
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.funcs.add(n.name)
            elif isinstance(n, ast.ClassDef):
                self.classes.add(n.name)

    # ----- pieces of expressions -----
    def q(self, x, n=44):
        if id(x) in self.seen:
            return 'that text' if isinstance(x, ast.JoinedStr) else 'the result'
        return _c(x, n)

    def snip(self, n):
        s = ' '.join(ast.unparse(n).split())
        if len(s) > 32 and isinstance(n, ast.Call):
            return f'`{ast.unparse(n.func)}(…)`'
        if isinstance(n, ast.BinOp) and id(n.left) in self.seen:
            left = ast.unparse(n.left)
            if s.startswith(left):
                return _c('… ' + s[len(left):].strip(), 32)
        return _c(s, 32)

    def range_words(self, a):
        if len(a) == 1:
            return f'0 up to {_c(a[0])} − 1'
        if len(a) == 2:
            return f'{_c(a[0])} up to {_c(a[1])} − 1'
        return f'{_c(a[0])} towards {_c(a[1])} in steps of {_c(a[2])} (stopping before {_c(a[1])})'

    def call(self, n):
        obj, name = _fname(n.func)
        a = n.args
        A = [self.q(x) for x in a]
        kw = {k.arg: k.value for k in n.keywords if k.arg}
        o = self.q(obj) if obj is not None else None
        mod = obj.id if isinstance(obj, ast.Name) else None
        if obj is None or mod in ('heapq', 'math', 'random', 'collections', 'np', 'numpy'):
            if name == 'print':
                if len(a) == 1 and isinstance(a[0], ast.JoinedStr):
                    vals = [_c(v.value, 24) for v in a[0].values if isinstance(v, ast.FormattedValue)]
                    return f'prints a line of text on the screen, with {_and(vals)} filled in' if vals else f'prints {A[0]} on the screen'
                return f'prints {_and(A)} on the screen' if A else 'prints an empty line'
            if name == 'input':
                if A and A[0] == 'that text':
                    return 'shows that text as a question and waits for you to type something. What you type comes back as text'
                return (f'shows the message {A[0]} and waits for you to type something. What you type comes back as text'
                        if A else 'waits for you to type something. What you type comes back as text')
            if name == 'int':
                return f'turns {A[0]} into a whole number' if A else 'makes the number 0'
            if name == 'float':
                return f'turns {A[0]} into a decimal number' if A else 'makes the number 0.0'
            if name == 'str':
                return f'turns {A[0]} into text' if A else 'makes empty text'
            if name == 'bool':
                return f'turns {A[0]} into True or False' if A else 'makes False'
            if name in ('list', 'set', 'tuple', 'dict'):
                kind = {'list': 'list', 'set': 'set (no duplicates)', 'tuple': 'tuple', 'dict': 'dictionary'}[name]
                return f'makes a {kind} out of {A[0]}' if A else f'makes a new empty {kind}'
            if name == 'len':
                return f'counts how many items are in {A[0]}' if A else None
            if name == 'range':
                return f'counts {self.range_words(a)}' if a else None
            if name == 'sorted' and A:
                s = f'makes a sorted copy of {A[0]}'
                if 'key' in kw:
                    s += f', ordered by {_c(kw["key"])}'
                return s + (', biggest first' if 'reverse' in kw else ', smallest first')
            if name == 'reversed' and A:
                return f'goes through {A[0]} backwards'
            if name == 'enumerate' and A:
                return f'pairs every item of {A[0]} with its position (0, 1, 2, …)'
            if name == 'zip' and A:
                return f'pairs up the items of {_and(A)} side by side'
            if name == 'sum' and A:
                return f'adds up everything in {A[0]}'
            if name in ('min', 'max') and A:
                w = 'smallest' if name == 'min' else 'biggest'
                return f'finds the {w} item in {A[0]}' if len(A) == 1 else f'picks the {w} of {_and(A)}'
            if name == 'abs' and A:
                return f'gives the size of {A[0]} without its minus sign'
            if name == 'round' and A:
                return f'rounds {A[0]} to the nearest whole number' if len(A) == 1 else f'rounds {A[0]} to {A[1]} decimal places'
            if name == 'any' and A:
                return f'is True if at least one item in {A[0]} is true'
            if name == 'all' and A:
                return f'is True only if every item in {A[0]} is true'
            if name == 'isinstance' and len(A) == 2:
                return f'checks whether {A[0]} is a {A[1]}'
            if name == 'ord' and A:
                return f'gives the number code of the character {A[0]}'
            if name == 'chr' and A:
                return f'gives the character whose number code is {A[0]}'
            if name == 'map' and len(A) == 2:
                return f'applies {A[0]} to every item of {A[1]}'
            if name == 'filter' and len(A) == 2:
                return f'keeps only the items of {A[1]} for which {A[0]} is true'
            if name == 'divmod' and len(A) == 2:
                return f'divides {A[0]} by {A[1]} and gives back both the whole part and the remainder'
            if name == 'type' and len(A) == 1:
                return f'tells you what type {A[0]} is'
            if name == 'open' and A:
                return f'opens the file {A[0]}'
            if name in ('exit', 'quit'):
                return 'stops the program'
            if name == 'next' and A:
                return f'gets the next item from {A[0]}'
            if name == 'heappush' and len(A) == 2:
                return f'adds {A[1]} to the heap {A[0]}. The smallest item always stays on top'
            if name == 'heappop' and A:
                return f'removes the smallest item from the heap {A[0]} and gives it back'
            if name == 'heapify' and A:
                return f'rearranges {A[0]} into a heap, with the smallest item on top'
            if name in ('nlargest', 'nsmallest') and len(A) == 2:
                return f'finds the {A[0]} {"biggest" if name == "nlargest" else "smallest"} items in {A[1]}'
            if name == 'randint' and len(A) == 2:
                return f'picks a random whole number from {A[0]} to {A[1]}'
            if name == 'choice' and A:
                return f'picks a random item from {A[0]}'
            if name == 'shuffle' and A:
                return f'mixes {A[0]} into a random order'
            if name == 'random' and mod == 'random':
                return 'picks a random decimal number between 0 and 1'
            if name == 'sqrt' and A:
                return f'works out the square root of {A[0]}'
            if name in ('floor', 'ceil') and A:
                return f'rounds {A[0]} {"down" if name == "floor" else "up"} to a whole number'
            if name == 'deque':
                return f'makes a queue (a line you can add to or take from at both ends) from {A[0]}' if A else 'makes a new empty queue (a line you can add to or take from at both ends)'
            if name == 'defaultdict' and A:
                start = {'int': '0', 'list': 'an empty list', 'set': 'an empty set', 'str': 'empty text'}.get(ast.unparse(a[0]), f'{A[0]}()')
                return f'makes a dictionary that starts any missing key at {start} automatically'
            if name == 'Counter':
                return f'counts how many times each item appears in {A[0]}' if A else 'makes an empty counter'
            if name == 'super':
                return 'gets the parent class, so its version of a method can be used'
            if name in self.classes and obj is None:
                return f'makes a new {name} object from the {name} blueprint' + (f', passing in {_and(A)}' if A else '')
            if name in self.funcs and obj is None:
                return (f'runs the function {_c(name)} with {_and(A)}' if A else f'runs the function {_c(name)}') + \
                    '. Python jumps into its code, then comes back here with its answer'
            if mod in ('np', 'numpy'):
                if name in ('array', 'asarray') and A:
                    return f'makes a numpy array (a fast grid of numbers) from {A[0]}'
                if name in ('zeros', 'ones') and A:
                    return f'makes a numpy array of shape {A[0]} filled with {"0" if name == "zeros" else "1"}s'
                if name == 'arange' and A:
                    return f'makes a numpy array of the numbers {self.range_words(a)}'
        if obj is not None:
            if isinstance(obj, ast.Name) and obj.id == 'self' and name in self.funcs:
                return (f'runs this object\'s own method {_c(name)} with {_and(A)}' if A else f'runs this object\'s own method {_c(name)}') + \
                    '. Python jumps into it, then comes back here with its answer'
            m = {
                'append': lambda: f'adds {A[0]} to the end of {o}',
                'appendleft': lambda: f'adds {A[0]} to the front of {o}',
                'extend': lambda: f'adds every item of {A[0]} to the end of {o}',
                'insert': lambda: f'puts {A[1]} into {o} at position {A[0]}',
                'popleft': lambda: f'removes the first item from {o} and gives it back',
                'remove': lambda: f'removes the first {A[0]} it finds in {o}',
                'discard': lambda: f'removes {A[0]} from the set {o} if it\'s there',
                'add': lambda: f'adds {A[0]} to the set {o} (duplicates are ignored)',
                'index': lambda: f'finds the position of {A[0]} in {o}',
                'count': lambda: f'counts how many times {A[0]} appears in {o}',
                'sort': lambda: f'sorts {o} in place, ' + ('biggest first' if 'reverse' in kw else 'smallest first'),
                'reverse': lambda: f'flips the order of {o}',
                'copy': lambda: f'makes a copy of {o}',
                'clear': lambda: f'empties {o}',
                'keys': lambda: f'gives all the keys of {o}',
                'values': lambda: f'gives all the values of {o}',
                'items': lambda: f'gives every key together with its value from {o}',
                'split': lambda: f'cuts the text {o} into a list of pieces at every {A[0]}' if A else f'cuts the text {o} into a list of words',
                'join': lambda: f'glues the items of {A[0]} together into one piece of text, with {o} between them',
                'strip': lambda: f'removes extra spaces from both ends of {o}',
                'lower': lambda: f'makes a lowercase copy of {o}',
                'upper': lambda: f'makes an uppercase copy of {o}',
                'replace': lambda: f'makes a copy of {o} with every {A[0]} replaced by {A[1]}',
                'startswith': lambda: f'checks whether {o} starts with {A[0]}',
                'endswith': lambda: f'checks whether {o} ends with {A[0]}',
                'isdigit': lambda: f'checks whether {o} is made only of digits',
                'isalpha': lambda: f'checks whether {o} is made only of letters',
                'isalnum': lambda: f'checks whether {o} is made only of letters and digits',
                'isspace': lambda: f'checks whether {o} is only spaces',
                'find': lambda: f'finds the position of {A[0]} in {o} (or -1 if it\'s not there)',
                'format': lambda: f'fills values into the text {o}',
                'setdefault': lambda: f'looks up {A[0]} in {o}, adding it with {A[1]} first if it\'s missing',
            }
            if name == 'pop':
                if not A:
                    return f'removes the last item from {o} and gives it back'
                if isinstance(a[0], ast.Constant) and a[0].value == 0:
                    return f'removes the first item from {o} and gives it back'
                return f'removes {A[0]} from {o} and gives it back'
            if name == 'get' and A:
                return f'looks up {A[0]} in {o}, or gives {A[1] if len(A) > 1 else "None"} if it isn\'t there'
            try:
                if name in m:
                    return m[name]()
            except IndexError:
                pass
        return None

    def clause(self, t):
        """A condition as a plain sentence, e.g. '`x` is less than `5`'."""
        if isinstance(t, ast.Compare):
            parts = [t.left] + list(t.comparators)
            if len(t.ops) > 1 and all(isinstance(op, ast.Eq) for op in t.ops):
                return f'{_and(_c(p) for p in parts)} are all equal'
            out = []
            for i, op in enumerate(t.ops):
                L, R = parts[i], parts[i + 1]
                if isinstance(R, ast.Constant) and R.value is None and isinstance(op, (ast.Is, ast.IsNot)):
                    out.append(f'{_c(L)} {"is None (nothing)" if isinstance(op, ast.Is) else "is not None (it has a value)"}')
                else:
                    out.append(f'{_c(L)} {OPS.get(type(op), "compares to")} {_c(R)}')
            return ', and '.join(out)
        if isinstance(t, ast.BoolOp):
            cl = [self.clause(v) for v in t.values]
            if isinstance(t.op, ast.Or):
                return 'at least one of these is true: ' + '; '.join(cl[:-1]) + '; or ' + cl[-1]
            return 'all of these are true: ' + '; '.join(cl[:-1]) + '; and ' + cl[-1]
        if isinstance(t, ast.UnaryOp) and isinstance(t.op, ast.Not):
            if isinstance(t.operand, (ast.Name, ast.Attribute, ast.Subscript)):
                return f'{_c(t.operand)} is empty, zero, None or False'
            return f'{_c(t.operand)} is NOT true'
        if isinstance(t, (ast.Name, ast.Attribute, ast.Subscript)):
            return f'{_c(t)} has a value (it isn\'t empty, zero, None or False)'
        if isinstance(t, ast.Call):
            return f'{_c(t)} gives back a true answer'
        if isinstance(t, ast.Constant):
            return f'{_c(t)} is true'
        return f'{_c(t)} is true'

    def phrase(self, n):
        """What a single expression piece does, or None if it's too simple to mention."""
        if isinstance(n, ast.Call):
            return self.call(n) or f'calls {_c(n.func)}'
        if isinstance(n, ast.JoinedStr):
            vals = [_c(v.value, 24) for v in n.values if isinstance(v, ast.FormattedValue)]
            return f'builds a piece of text and fills in {_and(vals)}' if vals else None
        if isinstance(n, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
            g = n.generators[0]
            kind = {ast.ListComp: 'a list', ast.SetComp: 'a set', ast.GeneratorExp: 'a sequence', ast.DictComp: 'a dictionary'}[type(n)]
            elt = f'{_c(n.key, 24)}: {_c(n.value, 24)}' if isinstance(n, ast.DictComp) else _c(n.elt, 30)
            s = f'builds {kind} by taking {elt} for each {_c(g.target)} in {_c(g.iter, 30)}'
            if g.ifs:
                s += f', but only when {self.clause(g.ifs[0])}'
            return s
        if isinstance(n, ast.IfExp):
            return f'picks {_c(n.body, 24)} if {self.clause(n.test)}, otherwise {_c(n.orelse, 24)}'
        if isinstance(n, ast.Compare):
            return f'checks whether {self.clause(n)}'
        if isinstance(n, ast.BoolOp):
            return f'checks whether {self.clause(n)}'
        if isinstance(n, ast.BinOp):
            L, R = self.q(n.left, 30), self.q(n.right, 30)
            return {
                ast.Add: f'adds {L} and {R}', ast.Sub: f'subtracts {R} from {L}', ast.Mult: f'multiplies {L} by {R}',
                ast.Div: f'divides {L} by {R}', ast.FloorDiv: f'divides {L} by {R} and drops the remainder (whole number result)',
                ast.Mod: f'gives the remainder after dividing {L} by {R}', ast.Pow: f'raises {L} to the power of {R}',
                ast.BitAnd: f'keeps only the bits that are on in both {L} and {R}', ast.BitOr: f'combines the on-bits of {L} and {R}',
                ast.BitXor: f'keeps the bits that differ between {L} and {R}', ast.LShift: f'shifts the bits of {L} left by {R}',
                ast.RShift: f'shifts the bits of {L} right by {R}',
            }.get(type(n.op))
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Slice):
            s, v = n.slice, _c(n.value, 24)
            if s.lower is None and s.upper is None and s.step is not None and ast.unparse(s.step) == '-1':
                return f'makes a reversed copy of {v}'
            if s.lower is None and s.upper is None and s.step is None:
                return f'makes a copy of {v}'
            if s.lower is None:
                return f'takes the first {_c(s.upper)} items of {v}'
            if s.upper is None:
                return f'takes everything in {v} from position {_c(s.lower)} onwards'
            return f'takes the items of {v} from position {_c(s.lower)} up to (not including) {_c(s.upper)}'
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.UnaryOp) and isinstance(n.slice.op, ast.USub) \
                and isinstance(n.slice.operand, ast.Constant) and n.slice.operand.value == 1:
            return f'takes the last item of {_c(n.value, 24)}'
        if isinstance(n, ast.Lambda):
            args = [x.arg for x in n.args.args]
            return f'makes a tiny nameless function that takes {_and(_c(x) for x in args) or "nothing"} and gives back {_c(n.body, 30)}'
        return None

    def steps(self, n):
        """Pieces of an expression in the order Python works them out (inside first)."""
        out = []
        if isinstance(n, (ast.Lambda, ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp, ast.JoinedStr)):
            kids = []
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'print' and \
                all(isinstance(x, (ast.JoinedStr, ast.Constant, ast.Name)) for x in n.args):
            kids = []
        elif isinstance(n, ast.Call):
            kids = list(n.args) + [k.value for k in n.keywords]
            if isinstance(n.func, ast.Attribute):
                kids = [n.func.value] + kids
        else:
            kids = list(ast.iter_child_nodes(n))
        for k in kids:
            if isinstance(k, ast.expr):
                out += self.steps(k)
        p = self.phrase(n)
        if p:
            out.append((n, p))
            self.seen.add(id(n))
        return out

    def order(self, steps):
        return [f'{self.snip(n)} {p}.' for n, p in steps]

    # ----- whole statements -----
    def target(self, t):
        if isinstance(t, ast.Subscript):
            return f'{_c(t.value)} at {_c(t.slice)}', 'slot'
        if isinstance(t, ast.Attribute):
            return _c(t), 'attr'
        return _c(t), 'name'

    def store(self, targets, v, ann=None):
        if len(targets) == 1 and isinstance(targets[0], ast.Tuple) and isinstance(v, ast.Tuple) and \
                sorted(ast.unparse(x) for x in targets[0].elts) == sorted(ast.unparse(x) for x in v.elts):
            return {'say': f'Swaps the values of {_and(_c(x) for x in targets[0].elts)} in one go. Python works out the whole right side first, then fills in the left side.'}
        if len(targets) == 1 and isinstance(targets[0], ast.Tuple):
            names = _and(_c(x) for x in targets[0].elts)
            st = self.steps(v)
            return {'say': f'Works out {_c(v)} and unpacks it into {names}: the first value goes into the first name, and so on.',
                    'order': self.order(st) if len(st) > 1 else []}
        where, kind = self.target(targets[0]) if len(targets) == 1 else (_and(_c(t) for t in targets), 'name')
        if kind == 'slot':
            into = f'puts it into {where}, replacing what was there'
        elif kind == 'attr':
            into = f'saves it as {where}, a value stored on the object'
        else:
            into = f'saves it in the variable {where}'
        st = self.steps(v)
        tip = f'The `: {ast.unparse(ann)}` part is only a label saying what type it should be. Python doesn\'t check it.' if ann is not None else ''
        if not st:
            if isinstance(v, ast.List) and not v.elts:
                say = f'Makes an empty list and {into}.'
            elif isinstance(v, ast.Dict) and not v.keys:
                say = f'Makes an empty dictionary (a lookup table of key → value pairs) and {into}.'
            elif isinstance(v, ast.List):
                say = f'Makes a list holding {_c(v)} and {into}.'
            elif isinstance(v, ast.Dict):
                say = f'Makes a dictionary (a lookup table of key → value pairs) and {into}.'
            elif isinstance(v, ast.Name):
                say = f'Takes the value of {_c(v)} and {into}.'
            else:
                say = f'Takes {_c(v)} and {into}.'
            return {'say': say, 'tip': tip}
        if len(st) == 1:
            return {'say': f'{_cap(st[0][1])}, then {into}.', 'tip': tip}
        return {'say': f'Works out {_c(v)}, then {into}.', 'order': self.order(st), 'tip': tip}

    def cond(self, t, lead):
        st = [x for x in self.steps(t) if not isinstance(x[0], (ast.Compare, ast.BoolOp))]
        return lead.format(self.clause(t)), self.order(st)

    def stmt(self, s, parent):
        if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef)):
            params = [x.arg for x in s.args.args if x.arg != 'self']
            in_cls = isinstance(parent, ast.ClassDef)
            what = 'a method (a function that belongs to this class)' if in_cls else 'a function (a reusable recipe)'
            ins = f' that takes {_and(_c(p) for p in params)}' if params else ' with no inputs'
            say = f'Defines {what} called {_c(s.name)}{ins}. Nothing inside runs yet: it only runs when the code calls {_c(s.name + "(...)")}.'
            tips = []
            if s.name == '__init__':
                tips.append('`__init__` is the setup recipe. It runs by itself every time a new object is made.')
            if in_cls and s.args.args and s.args.args[0].arg == 'self':
                tips.append('`self` is the object the method is working on.')
            for d in s.decorator_list:
                dn = ast.unparse(d)
                if re.match(r'(functools\.)?(lru_cache|cache)', dn):
                    tips.append(f'`@{dn}` makes Python remember answers it already worked out, so calling it again with the same inputs is instant.')
            if s.returns is not None or any(x.annotation is not None for x in s.args.args):
                tips.append('The `: type` and `-> type` parts are labels describing the inputs and answer. Python doesn\'t check them.')
            return {'say': say, 'tip': ' '.join(tips)}
        if isinstance(s, ast.ClassDef):
            base = [ast.unparse(b) for b in s.bases if ast.unparse(b) != 'object']
            say = f'Defines a class called {_c(s.name)}: a blueprint for making objects that keep their own data and functions together.'
            if base:
                say += f' It builds on {_and(_c(b) for b in base)}, so it gets everything that has too.'
            return {'say': say}
        if isinstance(s, ast.Return):
            if s.value is None:
                return {'say': 'Ends the function right here and goes back to the code that called it.'}
            st = self.steps(s.value)
            if not st:
                return {'say': f'Ends the function and hands back {_c(s.value)} to the code that called it.'}
            if len(st) == 1:
                return {'say': f'{_cap(st[0][1])}, then ends the function and hands that answer back to the code that called it.'}
            return {'say': f'Works out {_c(s.value)}, then ends the function and hands the answer back to the code that called it.', 'order': self.order(st)}
        if isinstance(s, ast.Assign):
            return self.store(s.targets, s.value)
        if isinstance(s, ast.AnnAssign):
            if s.value is None:
                return {'say': f'Says that {_c(s.target)} will hold a {_c(s.annotation)}. Nothing is stored yet.'}
            return self.store([s.target], s.value, s.annotation)
        if isinstance(s, ast.AugAssign):
            x, v = _c(s.target), _c(s.value)
            op = {ast.Add: f'Adds {v} to {x}', ast.Sub: f'Subtracts {v} from {x}', ast.Mult: f'Multiplies {x} by {v}',
                  ast.Div: f'Divides {x} by {v}', ast.FloorDiv: f'Divides {x} by {v} (dropping the remainder)',
                  ast.Mod: f'Replaces {x} with the remainder after dividing it by {v}'}.get(type(s.op), f'Updates {x} using {v}')
            short = f'`{ast.unparse(s.target)} = {ast.unparse(s.target)} {ast.unparse(ast.BinOp(s.target, s.op, s.value))[len(ast.unparse(s.target)) + 1:]}`'
            st = self.steps(s.value)
            return {'say': f'{op}. It\'s a short way of writing {short}.', 'order': self.order(st) if st else []}
        if isinstance(s, ast.If):
            src_line = self.lines[s.lineno - 1].lstrip()
            if re.match(r"__name__\s*==\s*['\"]__main__['\"]", ast.unparse(s.test)):
                return {'say': 'Checks whether this file is being run directly (not loaded into another file). Here it is, so the indented lines run.',
                        'tip': 'This is the usual "start here" line at the bottom of a Python program.'}
            lead = 'Otherwise (if the checks above were false), checks whether {}. If so, the indented lines below run.' if src_line.startswith('elif') \
                else 'Checks whether {}. If so, the indented lines below run. If not, Python skips them.'
            say, order = self.cond(s.test, lead)
            return {'say': say, 'order': order}
        if isinstance(s, ast.While):
            if isinstance(s.test, ast.Constant) and s.test.value is True:
                return {'say': 'Starts a loop that repeats the indented lines forever, until a `break` (or `return`) inside it stops it.'}
            say, order = self.cond(s.test, 'Repeats the indented lines again and again as long as {}. The check runs again before every round.')
            return {'say': say, 'order': order}
        if isinstance(s, ast.For):
            return self.loop(s)
        if isinstance(s, ast.Try) or type(s).__name__ == 'TryStar':
            return {'say': 'Starts a `try` block: Python runs the indented lines, and if one of them causes an error, it jumps to the matching `except` below instead of crashing.'}
        if isinstance(s, ast.Break):
            return {'say': 'Leaves the loop immediately. Python carries on with the first line after the loop.'}
        if isinstance(s, ast.Continue):
            return {'say': 'Skips the rest of this round of the loop and jumps straight to the next round.'}
        if isinstance(s, ast.Pass):
            return {'say': 'Does nothing. It\'s a placeholder, because Python needs at least one line here.'}
        if isinstance(s, ast.Import):
            parts = []
            for a in s.names:
                parts.append(f'{_c(a.name)} (and calls it {_c(a.asname)})' if a.asname else _c(a.name))
            return {'say': f'Loads the {_and(parts)} {"library" if len(parts) == 1 else "libraries"} so this code can use the tools inside.'}
        if isinstance(s, ast.ImportFrom):
            names = _and(_c(a.name) for a in s.names)
            tip = 'The `typing` tools are only labels for describing types.' if s.module == 'typing' else ''
            return {'say': f'Takes {names} from the {_c(s.module or ".")} library, so the code can use {"it" if len(s.names) == 1 else "them"} directly.', 'tip': tip}
        if isinstance(s, (ast.Global, ast.Nonlocal)):
            return {'say': f'Lets this function change {_and(_c(n) for n in s.names)}, which live outside it, instead of making new variables of its own.'}
        if isinstance(s, ast.Delete):
            return {'say': f'Deletes {_and(_c(t) for t in s.targets)}.'}
        if isinstance(s, ast.Assert):
            return {'say': f'Double-checks that {self.clause(s.test)}. If it isn\'t, the program stops with an error.'}
        if isinstance(s, ast.Raise):
            return {'say': f'Stops with an error on purpose: {_c(s.exc)}.' if s.exc else 'Passes the current error on (re-raises it).'}
        if isinstance(s, ast.With):
            return {'say': f'Opens {_and(_c(i.context_expr) for i in s.items)} for the indented lines, and closes it again automatically when they finish.'}
        if isinstance(s, ast.Expr):
            v = s.value
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                return {'say': 'A note (a docstring) describing this code. It doesn\'t do anything when the program runs.'}
            if isinstance(v, (ast.Yield, ast.YieldFrom)):
                return {'say': f'Hands out {_c(v.value) if v.value else "None"} and pauses here until the next value is asked for.'}
            st = self.steps(v)
            if not st:
                return {'say': f'Works out {_c(v)}.'}
            main = st[-1][1] if st[-1][0] is v else f'works out {_c(v)}'
            main = main.replace('then comes back here with its answer', 'then comes back here when it\'s done')
            return {'say': _cap(main) + '.', 'order': self.order(st[:-1] if st[-1][0] is v else st) if len(st) > 1 else []}
        if type(s).__name__ == 'Match':
            return {'say': f'Compares {_c(s.subject)} against each `case` below and runs the first one that fits.'}
        return None

    def loop(self, s):
        t, it = s.target, s.iter
        tip = 'When there are no items left, the loop ends and Python moves on to the code after it.'
        name = _fname(it.func)[1] if isinstance(it, ast.Call) else None
        if name == 'range' and it.args and not isinstance(t, ast.Tuple):
            a = it.args
            if len(a) == 1:
                say = f'Repeats the indented lines {_c(a[0])} times. Each round, {_c(t)} counts up: 0, 1, 2, … up to {_c(a[0])} − 1.'
            elif len(a) == 2:
                say = f'Repeats the indented lines with {_c(t)} counting from {_c(a[0])} up to {_c(a[1])} − 1 (the end number itself is left out).'
            else:
                say = f'Repeats the indented lines with {_c(t)} going from {_c(a[0])} towards {_c(a[1])} in steps of {_c(a[2])}, stopping before {_c(a[1])}.'
            st = [x for x in self.steps(it) if x[0] is not it]
            return {'say': say, 'order': self.order(st), 'tip': tip}
        if name == 'enumerate' and isinstance(t, ast.Tuple) and len(t.elts) == 2 and it.args:
            i, v = t.elts
            return {'say': f'Goes through {_c(it.args[0])} one item at a time. Each round, {_c(v)} is the item and {_c(i)} is its position (0, 1, 2, …).', 'tip': tip}
        if name == 'zip' and isinstance(t, ast.Tuple) and len(t.elts) == len(it.args):
            pairs = _and(f'{_c(x)} comes from {_c(y)}' for x, y in zip(t.elts, it.args))
            return {'say': f'Goes through {_and(_c(y) for y in it.args)} side by side. Each round, {pairs}.', 'tip': tip}
        if name == 'items' and isinstance(t, ast.Tuple) and len(t.elts) == 2:
            k, v = t.elts
            return {'say': f'Goes through every entry in the dictionary {_c(it.func.value)}. Each round, {_c(k)} is the key and {_c(v)} is its value.', 'tip': tip}
        st = self.steps(it)
        if isinstance(t, ast.Tuple):
            say = f'Goes through {_c(it)} one item at a time and unpacks each item into {_and(_c(x) for x in t.elts)}.'
        else:
            say = f'Goes through {_c(it)} one item at a time. Each round, the current item is called {_c(t)} and the indented lines run.'
        return {'say': say, 'order': self.order(st), 'tip': tip}

    def handler(self, h):
        if h.type is None:
            say = 'Runs only if the `try` block above hit an error (any error at all).'
        else:
            names = [ast.unparse(x) for x in (h.type.elts if isinstance(h.type, ast.Tuple) else [h.type])]
            glosses = [f'{n}: {ERRORS[n]}' for n in names if n in ERRORS]
            say = f'Runs only if the `try` block above hit {_and(_c(n) for n in names)}.'
            if glosses:
                say += ' (' + '; '.join(glosses) + ')'
        if h.name:
            say += f' The error itself is saved in {_c(h.name)}.'
        return {'say': say + ' Then Python carries on after the whole try/except.'}


def line_meanings(src):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return {}
    ex = Explainer(tree)
    ex.lines = src.split('\n')
    res = {}

    def put(line, m):
        if not m or not m.get('say'):
            return
        m = {k: v for k, v in m.items() if v}
        key = str(line)
        if key in res:
            res[key]['say'] += ' Then: ' + m['say']
        else:
            res[key] = m

    def mark(stmts, word, say):
        """Label a bare `else:` / `finally:` line that sits just above a block."""
        if not stmts:
            return
        for ln in range(stmts[0].lineno - 1, 0, -1):
            t = ex.lines[ln - 1].strip()
            if re.match(rf'{word}\s*:', t):
                put(ln, {'say': say})
                return
            if t and not t.startswith('#'):
                return

    def visit(node, parent):
        for s in getattr(node, 'body', []) if isinstance(getattr(node, 'body', None), list) else []:
            one(s, node)
        if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)) or type(node).__name__ == 'TryStar':
            for s in node.orelse:
                one(s, node)
        if isinstance(node, ast.Try) or type(node).__name__ == 'TryStar':
            for h in node.handlers:
                try:
                    put(h.lineno, ex.handler(h))
                except Exception:
                    pass
                for s in h.body:
                    one(s, node)
            for s in node.finalbody:
                one(s, node)
            mark(node.orelse, 'else', 'Runs only if the `try` block finished without any error.')
            mark(node.finalbody, 'finally', 'Always runs at the end of the try block, whether there was an error or not.')
        if isinstance(node, ast.If) and node.orelse and not (len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If)
                                                            and ex.lines[node.orelse[0].lineno - 1].lstrip().startswith('elif')):
            mark(node.orelse, 'else', 'Runs only when the `if` check above (and any `elif` checks) turned out false.')
        if isinstance(node, (ast.For, ast.While)) and node.orelse:
            mark(node.orelse, 'else', 'Runs if the loop finished normally, without hitting a `break`.')
        if type(node).__name__ == 'Match':
            for c in node.cases:
                put(c.pattern.lineno, {'say': f'If the value matches {_c(c.pattern)}, run the lines under this case.'})
                for s in c.body:
                    one(s, node)

    def one(s, parent):
        try:
            put(s.lineno, ex.stmt(s, parent))
        except Exception:
            pass
        visit(s, parent)

    for s in tree.body:
        one(s, tree)
    return res
