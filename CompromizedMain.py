import math
def contains(s, char):
    s = str(s)
    for i in s:
        if i == char:
            return True
    return False

class Complex:

    def __init__(self, a=0, b=0, p=0):
        if p == 0 or p == "0":
            self.real = float(a) if contains(a, ".") else int(a)
            self.imag = float(b) if contains(b, ".") else int(b)
        else:
            self.real = float(a) * round(math.cos(math.radians(float(b))), 5)
            self.imag = float(a) * round(math.sin(math.radians(float(b))), 5)

    def __str__(self):
        if not self.imag:
            return str(self.real)
        elif not self.real:
            return "j" + str(self.imag)
        else:
            return "( " + str(self.real) + " + " + "j" + str(self.imag) + " )"

    def subt(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Complex(self.real - other, self.imag)
        r = self.real - other.real
        i = self.imag - other.imag
        return Complex(r, i)

    def mult(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Complex(self.real * other, self.imag * other)
        r = self.real * other.real - (self.imag * other.imag)
        i = self.real * other.imag + (self.imag * other.real)
        return Complex(r, i)

    def div(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Complex(self.real / other, self.imag / other)
        r = other.real / (other.real ** 2 + other.imag ** 2)
        i = -other.imag / (other.real ** 2 + other.imag ** 2)
        return self.mult( Complex(r, i))


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
    return Complex(s[0], s[1], s[2])

def getMatrix():
    n = int(input("Num of equations : "))
    m = []
    for j in range(n + 1):
        m.append([])
    for j in range(n):
        for i in range(n + 1):
            m[i].append(treatStr(input("( " + str(j + 1) + " , " + str(i + 1) + " ) : ")))
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
        return (m[0][0].mult(m[1][1])).subt((m[0][1].mult(m[1][0])))
    res = Complex()
    alt = True
    for i in range(len(m)):
        res = (res.subt(m[0][i].mult(Complex(-1).mult(det(exclude(m, 0, i)))))) if alt else (res.subt(m[0][i].mult(det(exclude(m, 0, i)))))
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
        final = str(res[i].div(W))
        print(str(i + 1), ":", str(res[i]), "\n --> ", final + "\n")

solve(getMatrix())
