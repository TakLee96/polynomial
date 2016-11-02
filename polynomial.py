from __future__ import division
from math import e as __e__, log as __log__, pi as __pi__

class Expr:
    def __add__(self, other):
        assert isinstance(other, Expr)
        return Add.make(self, other)
    def __sub__(self, other):
        assert isinstance(other, Expr)
        return Sub.make(self, other)
    def __mul__(self, other):
        assert isinstance(other, Expr)
        return Mul.make(self, other)
    def __div__(self, other):
        assert isinstance(other, Expr)
        return Div.make(self, other)
    def __truediv__(self, other):
        assert isinstance(other, Expr)
        return Div.make(self, other)
    def __pow__(self, other):
        assert isinstance(other, Expr)
        return Pow.make(self, other)
    def __log__(self, other):
        assert isinstance(other, Expr)
        return Log.make(self, other)
    def __repr__(self):
        return str(self)
    def __call__(self, **kwargs):
        for name in kwargs:
            self = self.evaluate(name, kwargs[name])
        return self

class Var (Expr):
    def __init__(self, name):
        self.name = name
    def derivative(self, name):
        if self.name == name:
            return Val(1)
        return ZERO
    def evaluate(self, name, value):
        if self.name == name:
            return Val(value)
        return self
    def involves(self, name):
        return self.name == name
    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name
    def __str__(self):
        return str(self.name)

class Val (Expr):
    def __init__(self, value):
        self.value = value
    def derivative(self, name):
        return Val(0)
    def evaluate(self, name, value):
        return self
    def involves(self, name):
        return False
    def __eq__(self, other):
        return isinstance(other, Val) and self.value == other.value
    def __str__(self):
        if self.value == __pi__:
            return "pi"
        elif self.value == __e__:
            return "e"
        return str(self.value)

class Op (Expr):
    def __init__(self, one, other):
        self.one = one
        self.other = other
    def __eq__(self, other):
        return False
    def involves(self, name):
        return self.one.involves(name) or self.other.involves(name)

class Add (Op):
    @staticmethod
    def make(one, other):
        if isinstance(one, Val) and isinstance(other, Val):
            return Val(one.value + other.value)
        elif one == ZERO:
            return other
        elif other == ZERO:
            return one
        elif one == other:
            return TWO * one
        else:
            return Add(one, other)
    def derivative(self, name):
        if not self.involves(name): return self
        return self.one.derivative(name) + self.other.derivative(name)
    def evaluate(self, name, value):
        return self.one.evaluate(name, value) + self.other.evaluate(name, value)
    def __str__(self):
        return "(" + str(self.one) + " + " + str(self.other) + ")"

class Sub (Op):
    @staticmethod
    def make(one, other):
        if isinstance(one, Val) and isinstance(other, Val):
            return Val(one.value - other.value)
        elif one == ZERO:
            return Val(-1) * other
        elif other == ZERO:
            return one
        elif one == other:
            return ZERO
        else:
            return Sub(one, other)
    def derivative(self, name):
        if not self.involves(name): return self
        return self.one.derivative(name) - self.other.derivative(name)
    def evaluate(self, name, value):
        return self.one.evaluate(name, value) - self.other.evaluate(name, value)
    def __str__(self):
        return "(" + str(self.one) + " - " + str(self.other) + ")"

class Mul (Op):
    @staticmethod
    def make(one, other):
        if isinstance(one, Val) and isinstance(other, Val):
            return Val(one.value * other.value)
        elif one == ZERO or other == ZERO:
            return ZERO
        elif one == ONE:
            return other
        elif other == ONE:
            return one
        else:
            return Mul(one, other)
    def derivative(self, name):
        if not self.involves(name): return self
        return self.one * self.other.derivative(name) + self.one.derivative(name) * self.other
    def evaluate(self, name, value):
        return self.one.evaluate(name, value) * self.other.evaluate(name, value)
    def __str__(self):
        return "[" + str(self.one) + " * " + str(self.other) + "]"

class Div (Op):
    @staticmethod
    def make(one, other):
        if isinstance(one, Val) and isinstance(other, Val):
            return Val(one.value / other.value)
        elif one == ZERO:
            return ZERO
        elif other == ZERO:
            raise Exception("zero division")
        elif other == ONE:
            return one
        else:
            return Div(one, other)
    def derivative(self, name):
        if not self.involves(name): return self
        return (self.one.derivative(name) * self.other - self.one * self.other.derivative(name)) / (self.other * self.other)
    def evaluate(self, name, value):
        return self.one.evaluate(name, value) / self.other.evaluate(name, value)
    def __str__(self):
        return "[" + str(self.one) + " / " + str(self.other) + "]"

class Pow (Op):
    @staticmethod
    def make(one, other):
        if isinstance(one, Val) and isinstance(other, Val):
            return Val(one.value ** other.value)
        elif one == ZERO and other == ZERO:
            raise Exception("zero to zero power")
        elif one == ONE or other == ZERO:
            return ONE
        elif other == ONE:
            return one
        else:
            return Pow(one, other)
    def derivative(self, name):
        if not self.involves(name):
            return self
        elif isinstance(self.other, Val):
            return self.other * (self.one ** (self.other - ONE)) * self.one.derivative(name)
        elif isinstance(self.one, Val):
            return (self.one * log(E, self.one)) * self.other * self.other.derivative(name)
        return (log(E, self.one) * self.other).derivative(name) * self
    def evaluate(self, name, value):
        return self.one.evaluate(name, value) ** self.other.evaluate(name, value)
    def __str__(self):
        return str(self.one) + " ^ " + str(self.other)

class Log (Op):
    @staticmethod
    def make(one, other):
        if isinstance(one, Val) and isinstance(other, Val):
            return Val(__log__(other.value, one.value))
        elif isinstance(one, Val) and one.value <= 0:
            raise Exception("base less than zero")
        elif isinstance(other, Val) and other.value <= 0:
            raise Exception("log number less than zero")
        elif other == ONE:
            return ZERO
        elif one == other:
            return ONE
        else:
            return Log(one, other)
    def derivative(self, name):
        if not self.involves(name):
            return self
        elif self.one == E:
            return self.other.derivative(name) / self.other
        elif isinstance(self.one, Val):
            return self.other.derivative(name) / self.other / log(E, self.one)
        return (log(E, self.other) / log(E, self.one)).derivative(name)
    def evaluate(self, name, value):
        return log(self.one.evaluate(name, value), self.other.evaluate(name, value))
    def __str__(self):
        if self.one == E: return "ln(" + str(self.other) + ")"
        return "log(" + str(self.one) + ", " + str(self.other) + ")"

# Constants
ZERO = Val(0)
ONE = Val(1)
TWO = Val(2)
E = Val(__e__)
PI = Val(__pi__)

# Functions
log = lambda a, b: a.__log__(b)
d = lambda f, x: f.derivative('x')
