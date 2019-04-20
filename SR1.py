"""
Universidad del Valle de Guatemala
Josue David Lopez Florian
17081
Graficas por computadora
seccion 10
"""

import struct
from collections import namedtuple
#from random import randint as random

def char(c):
	return struct.pack("=c",c.encode('ascii'))
def word(c):
	return struct.pack("=h",c)
def dword(c):
	return struct.pack("=l",c)
def color(r,g,b):
	b = max(0,min(b,255))
	g = max(0,min(g,255))
	r = max(0,min(r,255))
	return bytes([b,g,r])



#clase que funciona para crear un objeto, del cual surgira la imagen
class Bitmap(object):
	#se inicializan las variables con las cuales se trabajara para crear la imagen
	def __init__(self, width,height):
		#variables de ancho y altura delfondo de la imagen
		self.width = width
		self.height = height
		#variables que dan posicion 0,0 en el viewport
		self.Initx = 0
		self.Inity = 0
		#variables del ancho y largo de la ventana del viewport
		self.vpwidth = 0
		self.vpheight = 0
		#variables que dan el color al fondo de la imagen
		self.r1 = 255
		self.g1 = 255
		self.b1 = 255
		#variables que dan el color al glVertex que dibuja pixeles en la pantalla
		self.r2 = 255
		self.g2 = 255
		self.b2 = 255
		#el framebuffer para pintar en la pantalla.
		self.framebuffer = []
		self.clear()


	#funcion que limpia toda la imagen del fondo de un color
	def clear(self):
		self.framebuffer = [[color(self.r1,self.g1,self.b1) for x in range(self.width)] for y in range(self.height)]
		
	"""
	funcion que cambia el color que limpia la pantalla
	a,c,d = valor float entre 0 y 1 para cambiar el color
	"""
	def clearColor(self,a,c,d):
		self.r1 = int(round(a *255.0)) 
		self.g1 = int(round(c *255.0))
		self.b1 = int(round(d *255.0))

	def gwidth(self):
		return self.width

	def gheight(self):
		return self.height
	"""
	esta funcion define la pantalla donde se dibujara en la imagen
	x = posicion horizontal de donde estara el viewport
	y = posicion vertical donde estara ubicado el viewport
	ancho = el tamaño del ancho del viewport a definir
	alto = el tamaño del alto del viewport a definir
	"""
	def ViewPort(self,x, y, ancho, alto):
		self.Initx = x + (ancho/2)
		self.Inity = y + (alto/2)
		self.vpheight = alto/2 
		self.vpwidth = ancho/2
	"""
	funcion que cambia el color con el que se pinta en la pantalla
	z,x,y = valores entre 0 y 1 por el cual cambiara el color
	"""
	def changeColor(self,z,x,y):
		self.r2 = int(round(z *255.0)) 
		self.g2 = int(round(x *255.0))
		self.b2 = int(round(y *255.0))
	"""
	funcion la cual creara la imagen con extencion .bmp
	filename = nombre del archivo con el cual se va a guardar
	"""
	def createFile(self, filename):
		f = open(filename, 'wb')

		#file header
		f.write(char('B'))
		f.write(char('M'))
		f.write(dword(54 + self.width * self.height *3))
		f.write(dword(0))
		f.write(dword(54))

		#image header 40
		f.write(dword(40))
		f.write(dword(self.width))
		f.write(dword(self.height))
		f.write(word(1))
		f.write(word(24))
		f.write(dword(0))
		f.write(dword(self.width * self.height *3))	
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))

		for x in range(self.height):
			for y in range(self.width):
				f.write(self.framebuffer[x][y])

		f.close()
	"""
	funcion que pinta un punto en la imagen
	x = posicion en el horizontal donde se pintara
	y = posicion en el vertical donde se pintara
	"""
	def vertex(self, x, y):
		self.framebuffer[int(round((self.Inity + (y * self.vpheight))))][int(round((self.Initx + (x * self.vpheight))))] = color(self.r2,self.g2,self.b2)

	def punto(self, x, y):
		self.framebuffer[ y ][ x ] = color(self.r2,self.g2,self.b2)

	def puntofz(self, x1, y1):
		x1 += round(self.width/8)
		y1 -= 10
		try:
			self.framebuffer[ y1 ][ x1 ] = color(self.r2,self.g2,self.b2)
		except:
			pass

	def puntofzq(self, x1, y1,colors):
		x1 += round(self.width/8)
		y1 -= 10
		try:
			self.framebuffer[ y1 ][ x1 ] = colors
		except:
			pass

	def line_float(self,x1,y1,x2,y2):
		if x1 >=-1 and y1 >=-1 and x2 >=-1 and y2 >=-1 and x1 <=1 and y1 <=1 and x2 <=1 and y2<=1:
			x1 *= self.width/2
			x2 *= self.width/2
			y1 *= self.height/2
			y2 *= self.height/2
			x1 = round(x1)
			x2 = round(x2)
			y1 = round(y1)
			y2 = round(y2)

			x1 += round(self.width/2)
			x2 += round(self.width/2)
			y1 += (round(self.height/2)) -1
			y2 += (round(self.height/2)) -1

			dy = abs(y2-y1)
			dx = abs(x2-x1)
			
			steep = dy >dx
			
			if steep:
				x1,y1 = y1,x1
				x2,y2 = y2,x2

			if x1>x2:
				x1,x2 = x2,x1
				y1,y2 = y2,y1

			dy = abs(y2-y1)
			dx = abs(x2-x1)

			offset = 0 *2 *dx
			threshold =0.5 *2 *dx
			y = y1

			for x in range(x1,x2, +1):

				if steep:
					point(y,x)
				else:
					point(x,y)  
				offset += dy
				if offset >= threshold:
					y +=1 if y1 <y2 else -1
					threshold +=1 *dx
		else:
			print("solo puede ingresar valores entre -1 y 1")

	def line_in(self,x1,y1,x2,y2):

		dy = abs(y2-y1)
		dx = abs(x2-x1)

		steep = dy >dx

		if steep:
			x1,y1 = y1,x1
			x2,y2 = y2,x2

		if x1>x2:
			x1,x2 = x2,x1
			y1,y2 = y2,y1

		dy = abs(y2-y1)
		dx = abs(x2-x1)

		offset = 0 *2 *dx
		threshold =0.5 *2 *dx
		y = y1

		for x in range(x1,x2, +1):

			if steep:
				point(y,x)
			else:
				point(x,y)  
			offset += dy
			if offset >= threshold:
				y +=1 if y1 <y2 else -1
				threshold +=1 *dx

	def pointbz(self, x, y, color):
		self.framebuffer[x][y] = color

var = None
def get_var():
	return var
	
#funcion con el que se inicia, pero no hace nada, pues el maestro me dijo que lo dejara vacio.
def glInit():
	global var
	var = Bitmap(width,height)
"""
funcion que genera el objeto bitmap para la ventana
width = ancho de la ventana
height = alto de la ventana
"""
def glCreateWindow(width, height):
	global var
	var = Bitmap(width,height)
"""
funcion para crear el viewport y la funcion que la genera
x = posicion horizontal de donde estara el viewport
y = posicion vertical donde estara ubicado el viewport
width = el tamaño del ancho del viewport a definir
height = el tamaño del alto del viewport a definir
"""
def glViewPort(x, y, width, height):
	var.ViewPort(x,y, width, height)
#funcion que limpia la pantalla
def glClear():
	var.clear()
"""
funcion para generar el cambio de color del clearcolor
r,g,b = valores entre 0 a 1
"""
def glClearColor(r, g, b):
	var.clearColor(r,g,b)
"""
funcion que pinta un punto llamando a la funcion point
x,y = de la posicion entre 0 y 1
"""
def  glVertex(x, y):
	var.vertex(x,y)
"""
funcion para el cambio de color para pintar
r,g,b = valores entre 0 a 1
"""
def  glColor(r, g, b):
	var.changeColor(r,g,b)
"""
funcion que permite dibujar un punto en la imagen.
recibe valores enteros para la corrdenada
"""
def point(x,y):
	var.punto(x,y)
"""
funcion que pinta lineas, pero con con valores entre -1 a 1 en la imagen
"""
def glline_fl(x1,y1,x2,y2):
	var.line_float(x1,y1,x2,y2)
"""
funcion que pinta lineas con valores enteros como coordenadas en la imagen
"""
def glLine(x1,y1,x2,y2):
	var.line_in(x1,y1,x2,y2)

#funcion para crear y mandar el nombre del archivo
def glFinish():
	var.createFile("Proyecto1Final.bmp")

def pointsf( x, y, color):
	var.puntofzq(x, y, color)

def pointf( x, y):
	var.puntofz( x, y)
def getwidth():
	return var.gwidth()

def getheight():
	return var.gheight()
#------------------------------------
#aqui se puede hacer uso de las funciones y probarlas para llamarlas
"""
var = glCreateWindow(300,300)
glViewPort(50,50, 100,100)
glClearColor(0.23,0.36,0.32)
glClear()
glColor(0.5,0.65,0.3)
glVertex(1, 1)
glVertex(1, -1)
glVertex(-1, -1)
glVertex(-1, 1)

glFinish()
"""
