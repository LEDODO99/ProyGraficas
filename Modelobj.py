from SR1 import *
from Textura import *
from math import * 
import copy
from collections import namedtuple
#width = 1920
width = 800
x = 0.1
y = 0.1
#height =1080
height = 800
V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])
zbuffer = [[-99999999999 for x in range(width+1)] for y in range(height+1)]
print(len(zbuffer), len(zbuffer[0]))

def loadModelMatrix(transalte, scale, rotate):
	transalte = V3(*transalte)
	scale = V3(*scale)
	rotate = V3(*rotate)
	translate_matrix=[
		[1,0,0,transalte.x],
		[0,1,0,transalte.y],
		[0,0,1,transalte.z],
		[0,0,0,1]
		]
	scale_matrix = [
			[scale.x,0,0,0],
			[0,scale.y,0,0],
			[0,0,1,scale.z],
			[0,0,0,1]
		]

	a = rotate.x
	rotation_matrix_x =[
			[1,0,0,0],
			[0,cos(a),-sin(a),0],
			[0,sin(a),cos(a),0],
			[0,0,0,1]
		]

	a = rotate.y
	rotation_matrix_y =[
			[cos(a),0,-sin(a),0],
			[0,1,0,0],
			[-sin(a),0,cos(a),0],
			[0,0,0,1]
		]

	a = rotate.z
	rotation_matrix_z =[
			[cos(a),-sin(a),0,0],
			[sin(a),cos(a),0,0],
			[0,0,1,0],
			[0,0,0,1]
		]
	
	rotation_matrix =  mulmat(rotation_matrix_z,mulmat(rotation_matrix_y,rotation_matrix_x))
	#Model = traslate_matrix @ rotation_matrix @ scale_matrix
	model = mulmat(scale_matrix,mulmat(rotation_matrix,translate_matrix))
	#print('model',model)
	return model


class Modelobj(object):
	def __init__(self,filename,material = None):
		with open(filename) as f:
			self.lines = f.read().splitlines()

		with open(material) as f:
			self.linesmtl = f.read().splitlines()

		self.tvertices= []
		self.vertices = []
		self.faces = []
		self.material = {}
		self.normales = []

	def read(self):
		global view
		materialA = ''
		for line in self.lines:
			if line:
				prefix, value = line.split(' ',1)

				if prefix == 'v':
					self.vertices.append(list(map(float,value.split(' '))))
				if prefix == 'vt':
					self.tvertices.append(list(map(float,value.split(' '))))
				if prefix == 'vn':
					self.normales.append(list(map(float,value.split(' '))))
				if prefix == 'f':
					# Separar por espacio
					listf1 = value.split(' ')
					listx = []
					# Ahora separar por guiones y castear a int
					for face in listf1:
						listf2 = face.split('/')
						listf = []
						for t2 in listf2:
							if t2:
								listf.append(int(t2))
							else:
								listf.append(0)
						# Se guarda el material antes de las caras a las que se aplicaran
						listf.append(materialA)
						listx.append(listf)
						self.faces.append(listx)
				# Para ver que material es el que toca a ciertas caras
				elif prefix == 'usemtl':
					materialA = value

	def readMtl(self):
		nameMat = ''
		for line in self.linesmtl:
			if line:
				prefix, value = line.split(' ',1)
				if prefix == 'newmtl':
					nameMat = value
				elif prefix == 'Kd':
					coloresStr = value. split(' ')
					listColores = list(map(float,coloresStr))
					self.material[nameMat] = listColores

	def getverts(self):
		return self.vertices
	def getfaces(self):
		return self.faces
	def getmateriales(self):
		return self.material
	def gettverts(self):
		return self.tvertices
	def getnormales(self):
		return self.normales
		
verts = []

def reverse(var):
	varc = []
	vat = []
	for y in range(0,len(var[0])):
		varf = []
		for x in range(0,len(var)):
			if y == 0 :
				vat.append(1)
			varf.append(var[x][y])

		varc.append(varf)

	varc.append(vat)
	#print(varc)
	return varc

def recover(mat):
    matriz = []
    for y in range(0,len(mat[0])):
        vam = []
        for x in range(0,len(mat)-1):
            vam.append(mat[x][y]/mat[3][y])
        matriz.append(vam)
    #print(matriz)
    return matriz


def mulmat(mat1, mat2):
	#print(mat1)
	mat3 = copy.deepcopy(mat2)
	for y in range(0,len(mat2)):
		for x in range(0,len(mat2[0])):
			mat3[y][x] = fabs(mat3[y][x]*0.0)
	#print(mat3)
	#print(mat1)
	#print(mat2)
	#print(len(mat3[0]))
	#print(len(mat3))
	#print(len(mat1[0]))
	#print(len(mat1))
	#print(len(mat2[0]))
	#print(len(mat2))
	for i in range(0,len(mat1)):
		#print('i =' + str(i))
		for j in range(0,len(mat2[1])):
			#print('j =' + str(j))
			for k in range(0,len(mat2)):
				#print('k =' + str(k))
				mat3[i][j] += mat1[i][k] * mat2[k][j]
				#print(mat3[i][j])
	#print(mat3)
	return mat3

def loadViewMatrix(x,y,z, center):
	M = [
		[x.x, x.y, x.z, 0],
		[y.x, y.y, y.z, 0],
		[z.x, z.y, z.z, 0],
		[0,0,0,1]
		]
	O = [
		[1,0,0,-center.x],
		[0,1,0,-center.y],
		[0,0,1,-center.z],
		[0,0,0,1]
		]
	
	view = mulmat(O,M)
	#print('view', view)
	return view

def loadProjectionMatrix(coeff):
	Projection = [
		[1,0,0,0],
		[0,1,0,0],
		[0,0,1,0],
		[0,0,coeff,1]
	]
	return Projection
#def lookat():	

def draw():
	verts_itter = iter(verts)
	try:
		while True:
			a = next(verts_itter)
			b = next(verts_itter)
			c = next(verts_itter)
			val.line_float(a[0],a[1],b[0],b[1])
			val.line_float(b[0],b[1],c[0],c[1])
			val.line_float(c[0],c[1],a[0],a[1])
	except StopIteration as e:
		print("f")

def loadViewportMatrix():
	Viewport = [
		[width/500,0,0,x+width/500],
		[0,height/500,0,y + height/500],
		[0,0,16,16],
		[0,0,0,1]
		]
	return Viewport
#eye=V3(0,0,1),center=V3(0,0,0),up=V3(0,1,0)
def load(filename,filenameMtl,eye,center,up,transalte, scale, rotate, light, textura = None):
	var = Modelobj(filename,filenameMtl)
	var.read()
	var.readMtl()
	tvertices = var.gettverts()
	vertices = var.getverts()
	faces = var.getfaces()
	materiales = var.getmateriales()
	normals = var.getnormales()
	z = normVec(restVec(eye, center))
	x = normVec(prodx(up,z))
	y = normVec(prodx(z,x))
	vert_buff_object = []
	#print(self.vertices)
	#print(reverse(self.vertices))
	#print('global view', view)
	#print(loadProjectionMatrix(-1/len(restVec(eye,center))))
	 
	matriz = mulmat(loadViewportMatrix(),mulmat(loadProjectionMatrix(-0.1),mulmat(loadViewMatrix(x,y,z, center),loadModelMatrix(transalte, scale, rotate))))
	vertices = mulmat(matriz,reverse(vertices))
	vertices = recover(vertices)
	#print(vertices)
	scal = 0.8


	luz=V3(0.5,0,1)
	for face in faces:
	
		x1=round(scal*(vertices[face[0][0]-1][0]+1)*(getwidth()/2))
		y1=round(scal*(vertices[face[0][0]-1][1]+1)*(getwidth()/2))
		z1=round(scal*(vertices[face[0][0]-1][2]+1)*(getwidth()/2))
		x2=round(scal*(vertices[face[1][0]-1][0]+1)*(getwidth()/2))
		y2=round(scal*(vertices[face[1][0]-1][1]+1)*(getwidth()/2))
		z2=round(scal*(vertices[face[1][0]-1][2]+1)*(getwidth()/2))
		x3=round(scal*(vertices[face[2][0]-1][0]+1)*(getwidth()/2))
		y3=round(scal*(vertices[face[2][0]-1][1]+1)*(getwidth()/2))
		z3=round(scal*(vertices[face[2][0]-1][2]+1)*(getwidth()/2))
		v1 = V3(x1,y1,z1)
		v2 = V3(x2,y2,z2)
		v3 = V3(x3,y3,z3)
		
		normal = normVec(prodx(restVec(v2,v1),restVec(v3,v1)))
		intens = prod(normal,luz)

		if not textura:
			if intens<0:
				pass
			else:
				#print("jjj")
				glColor(materiales[face[0][3]][0]*intens,materiales[face[0][3]][1]*intens,materiales[face[0][3]][2]*intens)
				#glColor(intens,intens,intens)
				triangleM(v1,v2,v3)
		else:
			xe1 = int(textura.width * ((tvertices[face[0][1] - 1][0]))) - 1
			ye1 = int(textura.height * ((tvertices[face[0][1] - 1][1]))) - 1
			xe2 = int(textura.width * ((tvertices[face[1][1] - 1][0]))) - 1
			ye2 = int(textura.height * ((tvertices[face[1][1] - 1][1]))) - 1
			xe3 = int(textura.width * ((tvertices[face[2][1] - 1][0]))) - 1
			ye3 = int(textura.height * ((tvertices[face[2][1] - 1][1]))) - 1
			# Se crean los nuevos vectores de texturas
			t1 = V3(xe1, ye1, 0)
			t2 = V3(xe2, ye2, 0)
			t3 = V3(xe3, ye3, 0)


			for facepart in face:
					#print(facepart)

				norma = V3(*normals[facepart[2]-1])
				vert_buff_object.append(norma)

			n1 = vert_buff_object[0]
			n2 = vert_buff_object[1]
			n3 = vert_buff_object[2]
			vert_buff_object = []
			triangleT(v1,v2,v3,t1,t2,t3,n1,n2,n3,light,textura,intens)
			
			#print("fallo")

def barycentric(A, B, C, P):
	cx, cy, cz = prodx(
		V3(B.x - A.x, C.x - A.x, A.x - P.x),
		V3(B.y - A.y, C.y - A.y, A.y - P.y)
	)

	if cz == 0:
		return -1, -1, -1
	# Coordenadas baricentricas
	u = cx/cz
	v = cy/cz
	w = 1 - (u + v)

	return w,v,u

def bbox(A, B, C):
	xs = sorted([A.x, B.x, C.x])
	ys = sorted([A.y, B.y, C.y])
	return V2(xs[0], ys[0]), V2(xs[2], ys[2])

def triangleM(A, B, C):
	bbox_min, bbox_max = bbox(A, B, C)

	for x in range(bbox_min.x, bbox_max.x + 1):
		for y in range(bbox_min.y, bbox_max.y + 1):
			w, v, u = barycentric(A, B, C, V2(x, y))

			# Si estan fuera del triangulo, no pintar
			if w < 0 or v < 0 or u < 0:
				pass
			else:
				z = A.z * w + B.z * v + C.z * u
				# Si z es mayor que el z buffer, pintar y cambiar valor zbuffer
				try:
					if z > zbuffer[x][y]:
						pointf(x, y)
						zbuffer[x][y] = z
				except:
						pass
def triangleT(A, B, C,tacord, tbcord, tccord, norm1,norm2,norm3,light, texture = None, intense = 1):
	bbox_min, bbox_max = bbox(A, B, C)


	for x in range(bbox_min.x, bbox_max.x + 1):
		for y in range(bbox_min.y, bbox_max.y + 1):
			w, v, u = barycentric(A, B, C, V2(x, y))

			# Si estan fuera del triangulo, no pintar
			if w < 0 or v < 0 or u < 0:
				pass
			else:
				if texture:
					TA,TB,TC = tacord,tbcord,tccord
					tx = TA.x*w + TB.x *v + TC.x *u
					ty = TA.y*w + TB.y *v + TC.y *u
					#color = texture.get_colors(tx,ty,intense)
				
				nA = norm1
				nB = norm2
				nC = norm3	

				color = gourad(
					light,
					texture,
					bar = (w,v,u),
					texture_coords = (tx,ty),
					varying_normals = (nA,nB,nC)
					)
				
					
				z = A.z * w + B.z * v + C.z * u
				# Si z es mayor que el z buffer, pintar y cambiar valor zbuffer
				#try:
				if x<width and x>0 and y<height and y>0 and z > zbuffer[y][x]:
					#glColor(*color)
					pointsf(x, y,color)
					zbuffer[y][x] = z
				#except:
				#		pass			

def prod(v0,v1):
	return (v0.x*v1.x)+(v0.y*v1.y)+(v0.z*v1.z)
def restVec(v0,v1):
	return V3(v0.x-v1.x,v0.y-v1.y,v0.z-v1.z)
def prodx(v0,v1):
	return V3(
	v0.y * v1.z - v0.z * v1.y,
	v0.z * v1.x - v0.x * v1.z,
	v0.x * v1.y - v0.y * v1.x
		)
def magVec(v0):
	return (v0.x**2 + v0.y**2 + v0.z**2)**0.5
def normVec(v0):
	l = magVec(v0)
	if not l:
		return V3(0, 0, 0)
	return V3(v0.x/l, v0.y/l, v0.z/l)

def gourad(light, texture, **kwargs):
	w,v,u = kwargs['bar']

	tx,ty = kwargs['texture_coords']

	nA,nB,nC = kwargs['varying_normals']

	tcolor = texture.get_colors(tx,ty)

	nx = nA.x * w + nB.x * u + nC.x * v
	ny = nA.y * w + nB.y * u + nC.y * v
	nz = nA.z * w + nB.z * u + nC.z * v

	vn = V3(nx,ny,nz)

	intensity = prod(vn, light)

	return color(
		int(tcolor[2]* intensity) if tcolor[2] * intensity > 0 else 0,
		int(tcolor[1]* intensity) if tcolor[1] * intensity > 0 else 0,
		int(tcolor[0]* intensity) if tcolor[0] * intensity > 0 else 0
		)

glCreateWindow(width,height)

val = get_var()
trans = [0.0,0.8]
sca = [1.0,1.0]
light = V3(0,1,1)
eye=V3(0,0,1)
center=V3(0,0,0)
up=V3(0,1,0)
#lookat()
#val.clear()
#textu = None
print('model1')
textu = Textura('TextureDH.bmp')
transalte=(-2.4,-3.01,0.5)
scale=(.455,0.455,0.455)
rotate=(0,0,0.05)
load("Arco.obj","Arco.mtl",eye,center,up,transalte,scale,rotate,light,textu)
#draw()
print('model2')
#textu=None
textu = Textura('TextureFalchion.bmp')
transalte=(-5,-11,-9)
scale=(0.08,0.08,0.08)
rotate=(-0.8,-0.050,0)
load("Falchion.obj","Falchion.mtl",eye,center,up,transalte,scale,rotate,light,textu)

print('model3')
#textu=None
textu = Textura('TextureMS.bmp')
transalte=(-2.5,-4.5,-3.5)
scale=(0.2,0.2,0.2)
rotate=(-0.8,-0.050,0)
load("MasterSword.obj","MasterSword.mtl",eye,center,up,transalte,scale,rotate,light,textu)

print('model4')
#textu=None
textu = Textura('TextureMyrtenaster.bmp')
transalte=(-3.5,-3.73,0)
scale=(0.35,0.35,0.35)
rotate=(0,0,0)
load("Myrtenaster.obj","Myrtenaster.mtl",eye,center,up,transalte,scale,rotate,light,textu)

print('model5')
#textu=None
textu = Textura('TexturaSC.bmp')
transalte=(-3.5,-5.4,-2)
scale=(0.3,0.3,0.3)
rotate=(0,0,0)
load("Doomhammer.obj","Doomhammer.mtl",eye,center,up,transalte,scale,rotate,light,textu)

print('bg')
bg=Textura('Nagrand_Landscape.bmp')
bg.read()
for x in range(width):
        for y in range(height):
                if (zbuffer[y][x]== -99999999999):
                        pointsf(x,y,bg.get_colors(x,y))
#,eye=V3(0,0,1),center=V3(0,0,0),up=V3(0,1,0),transalte=(-0.5,0,0),scale=(0.5,0.5,0.5), rotate=(0,0,0)
#load("Porygon22.obj","Porygon22.mtl",eye=V3(0,0,1),center=V3(0,0,0),up=V3(0,1,0),transalte=(-0.5,0,0),scale=(0.5,0.5,0.5),tex, rotate=(0,0,0))
print('Final')
glFinish()




