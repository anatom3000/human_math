from abc import ABC

from symbolics.nodes import Node, BinaryOperatorNode, EvaluateError


class NodeWithOperatorSupport(Node, ABC):

    def __add__(self, other):
        if isinstance(other, Node):
            return Add(self, other)
        else:
            return self + Value(other)

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Node):
            return Sub(self, other)
        else:
            return self - Value(other)

    __rsub__ = __sub__

    def __mul__(self, other):
        if isinstance(other, Node):
            return Mul(self, other)
        else:
            return self * Value(other)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Node):
            return Div(self, other)
        else:
            return self / Value(other)

    __rtruediv__ = __truediv__

    def __pow__(self, other):
        if isinstance(other, Node):
            return Pow(self, other)
        else:
            return self ** Value(other)

    __rpow__ = __pow__

    def __mod__(self, other):
        if isinstance(other, Node):
            return Mod(self, other)
        else:
            return self % Value(other)

    __rmod__ = __mod__


class ReduceableBinaryOperator(BinaryOperatorNode, ABC):
    def reduce(self):
        if isinstance(self.left, Value) and isinstance(self.right, Value):
            return self.evaluate()
        else:
            return type(self)(self.left.reduce(), self.right.reduce())


class Value(NodeWithOperatorSupport):

    def __init__(self, value: float):
        self.value = value
        print(f"Initiaizing a value: {self.value}")

    def evaluate(self):

        if isinstance(self.value, Node):
            return self.value.evaluate()
        else:
            return self.value

    def __repr__(self):
        if (not isinstance(self.value, Node)) and self.value.is_integer():
            return repr(int(self.value))
        else:
            return repr(self.value)


class Variable(NodeWithOperatorSupport):

    def __init__(self, name: str):
        self.name = name

    def evaluate(self):
        raise EvaluateError("can't evaluate a variable")

    def reduce(self):
        return self

    def __repr__(self):
        return self.name


class Add(ReduceableBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self):
        return Value(self.left.evaluate() + self.right.evaluate())

    def __repr__(self):
        return f"({repr(self.left)} + {repr(self.right)})"


class Sub(ReduceableBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self):
        return Value(self.left.evaluate() - self.right.evaluate())

    def __repr__(self):
        return f"({repr(self.left)} - {repr(self.right)})"


class Mul(ReduceableBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self):
        return Value(self.left.evaluate() * self.right.evaluate())

    def __repr__(self):
        return f"({repr(self.left)} * {repr(self.right)})"


class Div(ReduceableBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self):
        return Value(self.left.evaluate() / self.right.evaluate())

    def __repr__(self):
        return f"({repr(self.left)} / {repr(self.right)})"


class Pow(ReduceableBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self):
        return Value(self.left.evaluate() ** self.right.evaluate())

    def __repr__(self):
        return f"({repr(self.left)} ** {repr(self.right)})"


class Mod(ReduceableBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self):
        return Value(self.left.evaluate() % self.right.evaluate())

    def __repr__(self):
        return f"({repr(self.left)} % {repr(self.right)})"
