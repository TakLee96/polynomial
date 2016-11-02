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
>>> f = x ** TWO + log(E, x) + ONE
>>> f
((x ^ 2 + ln(x)) + 1)
>>> f(x=1)
2.0
>>> f_x = d(f, x)
>>> f_x
([2 * x] + [1 / x])
>>> f_x(x=1)
3.0
```

