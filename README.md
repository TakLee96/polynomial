# A simple implementation of polynomial

To launch the interactive session of python:

```
python -i polynomial.py
```

Or launch it with python3:

```
python3 -i polynomial.py
```

To create a polynomial with one variable:

```
>>> x = Var('x')
>>> f = x ** TWO + log(E, x) + Val(3)
>>> f
((x ^ 2 + ln(x)) + 3)
>>> f(x=1)
4.0
>>> f_x = d(f, x)
>>> f_x
([2 * x] + [1 / x])
>>> f_x(x=1)
3.0
```

Built-in `Val` objects

```
ZERO
ONE
TWO
E
PI
```

Built-in methods

```
def log(Expr a, Expr b) => Expr
def d(Expr f, str|Var x) => Expr
```

- log is different from math.log as the base is the first argument
- d simply takes the derivative of f with respect to x
