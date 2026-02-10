# ucilark - UCI parser and encoder library in python

The Universal Chess Interface (UCI) is an open communication protocol that enables chess engines to communicate with user interfaces.

`ucilark` parses from a UCI line string to a `UCI_msg` object containing `dicts`, and can encode the other way around.

Parsing is based on python [lark](https://github.com/lark-parser/lark/) toolkit.

## Overview

- [usage examples](#usage-examples) bellow
- the Lark-flavoured EBNF grammar definition of supported messages : [uci.lark](ucilark/uci.lark)
  - (only a subset of the UCI specification is supported) 
- the code at [ucilark.py](ucilark/ucilark.py)
- some tests at [test_ucilark.py](tests/test_ucilark.py).

## Installation

`pip install ucilark`

## Usage examples

### UCI message: position
```
from ucilark import UCI_msg

line = "position fen 1r1n1rk1/ppq2p2/2b2bp1/2pB3p/2P4P/4P3/PBQ2PP1/1R3RK1 w - - 0 1"
m = UCI_msg.parse(line)

print(m.cmd)
# "position"

print(m.args)
# {'fen': {'movefen': '1r1n1rk1/ppq2p2/2b2bp1/2pB3p/2P4P/4P3/PBQ2PP1/1R3RK1', 'active': 'w', 'castling': '-', 'enpassant': '-', 'halfmove_clock': 0, 'fullmove_clock': 1}}

assert m.encode() == line
```

### UCI message: info
```
from ucilark import UCI_msg

line = "info depth 23 seldepth 33 multipv 2 score cp 0 nodes 3358561 nps 7547328 hashfull 13 tbhits 0 time 445 pv d7d5 e4e3 d5f3 e3f3 e7e6 f3e4 f7g6 e4d4 e6f5 f4h6 g6e8 d4d5 e8b5 h6e3 f5g4 d5c5 b5a6 e3d2 a6b7 d2h6 g4f3"
m = UCI_msg.parse(line)

print(m.cmd)
# "info"

print(m.args)
# {'depth': 23, 'seldepth': 33, 'multipv': 2, 'score': {'cp': '0'}, 'nodes': 3358561, 'nps': 7547328, 'hashfull': 13, 'tbhits': 0, 'time': 445, 'pv': ['d7d5', 'e4e3', 'd5f3', 'e3f3', 'e7e6', 'f3e4', 'f7g6', 'e4d4', 'e6f5', 'f4h6', 'g6e8', 'd4d5', 'e8b5', 'h6e3', 'f5g4', 'd5c5', 'b5a6', 'e3d2', 'a6b7', 'd2h6', 'g4f3']}

assert m.encode() == line
```

