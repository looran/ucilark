import logging
from pathlib import Path

import lark

_log = logging.getLogger("ucilark")
#_log.setLevel(logging.DEBUG)

class UCI_trans(lark.Transformer):
    line = dict
    INT = int

    def __default__(self, tok, childs, meta):
        _log.debug(f'Trans-node {tok.type} {str(tok)} {len(childs)} : {childs}')
        if str(tok) in ["id", "info", "score", "position", "fen", "setoption"]:
            return (str(tok), dict(childs)) # dicts
        elif str(tok) in ["cp", "mate"]:
            return (str(tok), int(childs[0])) # signed integers
        elif len(childs) == 1 and str(tok) not in ["moves", "pv", "bestmove"]:
            return (str(tok), childs[0]) # simples values, treat as string
        else:
            return (str(tok), childs) # special values like pv, treat as list

    def __default_token__(self, t):
        _log.debug(f'Trans-token {t}')
        return t.value

    def move(self, m):
        return str(m[0])

class UCI_msg:
    ucilark_path = Path(__file__).resolve().parent / 'uci.lark'
    parser = lark.Lark(ucilark_path.read_text(), start='line', parser='lalr')

    @classmethod
    def parse(cls, line):
        return cls(UCI_trans().transform(cls.parser.parse(line)), line)

    def __init__(self, tree, line=None):
        self.cmd = list(tree.keys())[0]
        self.args = tree[self.cmd]
        self.line = line

    def encode(self):
        def _str(i, parent):
            _log.debug(f"encode {type(i)} {i} (parent {parent})")
            if type(i) == dict:
                if parent in ["fen"]:
                    return ' '.join([ f"{v}" for k, v in i.items() ])
                else:
                    return ' '.join([ f"{k} {_str(v, k)}" for k, v in i.items() ]).strip()
            elif type(i) in [list, tuple]:
                return ' '.join([_str(j, i) for j in i])
            else:
                return str(i)

        # place some values last
        for last_val in ['pv']:
             if last_val in self.args:
                self.args[last_val] = self.args.pop(last_val)

        # use cached line, otherwise iterate args tree
        if self.line:
            s = self.line
        else:
            s = self.cmd
            if self.args:
                s += " " + _str(self.args, None)
        return s

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"UCI_msg: {self.encode()}"

    def __eq__(self, other):
        return (self.cmd == other.cmd) and (self.args == other.args)

    def get(self, name, name2=None):
        if name in self.args:
            if name2:
                if name2 in self.args[name]:
                    return self.args[name][name2]
                return ""
            return self.args[name]
        return ""

