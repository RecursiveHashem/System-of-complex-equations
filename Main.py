import math


class Complex:

    def __init__(self, a, b, p):
        if not p:
            self.real = float(a)
            self.imag = float(b)
        else:
            self.real = a * round(math.cos(math.radians(b)), 5)
            self.imag = a * math.sin(math.radians(b))

    def __str__(self):
        if not self.imag:
            return str(self.real)
        elif not self.real:
            return "j" + str(self.imag)
        else:
            return "( " + str(self.real) + " + " + "j" + str(self.imag) + " )"

    def __neg__(self):
        return Complex(-self.real, -self.imag, 0)

    def __eq__(self, other):
        other = other.EffectiveValue()
        if isinstance(other, Complex):
            return self.real == other.real and self.imag == other.imag
        return False

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        if isinstance(other, int):
            return Complex(self.real + other, self.imag, 0)
        other = other.EffectiveValue()
        if isinstance(other, Expression):
            return (other + self).EffectiveValue()
        if isinstance(other, Complex):
            r = self.real + other.real
            i = self.imag + other.imag
        else:
            r = self.real + other
            i = self.imag
        return Complex(r, i, 0)

    def __sub__(self, other):
        if isinstance(other, int):
            return Complex(self.real - other, self.imag, 0)
        other = other.EffectiveValue()
        if isinstance(other, Expression):
            return (-one * other) + self
        if isinstance(other, Complex):
            r = self.real - other.real
            i = self.imag - other.imag
        else:
            r = self.real - other
            i = self.imag
        return Complex(r, i, 0)

    def __mul__(self, other):
        if isinstance(other, int):
            return Complex(self.real * other, self.imag * other, 0)
        other = other.EffectiveValue()
        if isinstance(other, Expression):
            return other * self
        if isinstance(other, Complex):
            r = self.real * other.real - (self.imag * other.imag)
            i = self.real * other.imag + (self.imag * other.real)
        else:
            r = self.real * other
            i = self.imag * other
        return Complex(r, i, 0)

    def __truediv__(self, other):
        if isinstance(other, int):
            return Complex(self.real / other, self.imag / other, 0)
        other = other.EffectiveValue()
        if isinstance(other, Expression):
            return (Expression.constant(self) / other).EffectiveValue()  # double check
        if isinstance(other, Complex):
            r = other.real / (other.real ** 2 + other.imag ** 2)
            i = -other.imag / (other.real ** 2 + other.imag ** 2)
            res = self * Complex(r, i, 0)
        else:
            res = Complex(self.real / other, self.imag / other, 0)
        return res

    def __pow__(self, other):
        res = one
        i = -1 if other >= 0 else 1
        while other:
            res = self * res if i == -1 else res / self
            other += i
        return res

    def abs(self):
        return math.sqrt(self.real ** 2 + self.imag ** 2)

    def quad(self):
        if self.real >= 0:
            return 1 if self.imag >= 0 else 4
        else:
            return 2 if self.imag >= 0 else 3

    def angle(self):
        ang = math.degrees(math.atan(self.imag / self.real))
        q = self.quad()
        if q == 1 or q == 4:
            return ang
        elif q == 2:
            return ang + 180
        else:
            return ang - 180

    def EffectiveValue(self):
        return self

    def compliment(self):
        return Complex(self.real, -self.imag, 0)


zero = Complex(0, 0, 0)
one = Complex(1, 0, 0)


class Expression:

    def __init__(self, name, c, k):
        self.varName = name
        self.coef = c
        self.const = k.EffectiveValue()

    def EffectiveValue(self):
        # if isinstance(self.coef, Complex):
        #	return self if self.coef != Complex(0, 0) else self.const.EffectiveValue()
        if self.coef.EffectiveValue() == zero:
            return self.const.EffectiveValue()
        return self

    def __str__(self):
        # if self.coef == Complex(0, 0):  # or str(self.coef) == "{0}":
        #	return "{" + str(self.const) + "}"
        self = self.EffectiveValue()
        if isinstance(self, Expression):
            return "[" + str(self.coef) + "]" + str(self.varName) + " + {" + str(self.const) + "}"
        return str(self)

    def __eq__(self, other):
        self = self.EffectiveValue()
        other = other.EffectiveValue()
        if isinstance(other, Expression) and isinstance(self, Expression):
            return self.coef == other.coef and self.const == other.const and self.varName == self.varName
        return self == other

    # double check
    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        other = other.EffectiveValue()
        if isinstance(other, Expression):
            if self.varName == other.varName:
                return Expression(self.varName, self.coef + other.coef, self.const + other.const).EffectiveValue()
        return Expression(self.varName, self.coef, self.const + other).EffectiveValue()

    def __sub__(self, other):
        other = other.EffectiveValue()
        if isinstance(other, Expression):
            if self.varName == other.varName:
                return Expression(self.varName, self.coef - other.coef, self.const - other.const).EffectiveValue()
        return Expression(self.varName, self.coef, self.const - other).EffectiveValue()

    def __mul__(self, other):
        other = other.EffectiveValue()
        return Expression(self.varName, self.coef * other, self.const * other).EffectiveValue()

    def __truediv__(self, other):

        other = other.EffectiveValue()
        """""""""
        if isinstance(other, expression):
            res = self+zero
            res.divider = other * res.divider
        else:
        """""""""
        res = Expression(self.varName, self.coef / other, self.const / other)
        return res.EffectiveValue()

    def __pow__(self, other):
        res = Expression(self.varName, zero, one)
        i = -1 if other >= 0 else 1
        while other:
            res = self * res if i == -1 else res / self
            other += i
        return res

    def inc(self):
        self.const += one
        return self

    def __neg__(self):
        return self * (-one)

    @staticmethod
    def constant(c):
        return Expression("shouldn't be seen", zero, c)


class BoxedExpr:

    def __init__(self, num):
        self.num = num
        self.div = one

    def EffectiveValue(self):
        self.num = self.num.EffectiveValue()
        self.div = self.div.EffectiveValue()
        if isinstance(self.div, Complex) and self.div != one:
            self.num = self.num / self.div
            self.div = one
        return self

    def __str__(self):
        self = self.EffectiveValue()
        num = str(self.num)
        if isinstance(self.div, Expression):
            div = str(self.div)
            return num + "\n" + "-" * max(len(num), len(div)) + "\n" + div
        else:
            return num

    def __neg__(self):
        return 4

    def __eq__(self, other):
        self = self.EffectiveValue()
        other = other.EffectiveValue()
        return self.num == other.num and self.div == other.div

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        other = other.EffectiveValue()
        if not isinstance(other, BoxedExpr):
            res = BoxedExpr(self.num + other)
        else:
            res = BoxedExpr(self.num + other.num)
        return res.EffectiveValue()

    def __sub__(self, other):
        other = other.EffectiveValue()
        if not isinstance(other, BoxedExpr):
            res = BoxedExpr(self.num - other)
        else:
            res = BoxedExpr(self.num - other.num)
        return res.EffectiveValue()

    def __mul__(self, other):
        if isinstance(other, BoxedExpr):
            return (BoxedExpr(self.num * other.num) / (self.div * other.div)).EffectiveValue()
        return (BoxedExpr(self.num * other) / self.div).EffectiveValue()

    def __truediv__(self, other):
        if isinstance(other, BoxedExpr):
            res = BoxedExpr(self.num * other.div)
            res.div = self.div * other.num
        else:
            res = BoxedExpr(self.num)
            res.div = self.div * other
        return res.EffectiveValue()

    def __pow__(self, other):
        res = BoxedExpr(one)
        i = -1 if other >= 0 else 1
        while other:
            res = self * res if i == -1 else res / self
            other += i
        return res


j = Complex(0, 1, 0)
v = Expression("v", zero, zero)
u = BoxedExpr(Expression("u", v, j))
a = Expression("a", one, zero)

x = BoxedExpr(a)

print(v)
print(u)
print(a)

print(x*zero)

