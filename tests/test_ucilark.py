#!/usr/bin/env python3

import sys
import pytest
import logging
from pathlib import Path

REPO = Path(__file__).parent / '..'
sys.path.insert(0, str(REPO))
from ucilark import UCI_msg

class Test_uci_msg:
    @pytest.mark.parametrize("cmd,line,expected_args", [
        ("info", # info 1 with mate
            "info depth 1 seldepth 7 multipv 1 score mate 2 nodes 2416 nps 2416000 hashfull 0 tbhits 0 time 1 pv c2g6 f6g7 g6g7",
            {'depth': 1, 'seldepth': 7, 'multipv': 1, 'score': {'mate': '2'}, 'nodes': 2416, 'nps': 2416000, 'hashfull': 0, 'tbhits': 0, 'time': 1, 'pv': ['c2g6', 'f6g7', 'g6g7']}),
        ( "info", # info 2
            "info depth 23 seldepth 33 multipv 2 score cp 0 nodes 3358561 nps 7547328 hashfull 13 tbhits 0 time 445 pv d7d5 e4e3 d5f3 e3f3 e7e6 f3e4 f7g6 e4d4 e6f5 f4h6 g6e8 d4d5 e8b5 h6e3 f5g4 d5c5 b5a6 e3d2 a6b7 d2h6 g4f3",
            {'depth': 23, 'seldepth': 33, 'multipv': 2, 'score': {'cp': '0'}, 'nodes': 3358561, 'nps': 7547328, 'hashfull': 13, 'tbhits': 0, 'time': 445, 'pv': ['d7d5', 'e4e3', 'd5f3', 'e3f3', 'e7e6', 'f3e4', 'f7g6', 'e4d4', 'e6f5', 'f4h6', 'g6e8', 'd4d5', 'e8b5', 'h6e3', 'f5g4', 'd5c5', 'b5a6', 'e3d2', 'a6b7', 'd2h6', 'g4f3']}),
        ("info", # info 3
            "info depth 2 seldepth 3 multipv 1 score cp -20 nodes 48 nps 48000 hashfull 0 tbhits 0 time 1 pv e7e5",
            {'depth': 2, 'seldepth': 3, 'multipv': 1, 'score': {'cp': '-20'}, 'nodes': 48, 'nps': 48000, 'hashfull': 0, 'tbhits': 0, 'time': 1, 'pv': ['e7e5']}),
        ("info", # info 4 with negative mate
            "info depth 245 seldepth 5 multipv 1 score mate -2 nodes 99211 nps 14173000 hashfull 0 tbhits 0 time 7 pv h8h7 e4g5 h7h8 g5f7",
            {'depth': 245, 'seldepth': 5, 'multipv': 1, 'score':
 {'mate': '-2'}, 'nodes': 99211, 'nps': 14173000, 'hashfull': 0, 'tbhits': 0, 'time': 7, 'pv': ['h8h7', 'e4g5', 'h7h8', 'g5f7']}),
        ("info", # info 5 with upperbound
            "info depth 22 seldepth 36 multipv 5 score cp -16 upperbound nodes 22225440 nps 2777485 hashfull 179 tbhits 0 time 8002 pv f1d3 c7c5",
            {'depth': 22, 'seldepth': 36, 'multipv': 5, 'score': {'cp': '-16', 'upperbound': []}, 'nodes': 22225440, 'nps': 2777485, 'hashfull': 179, 'tbhits': 0, 'time': 8002, 'pv': ['f1d3', 'c7c5']}),
        ("position", # position 1
            "position fen 1r1n1rk1/ppq2p2/2b2bp1/2pB3p/2P4P/4P3/PBQ2PP1/1R3RK1 w - - 0 1",
            {'fen': {'movefen': '1r1n1rk1/ppq2p2/2b2bp1/2pB3p/2P4P/4P3/PBQ2PP1/1R3RK1', 'active': 'w', 'castling': '-', 'enpassant': '-', 'halfmove_clock': 0, 'fullmove_clock': 1}}),
        ("position", # position 2
            "position fen rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
            {'fen': {'movefen': 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR', 'active': 'b', 'castling': 'KQkq', 'enpassant': '-', 'halfmove_clock': 0, 'fullmove_clock': 1}}),
        ("position", # position 3
            "position fen rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2 moves g1f3",
            {'fen': {'movefen': 'rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR', 'active': 'w', 'castling': 'KQkq', 'enpassant': '-', 'halfmove_clock': 0, 'fullmove_clock': 2}, 'moves': ['g1f3']}),
        ("position", # position 4
            "position fen rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2 moves g1f3 e7e5",
            {'fen': {'movefen': 'rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR', 'active': 'w', 'castling': 'KQkq', 'enpassant': '-', 'halfmove_clock': 0, 'fullmove_clock': 2}, 'moves': ['g1f3', 'e7e5']}),
        ("bestmove", # bestmove
            "bestmove c2g6",
            ['c2g6']),
        ("bestmove", # bestmove with ponder
            "bestmove c2g6 ponder f6g7",
            ['c2g6', ('ponder', 'f6g7')]),
        ("setoption", # setoption
            "setoption name MultiPV value 1",
            {"name": "MultiPV", "value": "1"}),
        ("readyok", # readyok
            "readyok",
            []),
    ])
    def test_parse_encode(self, cmd, line, expected_args):
        m = UCI_msg.parse(line)
        assert m.cmd == cmd
        assert m.args == expected_args
        m.line = None # remove cache
        assert m.encode() == line

    @pytest.mark.parametrize("m1,m2,expected", [
        (UCI_msg({"bestmove": ['0000']}), UCI_msg({"bestmove": ['0000']}), True),
        (UCI_msg({"bestmove": ['0000']}), UCI_msg({"bestmove": []}), False),
        (UCI_msg({"info": {"depth": 1}}), UCI_msg({"info": {"depth": 1}}), True),
        (UCI_msg({"info": {"depth": 1}}), UCI_msg({"info": {"depth": 2}}), False),
    ])
    def test_equal(self, m1, m2, expected):
        equals = m1 == m2
        assert equals == expected

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)

    sys.exit(pytest.main())
