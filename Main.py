
import math

class Complex:
	
	def __init__(self, a, b, p):
		if not p:
			self.real = float(a)
			self.imag = float(b)
		else:
			self.real = a*round(math.cos(math.radians(b)), 5)
			self.imag = a*math.sin(math.radians(b))
	
	def __str__(self):
		if not self.imag:
			return str(self.real)
		elif not self.real:
			return "j"+str(self.imag)
		else:
			return "( "+ str(self.real)+ " + " + "j"+str(self.imag)+" )"

	def refresh(self):
		self = self.EffectiveValue()
		return self

	def __eq__(self, other):
		if isinstance(other, Complex):
			return self.real == other.real and self.imag == other.imag
		return False

	def __ne__(self, other):
		return not self == other

	def __add__(self, other):
		if isinstance(other.refresh(), expression):
			return other+self
		if isinstance(other, Complex):
			r = self.real+other.real
			i = self.imag+other.imag
		else:
			r = self.real+other
			i = self.imag
		return Complex(r, i, 0)
	
	def __sub__(self, other):
		if isinstance(other, Complex):
			r = self.real-other.real
			i = self.imag-other.imag
		else:
			r = self.real-other
			i = self.imag
		return Complex(r, i, 0)
	
	def __mul__(self, other):
		if isinstance(other, Complex):
			r = self.real*other.real - (self.imag*other.imag)
			i = self.real*other.imag + (self.imag*other.real)
		else:
			r = self.real*other
			i = self.imag*other
		return Complex(r, i, 0)
	
	def __truediv__(self, other):
		if isinstance(other, Complex):
			r = other.real/(other.real**2 + other.imag**2)
			i = -other.imag/(other.real**2 + other.imag**2)
			res = self * Complex(r, i, 0)
		else:
			res = Complex(self.real / other, self.imag / other, 0)
		return res

	def __pow__(self, other):
		res = Complex(1, 0, 0)
		i = -1 if other >= 0 else 1
		while other:
			res = self * res if i == -1 else res / self
			other += i
		return res

	def abs(self):
		return math.sqrt(self.real**2 + self.imag**2)
	
	def quad(self):
		if self.real >= 0:
			return 1 if self.imag >= 0 else 4
		else:
			return 2 if self.imag >= 0 else 3
	
	def angle(self):
		ang = math.degrees(math.atan(self.imag/self.real))
		q = self.quad()
		if q == 1 or q == 4:
			return ang
		elif q == 2:
			return ang + 180
		else:
			return ang - 180

	def EffectiveValue(self):
		return self
		
	



class expression:
	
	def __init__(self, name, c, k):
		self.varName = name
		self.coef = c
		self.const = k

	def EffectiveValue(self):
		#if isinstance(self.coef, Complex):
		#	return self if self.coef != Complex(0, 0) else self.const.EffectiveValue()
		if self.coef.EffectiveValue() == Complex(0, 0, 0):
			return self.const.EffectiveValue()
		return self

	def refresh(self):
		self = self.EffectiveValue()
		return self

	def __str__(self):
		#if self.coef == Complex(0, 0):  # or str(self.coef) == "{0}":
		#	return "{" + str(self.const) + "}"
		self.refresh()
		if isinstance(self, expression):
			return "[" + str(self.coef) + "]" + str(self.varName) + " + {" + str(self.const) + "}"
		return str(self)

	def __eq__(self, other):
		self.refresh()
		other = other.EffectiveValue()
		if isinstance(other, expression) and isinstance(self, expression):
			return self.coef == other.coef and self.const == other.const and self.varName == self.varName
		return self == other
	# double check
	def __ne__(self, other):
		return not self == other
	
	def __add__(self, other):
		self.refresh()
		if isinstance(other.refresh(), expression):
			pass
		else:
			res = expression(self.varName, self.coef, self.const + other)
		return res

	def __sub__(self, other):
		if isinstance(other, expression):
			pass
		else:
			res = expression(self.varName, self.coef, self.const - other)
		return res

	def __mul__(self, other):
		if isinstance(other, expression):
			pass
		else:
			res = expression(self.varName, self.coef * other, self.const * other)
		return res
	
	def __truediv__(self, other):
		if isinstance(other, expression):
			pass
		else:
			res = expression(self.varName, self.coef / other, self.const / other)
		return res

	def __pow__(self, other):
		res = expression(self.varName, 0, 1)
		i = -1 if other >= 0 else 1
		while other:
			res = self * res if i == -1 else res / self
			other += i
		return res


z = Complex(0, 1, 0)
x = Complex(0, 0, 0)
y = Complex(1, 90, 1)
v = expression("y", x, x)
u = expression("x", v, z)


print(y)
print(u)

