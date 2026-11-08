# PeakDSA tracer: runs Python code and records every step for the visualizer.
import sys, io, ast, json, math, types, time, traceback
import collections, heapq, bisect, itertools, functools, re, string, random, operator
from typing import *
from collections import deque, defaultdict, Counter, OrderedDict
from functools import lru_cache, cache, reduce
from itertools import accumulate, permutations, combinations, product
from heapq import heappush, heappop, heapify, heappushpop, nlargest, nsmallest
from bisect import bisect_left, bisect_right, insort
from math import inf

USER = '<solution>'
NODE_MODE = 'graph'


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


class Node:
    def __init__(self, val=0, a=None, b=None, c=None):
        self.val = val
        if NODE_MODE == 'graph':
            self.neighbors = a if a is not None else []
        elif NODE_MODE == 'random':
            self.next = a
            self.random = b
        elif NODE_MODE == 'nary':
            self.children = a if a is not None else []
        elif NODE_MODE == 'connect':
            self.left = a
            self.right = b
            self.next = c

    def __repr__(self):
        return f"Node({self.val})"


# ---------- builders / converters ----------
def build_list(arr):
    dummy = ListNode()
    cur = dummy
    for v in arr or []:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def build_cycle(arr, pos):
    head = build_list(arr)
    if pos is None or pos < 0 or head is None:
        return head
    nodes, cur = [], head
    while cur:
        nodes.append(cur)
        cur = cur.next
    nodes[-1].next = nodes[pos]
    return head


def list_to_arr(head):
    out, seen = [], set()
    while head is not None and id(head) not in seen and len(out) < 10000:
        seen.add(id(head))
        out.append(head.val)
        head = head.next
    return out


def build_tree(arr, cls=None):
    cls = cls or TreeNode
    if not arr or arr[0] is None:
        return None
    root = cls(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = cls(arr[i])
            q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = cls(arr[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_arr(root):
    if root is None:
        return []
    out, q = [], deque([root])
    while q:
        n = q.popleft()
        if n is None:
            out.append(None)
            continue
        out.append(n.val)
        q.append(n.left)
        q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


def build_graph(adj):
    global NODE_MODE
    NODE_MODE = 'graph'
    if not adj:
        return None
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, nb in enumerate(adj):
        nodes[i].neighbors = [nodes[j - 1] for j in nb]
    return nodes[0]


def graph_to_adj(node):
    if node is None:
        return []
    seen, q = {node.val: node}, deque([node])
    while q:
        n = q.popleft()
        for m in n.neighbors:
            if m.val not in seen:
                seen[m.val] = m
                q.append(m)
    return [[m.val for m in seen[k].neighbors] for k in sorted(seen)]


def build_random(pairs):
    global NODE_MODE
    NODE_MODE = 'random'
    nodes = [Node(p[0]) for p in pairs]
    for i, p in enumerate(pairs):
        nodes[i].next = nodes[i + 1] if i + 1 < len(nodes) else None
        nodes[i].random = nodes[p[1]] if p[1] is not None else None
    return nodes[0] if nodes else None


def random_to_arr(head):
    nodes, cur = [], head
    while cur is not None and len(nodes) < 10000:
        nodes.append(cur)
        cur = cur.next
    idx = {id(n): i for i, n in enumerate(nodes)}
    return [[n.val, idx.get(id(n.random)) if n.random is not None else None] for n in nodes]


def to_plain(v, depth=0):
    if depth > 50:
        return repr(v)
    if isinstance(v, ListNode):
        return list_to_arr(v)
    if isinstance(v, TreeNode):
        return tree_to_arr(v)
    if isinstance(v, Node):
        if hasattr(v, 'neighbors'):
            return graph_to_adj(v)
        if hasattr(v, 'random'):
            return random_to_arr(v)
        return v.val
    if isinstance(v, (list, tuple)):
        return [to_plain(x, depth + 1) for x in v]
    if isinstance(v, (set, frozenset)):
        try:
            return sorted(to_plain(x, depth + 1) for x in v)
        except TypeError:
            return [to_plain(x, depth + 1) for x in v]
    if isinstance(v, dict):
        return {str(k): to_plain(x, depth + 1) for k, x in v.items()}
    if isinstance(v, float) and not math.isfinite(v):
        return str(v)
    return v


def convert_arg(v, typ):
    if typ == 'ListNode':
        return build_list(v)
    if typ == 'TreeNode':
        return build_tree(v)
    if typ == 'graph':
        return build_graph(v)
    if typ == 'random':
        return build_random(v)
    if typ == 'lists':
        return [build_list(x) for x in v]
    if typ == 'chars':
        return [list(r) if isinstance(r, str) else r for r in v]
    return v


def short(v, n=24):
    if isinstance(v, (ListNode, TreeNode, Node)):
        return f"({v.val})"
    if v is None:
        return 'None'
    try:
        r = repr(v)
    except Exception:
        r = '?'
    return r if len(r) <= n else r[:n - 1] + '…'


# ---------- encoder ----------
class Encoder:
    LIM = 120
    HEAP_LIM = 400

    def __init__(self):
        self.ids = {}
        self.keep = []

    def rid(self, o):
        k = id(o)
        r = self.ids.get(k)
        if r is None:
            r = len(self.ids) + 1
            self.ids[k] = r
            self.keep.append(o)
        return r

    def snapshot(self, roots):
        self.heap, self.pending = {}, []
        out = [[name, self.enc(v)] for name, v in roots]
        while self.pending:
            r, o = self.pending.pop()
            self.heap[r] = self.obj(o)
        return out, self.heap

    def enc(self, v):
        if v is None or isinstance(v, bool):
            return v
        if isinstance(v, int):
            return v if abs(v) < 2 ** 53 else {"big": str(v)}
        if isinstance(v, float):
            return v if math.isfinite(v) else {"f": str(v)}
        if isinstance(v, str):
            return {"s": v if len(v) <= 400 else v[:400] + '…'}
        if isinstance(v, (complex, bytes, range)):
            return {"s": repr(v), "q": 1}
        if (type(v).__module__ or '').startswith('numpy') and getattr(v, 'ndim', None) == 0 and hasattr(v, 'item'):
            return self.enc(v.item())
        r = self.rid(v)
        if r not in self.heap:
            if len(self.heap) >= self.HEAP_LIM:
                return {"s": '…', "q": 1}
            self.heap[r] = None
            self.pending.append((r, v))
        return {"r": r}

    def obj(self, v):
        L = self.LIM
        lib = self.lib(v)
        if lib is not None:
            return lib
        if isinstance(v, list):
            return {"k": "list", "v": [self.enc(x) for x in v[:L]], "n": len(v)}
        if isinstance(v, tuple):
            return {"k": "tuple", "v": [self.enc(x) for x in v[:L]], "n": len(v)}
        if isinstance(v, (set, frozenset)):
            items = list(v)
            try:
                items.sort()
            except TypeError:
                pass
            return {"k": "set", "v": [self.enc(x) for x in items[:L]], "n": len(v)}
        if isinstance(v, deque):
            return {"k": "deque", "v": [self.enc(x) for x in list(v)[:L]], "n": len(v)}
        if isinstance(v, dict):
            items = list(v.items())[:L]
            d = {"k": "dict", "v": [[self.enc(a), self.enc(b)] for a, b in items], "n": len(v)}
            if type(v) is not dict:
                d["cls"] = type(v).__name__
            return d
        if isinstance(v, (types.FunctionType, types.BuiltinFunctionType, types.MethodType, functools.partial)):
            return {"k": "func", "name": getattr(v, '__name__', 'function')}
        if isinstance(v, type):
            return {"k": "class", "name": v.__name__}
        if isinstance(v, types.ModuleType):
            return {"k": "other", "repr": f"module {v.__name__}"}
        d = getattr(v, '__dict__', None)
        if isinstance(d, dict) and not isinstance(v, (types.GeneratorType,)):
            return {"k": "obj", "cls": type(v).__name__,
                    "a": [[a, self.enc(b)] for a, b in list(d.items())[:40] if not a.startswith('__')]}
        try:
            r = repr(v)
        except Exception:
            r = type(v).__name__
        return {"k": "other", "repr": r[:120]}


    def lib(self, v):
        mod, name, L = type(v).__module__ or '', type(v).__name__, self.LIM
        try:
            if mod.startswith('numpy') and name == 'ndarray' and v.ndim in (1, 2):
                t = v.tolist()
                self.keep.append(t)
                return {"k": "list", "v": [self.enc(x) for x in t[:L]], "n": len(t), "cls": "array"}
            if mod.startswith('pandas') and name == 'DataFrame':
                t = [[str(c) for c in v.columns]] + v.head(L).values.tolist()
                self.keep.append(t)
                return {"k": "list", "v": [self.enc(x) for x in t], "n": len(v) + 1, "cls": "DataFrame"}
            if mod.startswith('pandas') and name == 'Series':
                items = list(v.head(L).items())
                return {"k": "dict", "v": [[self.enc(a), self.enc(b)] for a, b in items], "n": len(v), "cls": "Series"}
        except Exception:
            return None
        return None


# ---------- safe condition evaluation ----------
SAFE_FUNCS = {'len', 'abs', 'min', 'max', 'sum', 'int', 'str', 'float', 'bool', 'ord', 'chr', 'isinstance', 'any', 'all', 'sorted', 'set', 'tuple', 'list'}
SAFE_METHODS = {'isalnum', 'isdigit', 'isalpha', 'isspace', 'islower', 'isupper', 'lower', 'upper', 'get', 'keys', 'values', 'items', 'count', 'index', 'startswith', 'endswith', 'find'}
SAFE_NODES = (ast.Expression, ast.BoolOp, ast.BinOp, ast.UnaryOp, ast.Compare, ast.Name, ast.Load, ast.Constant,
              ast.Subscript, ast.Slice, ast.Attribute, ast.Tuple, ast.List, ast.Call, ast.IfExp, ast.keyword,
              ast.boolop, ast.operator, ast.unaryop, ast.cmpop, ast.expr_context)


def is_safe(node):
    for n in ast.walk(node):
        if not isinstance(n, SAFE_NODES):
            return False
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name) and f.id in SAFE_FUNCS:
                continue
            if isinstance(f, ast.Attribute) and f.attr in SAFE_METHODS:
                continue
            return False
    return True


PRIM = (int, float, str, bool, type(None))


class Sub(ast.NodeTransformer):
    def __init__(self, g, l):
        self.g, self.l = g, l

    def _try(self, node):
        try:
            v = eval(compile(ast.Expression(node), '<c>', 'eval'), self.g, self.l)
        except Exception:
            return None
        if isinstance(v, PRIM) and len(repr(v)) <= 22:
            return ast.copy_location(ast.Constant(v), node)
        if isinstance(v, (ListNode, TreeNode, Node)):
            return ast.copy_location(ast.Name(id=f"node({v.val})", ctx=ast.Load()), node)
        return None

    def visit_Name(self, node):
        if node.id in ('True', 'False', 'None'):
            return node
        return self._try(node) or node

    def visit_Subscript(self, node):
        return self._try(node) or self.generic_visit(node)

    def visit_Attribute(self, node):
        return self._try(node) or self.generic_visit(node)

    def visit_Call(self, node):
        return self._try(node) or self.generic_visit(node)


def analyze_source(src):
    conds = {}
    try:
        tree = ast.parse(src)
    except Exception:
        return conds
    for n in ast.walk(tree):
        if isinstance(n, (ast.If, ast.While)) and is_safe(n.test):
            conds[n.test.lineno] = (n.test, 'while' if isinstance(n, ast.While) else 'if')
    return conds


# ---------- tracer ----------
class StepLimit(Exception):
    pass


class NeedInput(BaseException):
    pass


class Out:
    def __init__(self):
        self.parts, self.n = [], 0

    def write(self, s):
        if self.n < 200000:
            self.parts.append(s)
            self.n += len(s)
        return len(s)

    def flush(self):
        pass

    def text(self):
        return ''.join(self.parts)


HIDE_TYPES = (types.ModuleType, type, types.FunctionType, types.BuiltinFunctionType, types.MethodType)


class Tracer:
    def __init__(self, src, max_steps=3000, hide=()):
        self.steps, self.calls = [], []
        self.enc = Encoder()
        self.max = max_steps
        self.conds = analyze_source(src)
        self.frames = {}
        self.callstack = []
        self.hide = set(hide)
        self.out = None
        self.truncated = False
        self.need = None
        self.cut = None
        self.fb = []

    def visible(self, frame):
        mod = frame.f_code.co_name == '<module>'
        res = []
        for k, v in list(frame.f_locals.items()):
            if k.startswith('__') or (mod and k in self.hide):
                continue
            if isinstance(v, HIDE_TYPES) or isinstance(v, functools._lru_cache_wrapper):
                continue
            if k == 'self' and not getattr(v, '__dict__', None):
                continue
            res.append((k, v))
        return res

    def record(self, frame, event, arg):
        chain = []
        f = frame
        while f is not None:
            if f.f_code.co_filename == USER:
                chain.append(f)
            f = f.f_back
        chain.reverse()
        roots, meta = [], []
        for f in chain:
            vis = self.visible(f)
            meta.append((f, len(vis)))
            roots.extend(vis)
        encoded, heap = self.enc.snapshot(roots)
        st, i = [], 0
        for f, n in meta:
            uid = self.frames.get(id(f), 0)
            name = f.f_code.co_name
            st.append({"f": name, "u": uid, "l": f.f_lineno, "v": encoded[i:i + n]})
            i += n
        step = {"l": frame.f_lineno, "e": event, "st": st, "h": heap,
                "o": self.out.n if self.out else 0,
                "c": self.callstack[-1] if self.callstack else 0}
        if event == 'line' and frame.f_lineno in self.conds:
            test, kind = self.conds[frame.f_lineno]
            try:
                val = eval(compile(ast.Expression(test), '<c>', 'eval'), frame.f_globals, frame.f_locals)
                sub = ast.unparse(Sub(frame.f_globals, frame.f_locals).visit(ast.parse(ast.unparse(test), mode='eval')))
                step["x"] = {"cond": ast.unparse(test), "sub": sub, "val": bool(val), "kind": kind}
            except Exception:
                pass
        elif event == 'return':
            step["ret"] = self.enc.snapshot([('r', arg)])[0][0][1]
            step["h"].update(self.enc.heap)
            step["rs"] = short(arg, 40)
        elif event == 'exception':
            et, ev, _ = arg
            step["exc"] = f"{et.__name__}: {ev}"
        self.steps.append(step)

    def trace(self, frame, event, arg):
        if frame.f_code.co_filename != USER:
            return None
        if self.need is not None:
            if event == 'line':
                raise NeedInput()
            return self.trace
        if event == 'call':
            cid = len(self.calls) + 1
            self.frames[id(frame)] = cid
            code = frame.f_code
            names = code.co_varnames[:code.co_argcount]
            args = ', '.join(f"{n}={short(frame.f_locals.get(n), 16)}" for n in names if n != 'self')
            if len(self.calls) < 400:
                self.calls.append({"id": cid, "p": self.callstack[-1] if self.callstack else 0,
                                   "f": code.co_name, "a": args, "s": len(self.steps)})
            self.callstack.append(cid)
        self.record(frame, event, arg)
        if event == 'return':
            cid = self.callstack.pop() if self.callstack else 0
            if 0 < cid <= len(self.calls):
                self.calls[cid - 1]["e"] = len(self.steps) - 1
                self.calls[cid - 1]["r"] = short(arg, 18)
            self.frames.pop(id(frame), None)
        if len(self.steps) >= self.max:
            self.truncated = True
            sys.settrace(None)
            raise StepLimit()
        return self.trace


# ---------- harness ----------
BASE_NAMES = None


def fresh_globals():
    g = {'__name__': '__main__', '__builtins__': __builtins__}
    for k, v in list(globals().items()):
        if not k.startswith('_') and k not in ('api', 'Tracer', 'Encoder', 'Sub', 'Out', 'StepLimit', 'NeedInput', 'fresh_globals',
                                                     'line_meanings', 'Explainer', 'ERRORS', 'OPS',
                                                     'suggest_answer', 'guess_param'):
            g[k] = v
    return g


def find_target(g, fn):
    sol = g.get('Solution')
    if isinstance(sol, type):
        inst = sol()
        if fn and hasattr(inst, fn):
            return getattr(inst, fn)
        for name in vars(sol):
            if not name.startswith('_') and callable(getattr(inst, name)):
                return getattr(inst, name)
    if fn and callable(g.get(fn)):
        return g[fn]
    raise NameError(f"Couldn't find a function called '{fn}'. Keep the name from the starter code!")


def compare(got, exp, mode):
    if got is None and exp == []:
        return True
    if mode == 'any':
        return True
    if mode == 'float':
        try:
            return abs(float(got) - float(exp)) < 1e-5
        except Exception:
            return False
    if mode == 'sorted':
        try:
            return sorted(got) == sorted(exp)
        except TypeError:
            return False
    if mode == 'deep':
        def norm(x):
            if isinstance(x, list):
                inner = [norm(y) for y in x]
                try:
                    return sorted(inner)
                except TypeError:
                    return inner
            return x
        return norm(got) == norm(exp)
    return got == exp


def prepare(p, args):
    global NODE_MODE
    NODE_MODE = p.get('nodeMode', 'graph')
    types_ = p.get('types', {})
    params = p.get('params', [])
    if 'joined' in types_.values():
        a, b, sa, sb = args
        ha = build_list(a)
        hb = build_list(b[:sb])
        shared = ha
        for _ in range(sa):
            shared = shared.next if shared else None
        if hb:
            t = hb
            while t.next:
                t = t.next
            t.next = shared
        else:
            hb = shared
        return [ha, hb]
    out = []
    for i, a in enumerate(args):
        t = types_.get(params[i] if i < len(params) else str(i), types_.get(str(i)))
        out.append(convert_arg(a, t))
    if p.get('cycle') is not None and out:
        out[0] = build_cycle(args[0], args[p['cycle']])
        out = out[:p['cycle']] + out[p['cycle'] + 1:]
    return out


def call_design(g, ops, argl):
    cls = g.get(ops[0])
    if not isinstance(cls, type):
        raise NameError(f"Couldn't find class '{ops[0]}'")
    res = [None]
    obj = cls(*argl[0])
    for op, a in zip(ops[1:], argl[1:]):
        res.append(to_plain(getattr(obj, op)(*a)))
    return res


def run_one(p, g, args):
    if p.get('mode') == 'design':
        return call_design(g, args[0], args[1])
    call_args = prepare(p, args)
    f = find_target(g, p.get('fn'))
    r = f(*call_args)
    if p.get('inplace') is not None:
        r = call_args[p['inplace']]
    return to_plain(r)


def fmt_exc(e):
    tb = traceback.extract_tb(e.__traceback__)
    line = None
    for fr in tb:
        if fr.filename == USER:
            line = fr.lineno
    return {"error": f"{type(e).__name__}: {e}", "line": line}


def do_trace(p):
    src = p['code']
    g = fresh_globals()
    out = Out()
    old = sys.stdout
    sys.stdout = out
    tr = Tracer(src, p.get('maxSteps', 3000), hide=set(g.keys()))
    tr.out = out
    answers = [str(a) for a in (p.get('stdin') or [])]

    def fake_input(prompt=''):
        out.write(str(prompt))
        if answers:
            a = answers.pop(0)
            out.write(a + '\n')
            tr.fb.append(out.n)
            return a
        if tr.need is None:
            tr.need, tr.cut = str(prompt), len(tr.steps)
        # Re-arm tracing so a bare `except:` around input() can't swallow the stop forever:
        # the next line of the handler raises NeedInput again from the tracer.
        f = sys._getframe(1)
        while f is not None:
            if f.f_code.co_filename == USER:
                f.f_trace = tr.trace
            f = f.f_back
        sys.settrace(tr.trace)
        raise NeedInput()

    class FakeStdin:
        def readline(self):
            return fake_input() + '\n'

        def read(self):
            return '\n'.join(answers.pop(0) for _ in range(len(answers)))

        def __iter__(self):
            while answers:
                yield answers.pop(0) + '\n'

    g['input'] = fake_input
    old_in, old_sleep = sys.stdin, time.sleep
    sys.stdin, time.sleep = FakeStdin(), (lambda *a, **k: None)
    if 'seed' in p:
        random.seed(p['seed'])
    result, err = None, None
    try:
        code = compile(src, USER, 'exec')
        if p.get('mode') == 'script':
            sys.settrace(tr.trace)
            try:
                exec(code, g)
            finally:
                sys.settrace(None)
        else:
            exec(code, g)
            sys.settrace(tr.trace)
            try:
                result = run_one(p, g, p['args'])
            finally:
                sys.settrace(None)
            result = json.dumps(to_plain(result), default=str)
    except (StepLimit, NeedInput, SystemExit):
        err = None
    except SyntaxError as e:
        err = {"error": f"SyntaxError: {e.msg}", "line": e.lineno}
    except Exception as e:
        err = fmt_exc(e) if tr.need is None else None
    finally:
        sys.settrace(None)
        sys.stdout, sys.stdin, time.sleep = old, old_in, old_sleep
    if tr.need is not None:
        result, err = None, None
        tr.steps = tr.steps[:tr.cut]
        if tr.steps:
            last = dict(tr.steps[-1], o=out.n, e='input')
            last.pop('exc', None)
            tr.steps.append(last)
        tr.calls = [c for c in tr.calls if c['s'] < tr.cut]
        for c in tr.calls:
            if c.get('e', -1) >= tr.cut:
                c.pop('e', None)
                c.pop('r', None)
        try:
            suggest = suggest_answer(src, tr.steps[-1]['l'] if tr.steps else 0, tr.need,
                                     [str(a) for a in (p.get('stdin') or [])], out.text(), tr.fb)
        except Exception:
            suggest = 'hello'
    else:
        suggest = None
    try:
        meaning = globals()['line_meanings'](src)
    except Exception:
        meaning = {}
    return {"steps": tr.steps, "calls": tr.calls, "out": out.text(), "result": result,
            "error": err, "truncated": tr.truncated, "needInput": tr.need, "meaning": meaning,
            "suggest": suggest}


def do_test(p):
    src = p['code']
    results = []
    old = sys.stdout
    try:
        code = compile(src, USER, 'exec')
    except SyntaxError as e:
        return {"error": {"error": f"SyntaxError: {e.msg}", "line": e.lineno}, "results": []}
    for t in p['tests']:
        g = fresh_globals()
        out = Out()
        sys.stdout = out
        item = {"args": t[0], "exp": t[1]}
        t0 = time.time()
        try:
            exec(code, g)
            got = run_one(p, g, t[0])
            item["got"] = got
            item["pass"] = compare(got, t[1], p.get('cmp', 'exact'))
        except RecursionError as e:
            item.update({"pass": False, **fmt_exc(e)})
        except Exception as e:
            item.update({"pass": False, **fmt_exc(e)})
        finally:
            sys.stdout = old
        item["ms"] = round((time.time() - t0) * 1000, 2)
        item["out"] = out.text()[:2000]
        results.append(item)
    return {"results": results, "error": None}


def py_literal(s):
    s = s.strip()
    if not s:
        return None
    try:
        return json.loads(s)
    except Exception:
        pass
    t = re.sub(r'\bnull\b', 'None', s)
    t = re.sub(r'\btrue\b', 'True', t)
    t = re.sub(r'\bfalse\b', 'False', t)
    return ast.literal_eval(t)


def ann_type(a):
    if a is None:
        return None
    s = ast.unparse(a)
    for k in ('ListNode', 'TreeNode'):
        if k in s:
            return k
    if "'Node'" in s or s.endswith('Node') or 'Node]' in s:
        return 'graph'
    return None


def suggest_answer(src, line, prompt, answers, text, fb):
    """Pick a sensible answer for input(), using the question text and how the code uses the answer."""
    rng = random.Random(len(answers) * 7919 + len(text))
    lines = src.split('\n')
    code = lines[line - 1] if 0 < line <= len(lines) else ''
    pl = prompt.lower()
    numeric = bool(re.search(r'\b(int|float)\s*\(\s*input', code))
    m = re.search(r'[(\[]([^()\[\]]*/[^()\[\]]*)[)\]]', prompt)
    if m:
        opts = [o.strip() for o in m.group(1).split('/') if o.strip()]
        if opts and {o.lower() for o in opts} <= {'y', 'n', 'yes', 'no'}:
            again = re.search(r'again|another|continue|more|retry', pl)
            return next((o for o in opts if o.lower().startswith('n' if again else 'y')), opts[0])
        if opts and not all(re.fullmatch(r'-?\d+', o) for o in opts):
            return rng.choice(opts)
    var = re.match(r'\s*(\w+)\s*=.*\binput\s*\(', code)
    if var and not numeric:
        name, lits = var.group(1), []
        for n in ast.walk(ast.parse(src)):
            if isinstance(n, ast.Compare):
                parts = [n.left] + list(n.comparators)
                hit = any((isinstance(x, ast.Name) and x.id == name) or
                          (isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute) and
                           isinstance(x.func.value, ast.Name) and x.func.value.id == name) for x in parts)
                if hit:
                    for x in parts:
                        if isinstance(x, ast.Constant) and isinstance(x.value, str):
                            lits.append(x.value)
                        if isinstance(x, (ast.Tuple, ast.List, ast.Set)):
                            lits += [e.value for e in x.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
        lits = [x for x in dict.fromkeys(lits) if x.strip()]
        if lits:
            stop = [x for x in lits if x.lower() in ('q', 'quit', 'exit', 'stop', 'n', 'no', 'done', 'end', 'bye')]
            if stop and len(answers) >= 8:
                return stop[0]
            return rng.choice([x for x in lits if x not in stop] or lits)
    r = re.search(r'(-?\d+)\s*(?:-|–|to|and|\.\.)\s*(-?\d+)', prompt)
    lo, hi = (int(r.group(1)), int(r.group(2))) if r else (None, None)
    if lo is not None and lo > hi:
        lo, hi = hi, lo
    nums = [int(a) for a in answers if re.fullmatch(r'\s*-?\d+\s*', a)]
    if 'guess' in pl or re.search(r'higher|too (high|low)', text, re.I):
        if lo is None:
            lo, hi = 1, 100
        for i, a in enumerate(answers):
            if not re.fullmatch(r'\s*-?\d+\s*', a) or i >= len(fb):
                continue
            seg, v = text[fb[i]: fb[i + 1] if i + 1 < len(fb) else len(text)], int(a)
            if re.search(r'higher|too low|bigger|greater|go up', seg, re.I):
                lo = max(lo, v + 1)
            elif re.search(r'lower|too high|smaller|go down', seg, re.I):
                hi = min(hi, v - 1)
        if hi < lo:
            lo, hi = hi, lo
        return str((lo + hi) // 2)
    if lo is not None:
        free = [v for v in range(lo, hi + 1) if v not in nums] if hi - lo <= 1000 else []
        return str(rng.choice(free) if free else rng.randint(lo, hi))
    if re.search(r'colou?r', pl) and not numeric:
        return rng.choice(['red', 'green', 'blue'])
    if numeric or re.search(r'number|how many|\bage\b|how old|count|amount|size|digit|\bn\b|score|year|times|rows|\bcols?\b|column', pl):
        if re.search(r'\bage\b|how old', pl):
            return str(rng.randint(12, 60))
        if 'year' in pl:
            return str(rng.randint(1990, 2025))
        return str(rng.randint(1, 10))
    if 'name' in pl:
        return rng.choice(['Ada', 'Alan', 'Grace', 'Linus'])
    if 'word' in pl:
        return rng.choice(['banana', 'racecar', 'python'])
    if re.search(r'colou?r', pl):
        return rng.choice(['red', 'green', 'blue'])
    if re.search(r'sentence|text|message|string|line', pl):
        return 'hello world'
    return 'hello'


STR_USES = {'.lower', '.upper', '.isalpha', '.isdigit', '.isalnum', '.split', '.strip', '.startswith', '.endswith',
            '.replace', '.isspace', '.find', 'cmpstr', 'ord()'}
LIST_USES = {'[]', 'for', 'len()', 'sum()', 'sorted()', 'max()', 'min()', 'set()', 'enumerate()', 'reversed()',
             '.append', '.sort', '.pop', 'Counter()', 'heapify()'}


def guess_param(fdef, name, typ):
    """Example input for a parameter, worked out from its name and how the function uses it."""
    if typ:
        return None, None
    uses = set()
    for n in ast.walk(fdef):
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == name:
            uses.add('.' + n.attr)
        elif isinstance(n, ast.Subscript):
            v = n.value
            if isinstance(v, ast.Subscript) and isinstance(v.value, ast.Name) and v.value.id == name:
                uses.add('[][]')
            elif isinstance(v, ast.Name) and v.id == name:
                uses.add('[]')
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and \
                any(isinstance(a, ast.Name) and a.id == name for a in n.args):
            uses.add(n.func.id + '()')
        elif isinstance(n, (ast.For, ast.comprehension)) and isinstance(n.iter, ast.Name) and n.iter.id == name:
            uses.add('for')
        elif isinstance(n, ast.BinOp) and any(isinstance(x, ast.Name) and x.id == name for x in (n.left, n.right)):
            uses.add('math')
        elif isinstance(n, ast.Compare):
            parts = [n.left] + list(n.comparators)
            if any(isinstance(x, ast.Name) and x.id == name for x in parts):
                for x in parts:
                    if isinstance(x, ast.Constant) and isinstance(x.value, str):
                        uses.add('cmpstr')
                    elif isinstance(x, ast.Constant) and isinstance(x.value, (int, float)) and not isinstance(x.value, bool):
                        uses.add('cmpnum')
    low = name.lower()
    if uses & {'.left', '.right'} or re.fullmatch(r'root\d?|tree|node', low):
        return '[3, 9, 20, null, null, 15, 7]', 'TreeNode'
    if '.next' in uses or re.fullmatch(r'head|l1|l2|list1|list2', low):
        return '[1, 2, 3, 4, 5]', 'ListNode'
    if '.neighbors' in uses:
        return '[[2, 4], [1, 3], [2, 4], [1, 3]]', 'graph'
    if '[][]' in uses or re.search(r'grid|board|matrix|mat$', low):
        return ('[["1", "1", "0"], ["1", "0", "0"], ["0", "0", "1"]]' if 'cmpstr' in uses
                else '[[1, 3, 1], [1, 5, 1], [4, 2, 1]]'), None
    if re.search(r'interval|meeting', low):
        return '[[1, 3], [2, 6], [8, 10], [15, 18]]', None
    if re.search(r'edge|prereq|connection', low):
        return '[[0, 1], [1, 2], [2, 3]]', None
    if re.search(r'point', low):
        return '[[1, 1], [2, 2], [3, 3]]', None
    if re.search(r'^(words|strs|strings|names|tokens|wordlist)$', low):
        return '["eat", "tea", "tan", "ate", "nat", "bat"]', None
    is_str = bool(uses & STR_USES) or re.fullmatch(r's|t|s1|s2|word|text|string|sentence|pattern|p|txt|str\w*', low)
    is_list = bool(uses & LIST_USES) or re.search(r'nums|arr|array|list|numbers|heights|prices|values|items|coins|stones', low)
    if is_str and not re.search(r'nums|arr|list', low):
        return ('"hello world"' if re.search(r'sentence|text', low) else '"racecar"'), None
    if is_list:
        return '[3, 1, 4, 1, 5, 9, 2, 6]', None
    if uses & {'range()', 'math', 'cmpnum'} or re.fullmatch(r'n|m|k|x|y|num|target|amount|capacity|limit|goal|count|size|steps', low):
        return {'target': '9', 'k': '3', 'amount': '11'}.get(low, '5'), None
    if re.match(r'is_|flag|ok$', low):
        return 'True', None
    return None, None


def do_inspect(p):
    """Figure out what a pasted LeetCode solution expects as input."""
    src = p['code']
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return {"error": f"SyntaxError on line {e.lineno}: {e.msg}"}
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    sol = next((c for c in classes if c.name == 'Solution'), None)

    def sig(fdef, skip_self):
        args = fdef.args.args[1:] if skip_self else fdef.args.args
        out = []
        for a in args:
            typ = ann_type(a.annotation)
            g, t2 = guess_param(fdef, a.arg, typ)
            out.append({"name": a.arg, "type": typ or t2, "guess": g,
                        "hint": ast.unparse(a.annotation) if a.annotation else ''})
        return out

    if sol:
        meths = [m for m in sol.body if isinstance(m, ast.FunctionDef) and not m.name.startswith('_')]
        if meths:
            m = meths[-1] if len(meths) > 1 and any(x.name == 'helper' for x in meths[:1]) else meths[0]
            names = [x.name for x in meths]
            return {"mode": "function", "fn": m.name, "params": sig(m, True), "methods": names}
    design = [c for c in classes if c.name not in ('ListNode', 'TreeNode', 'Node', 'Solution')
              and any(isinstance(m, ast.FunctionDef) and m.name == '__init__' for m in c.body)]
    if design and not any(isinstance(n, (ast.Expr, ast.Assign)) for n in tree.body):
        return {"mode": "design", "cls": design[-1].name}
    has_top = any(not isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom)) for n in tree.body)
    if funcs and not has_top:
        f = funcs[0]
        return {"mode": "function", "fn": f.name, "params": sig(f, False), "methods": [x.name for x in funcs]}
    return {"mode": "script"}


def api(cmd, payload):
    p = json.loads(payload)
    if cmd == 'trace':
        if 'rawArgs' in p:
            p['args'] = [py_literal(x) for x in p['rawArgs']]
        res = do_trace(p)
    elif cmd == 'test':
        res = do_test(p)
    elif cmd == 'inspect':
        res = do_inspect(p)
    else:
        res = {"error": "unknown command"}
    return json.dumps(res, default=str, allow_nan=False) if cmd != 'trace' else json.dumps(res, default=str)
