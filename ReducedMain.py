
def contains(s, char):
    s = str(s)
    for i in s:
        if i == char:
            return True
    return False

class Complex:

    def __init__(self, a=0, b=0):
        self.real = float(a) if contains(a, ".") else int(a)
        self.imag = float(b) if contains(b, ".") else int(b)

    def __eq__(self, other):
        other = other.EffectiveValue()
        if isinstance(other, Complex):
            return self.real == other.real and self.imag == other.imag
        return False
    def __str__(self):
        if not self.imag:
            return str(self.real)
        elif not self.real:
            return "j" + str(self.imag)
        else:
            return "( " + str(self.real) + " + " + "j" + str(self.imag) + " )"



    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Complex(self.real - other, self.imag)
        other = other.EffectiveValue()
        if isinstance(other, Expression):
            return (Complex(-1) * other) + self
        r = self.real - other.real
        i = self.imag - other.imag
        return Complex(r, i)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Complex(self.real * other, self.imag * other)
        other = other.EffectiveValue()
        if isinstance(other, Expression):
            return other * self
        r = self.real * other.real - (self.imag * other.imag)
        i = self.real * other.imag + (self.imag * other.real)
        return Complex(r, i)

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Complex(self.real / other, self.imag / other)
        other = other.EffectiveValue()
        r = other.real / (other.real ** 2 + other.imag ** 2)
        i = -other.imag / (other.real ** 2 + other.imag ** 2)
        return self * Complex(r, i)

    def EffectiveValue(self):
        return self



zero = Complex()
one = Complex(1)


class Expression:

    def __init__(self, name, c=one, k=zero):
        self.varName = name
        self.coef = c
        self.const = k.EffectiveValue()

    def EffectiveValue(self):
        if self.coef.EffectiveValue() == zero:
            return self.const.EffectiveValue()
        return self

    def __str__(self):
        self = self.EffectiveValue()
        if isinstance(self, Expression):
            return "[" + str(self.coef) + "]" + str(self.varName) + " + {" + str(self.const) + "}"
        return str(self)

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
        return Expression(self.varName, self.coef / other, self.const / other).EffectiveValue()


def printl(l):
    s = "["
    for i in l:
        s += " " + str(i) + ","
    s = s[:-1] + " ]"
    print(s)


def printm(m):
    print()
    for i in range(len(m)):
        printl(m[i])
    print("\n")


def treatStr(s):
    s = s.split(",")
    if len(s) == 1:
        return Complex(s[0])
    if len(s) == 2:
        return Complex(s[0], s[1])
    if len(s) == 3:
        return Expression(s[2], Complex(s[0], s[1]))
    return Expression(s[2], Complex(s[0], s[1]), Complex(s[3], s[4]))


def bettertreatStr(s):
    s = s.split("+")
    summ = zero
    for i in s:
        summ = summ + treatStr(i)
    return summ

def getMatrix():
    n = int(input("Num of equations : "))
    m = []
    for j in range(n + 1):
        m.append([])
    for j in range(n):
        for i in range(n + 1):
            m[i].append(bettertreatStr(input("( " + str(i + 1) + " , " + str(j + 1) + " ) : ")))
    return m


def excluderow(m, row):
    new = []
    for i in range(len(m)):
        if i != row:
            new.append(m[i])
    return new


def excludecol(m, col):
    new = []
    for i in range(len(m)):
        new.append([])
        for j in range(len(m[i])):
            if j != col:
                new[i].append(m[i][j])
    return new


def exclude(m, row, col):
    return excludecol(excluderow(m, row), col)

def det(m):
    if len(m) == 2:
        return (m[0][0] * m[1][1]) - (m[0][1] * m[1][0])
    res = zero
    alt = True
    for i in range(len(m)):
        res = (res + m[0][i] * det(exclude(m, 0, i))) if alt else (res - m[0][i] * det(exclude(m, 0, i)))
        alt = not alt
    return res

def replacewithlast(m, row):
    new = excluderow(m, len(m) - 1)
    new[row] = m[len(m) - 1]
    return new

def solve(m):
    W = det(excluderow(m, len(m) - 1))
    print("\nW :", str(W) + "\n")
    res = []
    for i in range(len(m) - 1):
        temp = det(replacewithlast(m, i))
        res.append(temp)
    for i in range(len(res)):
        final = str(res[i]/W) if not isinstance(W, Expression) else str(res[i]) + "\n" + "-" * max(len(str(res[i])), len(str(W))) + "\n" + str(W)
        print(str(i + 1), ":", str(res[i]), "\n --> ", final + "\n")
    return res

M = getMatrix()
solve(M)
