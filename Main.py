
import math

class Complex:
	
	def __init__(self,r,i):
		self.real = float(r)
		self.imag = float(i)
	
	def __str__(self):
		if not self.imag:
			return str(self.real)
		elif not self.real:
			return "j"+str(self.imag)
		else:
			return "( "+ str(self.real)+ " + " + "j"+str(self.imag)+" )"
	
	
	def __add__(self,other):
		if isinstance(other,Complex):
			self.real+=other.real
			self.imag+=other.imag
		else:
			self.real+=other
		return self
	
	def __sub__(self,other):
		if isinstance(other,Complex):
			self.real-=other.real
			self.imag-=other.imag
		else:
			self.real-=other
		return self
	
	def __mul__(self,other):
		if isinstance(other,Complex):
			r = self.real*other.real - (self.imag*other.imag)
			i = self.real*other.imag + (self.imag*other.real)
			self.real = r
			self.imag = i
		else:
			self.real*=other
			self.imag*=other
		return self
	
	def __truediv__(self,other):
		if isinstance(other,Complex):
			r = other.real/(other.real**2 + other.imag**2)
			i =-other.imag/(other.real**2 + other.imag**2)
			self*= Complex(r,i)
		else:
			self.real/=other
			self.imag/=other
		return self
		
	def abs(self):
		return math.sqrt(self.real**2 + self.imag**2)
	
	def quad(self):
		if self.real>=0:
			return 1 if self.imag>=0 else 4
		else:
			return 2 if self.imag>=0 else 3
	
	def angle(self):
		ang = math.degrees(math.atan(self.imag/self.real))
		q = self.quad()
		if q == 1 or q == 4:
			return ang
		elif q == 2:
			return ang + 180
		else:
			return ang - 180
		
		
	



class expression:
	
	def __init__(self, name):
		self.varName = name
		self.coef = Complex(1,0)
		self.const = Complex(0,0)
	
	def __str__(self):
		return str(self.coef) + str(self.varName) + " + " + str(self.const)
	
	def __add__(self,other):
		if isinstance(other,expression):
			pass
		else:
			self.const+=other
		return self
		
		
	def __sub__(self,other):
		if isinstance(other,expression):
			pass
		else:
			self.const-=other
		return self
	

	def __mul__(self,other):
		if isinstance(other,expression):
			pass
		else:
			self.const*=other
			self.coef*=other
		return self
	
	def __tuediv__(self,other):
		if isinstance(other,expression):
			pass
		else:
			self.const/=other
			self.coef/=other
		return self


#z = Complex(2,1)
#x = Complex(0,2)

#v = expression("y")



#hohohiho