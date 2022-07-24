import math

class Vector():
	def __init__(self, _x=0, _y=0):
		self.x = _x
		self.y = _y
		
	def __repr__(self): #Represent the object as a string
		return f'<{self.x},{self.y}>'
	
	def __call__(self): #call the object as a function
		return self.x, self.y
	
	def __add__(self, other): #addition
		return Vector(self.x + other.x, self.y + other.y)
	
	def __sub__(self, other): #subtraction
		return Vector(self.x - other.x, self.y - other.y)
	
	def __mul__(self, coeff): #multiplication (scaling)
		return Vector(self.x * coeff, self.y * coeff)
		
	def __truediv__(self, coeff): #division (scaling)
		return Vector(self.x / coeff, self.y / coeff)
	
	def __iadd__(self, other): #addition
		return self + other
	
	def __isub__(self, other): #subtraction
		return self - other
	
	def __imul__(self, coeff): #multiplication (scaling)
		return self * coeff
		
	def __itruediv__(self, coeff): #division (scaling)
		return self / coeff
  
	def mag(self): #magnitude
		return (self.x ** 2 + self.y ** 2) ** (1/2)

	def normalize(self):
		if self.mag() == 0:
			return Vector()
		return self / self.mag()
	
	def ang(self):
		return math.atan2(self.y, self.x)

	def resize(self, scale):
		return self.normalize() * scale

	def from_tuple(tup):
		x,y = tup
		return Vector(x,y)

	def from_rads(rad):
		return Vector(math.cos(rad), math.sin(rad))

	def average(vecs):
		a = Vector()
		for vec in vecs:
			a += vec
		return a / len(vecs)