from __future__ import annotations

from collections.abc import MutableSequence
from typing import Optional, Type

from human_math.symbolics import Node
from human_math.tokens import Token, tokenize
from .processors import Parentheses, TokenProcessor, ImplicitMulitplication, Signs, Wildcard
from .tokens import Add, Sub, Pow, Num, Mul, Div, Mod, ParentheseOpen, ParentheseClose, Name, WildcardClose, \
    WildcardOpen

TOKENS = [
    Num,
    Add,
    Sub,
    Mul,
    Div,
    Pow,
    Mod,
    ParentheseOpen,
    ParentheseClose,
    Name,
    WildcardOpen,
    WildcardClose
]

TOKENS_PROCESSORS: list[Type[TokenProcessor]] = [
    ImplicitMulitplication,
    Parentheses,
    Signs,
    Num,
    Name,
    Wildcard,
    Pow,
    Div,
    Mul,
    Mod,
    Sub,
    Add,
]


class ParsingError(Exception):
    pass


def parse_tokens(token_stream: MutableSequence[Token | Node]) -> Optional[Node]:
    for op in TOKENS_PROCESSORS:
        # print(f"Before {op.__name__}: \n\t{token_stream = }")
        token_stream = op.to_node(token_stream)

    if len(token_stream) == 0:
        return None

    if len(token_stream) != 1:
        print(token_stream)
        raise ParsingError("incorrect number of nodes/tokens remaining after parsing")

    result = token_stream[0]

    if not isinstance(result, Node):
        raise ParsingError(f"unknown token found {result}")

    return result


def parse(expression: str) -> Node:
    return parse_tokens(tokenize(expression, TOKENS, raise_on_unknown=True))  # type: ignore
