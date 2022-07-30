import math
from vector import Vector

import pygame
pygame.init()

class Blob():
	def __init__(self, n=4, e=6, verts=False, fill=False, forces=False):
		self.n = n
		self.e = 6
		self.pos = False
		self.edges = False
		
		self.vel = [Vector() for _ in range(self.n)]
		self.acc = [Vector() for _ in range(self.n)]
		self.acc_int = [Vector() for _ in range(self.n)]
		self.normals = [Vector() for _ in range(self.n)]

		#stiffness > 0.003 makes the equilibrium unstable
		self.k = 0.003 * self.n
		self.b = 3 #normal force coefficient
  
		self.verts = verts
		self.fill = fill
		self.debug = forces
  
	def move(self, bounds):
		for i in range(self.n):
			#print('move>> ', i, self.acc[i])
			self.bound(bounds)
			
			self.vel[i] += self.acc[i] + self.acc_int[i]
			self.vel[i] *= 0.97 #air resistance
			self.pos[i] += self.vel[i]
		self.calc_normals()
		self.spring()
	
	def add_force(self, g):
		for i in range(self.n):
			self.acc[i] = g.resize(0.2)
  
	def spring(self):
		self.acc_int = [Vector() for _ in range(self.n)]
		for i1, i2, dist in self.edges:
			#think of this as a regular spring system
			origin = self.pos[i1]
			x_1 = self.pos[i2]
			dir = (x_1 - origin).normalize() #unit vector
			x_0 = origin + dir * dist
			#F = -k(x - x_0), ignore when negligible
			f = (x_0 - x_1) * -(self.k * dist) #longer springs are stiffer
			
			self.acc_int[i1] += f #two forces
			self.acc_int[i2] -= f #so that each pair is pulled together
   
		#normal force
		for i, edge in enumerate(self.edges):
			i1, i2, dist = edge
			norm = self.normals[i] * self.b / (self.n ** 0.5)
			self.acc_int[i1] += norm
			self.acc_int[i2] += norm
	
	def bound(self, bounds):
		min_x, min_y, max_x, max_y = bounds
		for i in range(self.n):
			if self.pos[i].y >= max_y:
				#All collisions will lose energy - faster = more loss
				self.pos[i].y = 2 * max_y - self.pos[i].y
				#self.vel[i].y = -abs(self.vel[i].y) * 0.9 if abs(self.vel[i].y) > 1000 else 0
				self.vel[i].y = min(self.vel[i].y, 0)
				self.vel[i].x *= 0.9
    
			if self.pos[i].y <= min_y:
				#All collisions will lose energy - faster = more loss
				self.pos[i].y = 2 * min_y - self.pos[i].y
				#self.vel[i].y = -abs(self.vel[i].y) * 0.9 if abs(self.vel[i].y) > 1000 else 0
				self.vel[i].y = max(self.vel[i].y, 0)
				self.vel[i].x *= 0.9
    
			if self.pos[i].x >= max_x:
				#All collisions will lose energy - faster = more loss
				self.pos[i].x = 2 * max_x - self.pos[i].x
				#self.vel[i].y = -abs(self.vel[i].y) * 0.9 if abs(self.vel[i].y) > 1000 else 0
				self.vel[i].x = min(self.vel[i].x, 0)
				self.vel[i].y *= 0.9
    
			if self.pos[i].x <= min_x:
				#All collisions will lose energy - faster = more loss
				self.pos[i].x = 2 * min_x - self.pos[i].x
				#self.vel[i].y = -abs(self.vel[i].y) * 0.9 if abs(self.vel[i].y) > 1000 else 0
				self.vel[i].x = max(self.vel[i].x, 0)
				self.vel[i].y *= 0.9


	def calc_normals(self):
		self.normals = []
		for i1, i2, dist in self.edges:
			p1 = self.pos[i1]
			p2 = self.pos[i2]
			self.normals.append(Vector.from_rads((p2-p1).ang() - math.radians(90)))

	def generate_points(self, rad, center, ang_offset):
		self.pos = []
		for i in range(self.n):
			angle = i * 2 * math.pi / self.n + math.radians(ang_offset)
			offset = Vector(math.cos(angle), math.sin(angle)) * rad
			self.pos.append(center + offset)

	def add_points(self, verts_pos):
		self.pos = []
		for x, y in verts_pos:
			self.pos.append(Vector(x, y))
		self.n = len(self.pos)

	def generate_edges(self, vert_pairs):
		self.edges = []
		for verts in vert_pairs:
			i1, i2 = verts
			p1 = self.pos[i1]
			p2 = self.pos[i2]
			dist = (p2-p1).mag()
			self.edges.append((i1, i2, dist))
		self.e = len(self.edges)
  
	def draw(self, disp):
		if self.fill:
			pygame.draw.polygon(disp, (41, 155, 217), [p() for p in self.pos])
   
		for edge in self.edges:
			p1, p2, dist = edge
			color = (0,0,0)
			pygame.draw.line(disp, color, self.pos[p1](), self.pos[p2](), 2)
		
		if self.verts:
			for pos in self.pos:
				pygame.draw.circle(disp, (255,0,0), pos(), 2)		
   
		if self.debug:
			for i, edge in enumerate(self.edges):
				i1, i2, dist = edge
				p1 = self.pos[i1]
				p2 = self.pos[i2]
				mid = (p1 + p2) / 2
				norm = mid + self.normals[i] * 20
				pygame.draw.line(disp, (0, 100, 255), mid(), norm())
     
			for i, pos in enumerate(self.pos):
				pygame.draw.line(disp, (255,255,0), pos(), (pos + self.acc[i].normalize() * 30)())
				pygame.draw.line(disp, (0,255,0), pos(), (pos + self.acc_int[i].normalize() * 30)())