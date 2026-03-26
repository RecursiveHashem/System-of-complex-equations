def contains(s, char):
    s = str(s)
    for i in s:
        if i == char:
            return True
    return False


def EffectiveValue(self):
    if isinstance(self, tuple) or isinstance(self, list):
        if len(self) == 2 or len(self) == 4:
            return self
        coef = EffectiveValue(self[0])
        if coef == [0, 0] or coef == (0, 0):
            return EffectiveValue(self[1])
    return self


def areEqual(self, other):
    other = EffectiveValue(other)
    self = EffectiveValue(self)
    equals = len(other) == len(self)
    if equals:
        for i in range(len(other)):
            equals = self[i] == other[i] and equals
    return equals


def Display(self):
    self = EffectiveValue(self)
    if isinstance(self, tuple) or isinstance(self, list):
        if len(self) == 2:
            if not self[1]:
                return str(self[0])
            elif not self[0]:
                return "j" + str(self[1])
            else:
                return "( " + str(self[0]) + " + " + "j" + str(self[1]) + " )"
        elif len(self) == 3:
            return "[" + Display(self[0]) + "]" + self[2] + " + {" + Display(self[1]) + "}"
        else:
            res = Display(EffectiveValue((self[0], self[1], self[2])))
            res2 = Display(self[3])
            res = res + "\n" + "-" * max(len(res), len(res2)) + "\n" + res2
            return res
    return str(self)


def subt(self, other):
    if len(self) == 2 and len(other) == 2:
        return (self[0] - other[0], self[1] - other[1])
    if len(self) == 3 and len(other) == 3:
        if self[2] == other[2]:
            return EffectiveValue((subt(self[0], other[0]), subt(self[1], other[1]), self[2]))
    if len(self) == 3:
        return (self[0], subt(self[1], other), self[2])
    if len(other) == 3:
        return (mult(other[0], [-1, 0]), subt(self, other[1]), other[2])


def mult(self, other):
    if len(self) == 2 and len(other) == 2:
        r = self[0] * other[0] - (self[1] * other[1])
        i = self[0] * other[1] + (self[1] * other[0])
        return (r, i)
    if len(self) == 3:
        return EffectiveValue((mult(self[0], other), mult(self[1], other), self[2]))
    if len(other) == 3:
        return (mult(other[0], self), mult(other[1], self), other[2])


def div(self, other):
    other = EffectiveValue(other)
    self = EffectiveValue(self)
    if len(self) == 2 and len(other) == 2:
        r = other[0] / (other[0] ** 2 + other[1] ** 2)
        i = -other[1] / (other[0] ** 2 + other[1] ** 2)
        return mult(self, (r, i))
    if len(other) == 2:
        return EffectiveValue((div(self[0], other), div(self[1], other), self[2]))
    if len(self) == 3:
        return [self[0], self[1], self[2], other]
    return [(0, 0), (self[0], self[1]), "Default", other]

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
        return (eval(s[0]), 0)
    if len(s) == 2:
        return (eval(s[0]), eval(s[1]))
    if len(s) == 3:
        return [[eval(s[0]), eval(s[1])], [0, 0], s[2]]
    return [[eval(s[0]), eval(s[1])], [eval(s[3]), eval(s[4])], s[2]]


def bettertreatStr(s):
    s = s.split("+")
    summ = (0, 0)
    for i in s:
        summ = subt(summ, treatStr(i))
    return mult(summ, (-1, 0))


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
        return subt(mult(m[0][0], m[1][1]), mult(m[0][1], m[1][0]))
    res = (0, 0)
    alt = True
    for i in range(len(m)):
        res = subt(res, mult(mult(m[0][i], (-1,0)), det(exclude(m, 0, i)))) if alt else subt(res, mult(m[0][i], det(exclude(m, 0, i))))
        alt = not alt
    return res


def replacewithlast(m, row):
    new = excluderow(m, len(m) - 1)
    new[row] = m[len(m) - 1]
    return new


def solve(m):
    W = det(excluderow(m, len(m) - 1))
    print("\nW :", Display(W) + "\n")
    res = []
    for i in range(len(m) - 1):
        temp = det(replacewithlast(m, i))
        res.append(temp)
    for i in range(len(res)):
        final = Display(div(res[i], W))
        print(str(i + 1), ":", Display(res[i]), "\n" + final + "\n")


solve(getMatrix())
