from copy  import deepcopy
listaVisitados = []

class Board(object):# Objeto llamado Tablero

	def __init__(self, blocks): # COPIA DE MANERA PROFUNDA UN BLOQUE Y SE LO ASIGNA AL BLOQUE PROPIO DEL OBJETO
		self.blocks = deepcopy(blocks)

	def tileAt(self, i, j): # TOMA UNA SECCION DEL BLOQUE Y LA RETURNA
		return self.blocks[i][j]

	def size(self): # OBTIENE EL TAMAÑO DEL BLOQUE
		return len(self.blocks)

	def goal(self): # ESTE METODO SE LLAMA OBJETIVO (AQUI SE USA EL ALGORITMO MANHATTAN)
		return self.manhattan() == 0

	def __eq__(self, other):
		if isinstance(other, self._class_):
			return self._dict_ == other._dict_
		return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def neighbors(self):
		row, col = 0, 0 # columnas = 0 , filas = 0
		while self.blocks[row][col] != 0: # se le da un tamaño al bloque (el bloque es un arreglo row * col)
			col += 1 # cada vez que se haga el ciclo se le suma 1 a las columnas
			if col == self.size(): # PREGUNTA SI COLUMNAS ES IGUAL AL TAMAÑO DEL B
				row += 1 # LE SUMAMOS 1 A LA FILA
				col  = 0 # REINICIAMOS COLUMNA EN 0

		neighbors = list() # CREA A LOS VECINOS COMO UNA LISTA
		if self.valid(row-1,col): # VALIDA SI PUEDE RESTAR UNA FILA
			b = Board(deepcopy(self.blocks)) # CREA UN NUEVO TABLERO
			b.exch(row-1,col,row,col) # INTERCAMBIA 
			neighbors.append(b) # AGREGA EL BLOQUE EN LA LISTA DE LOS VECINOS

		if self.valid(row,col+1):
			b = Board(deepcopy(self.blocks))
			b.exch(row,col+1,row,col)
			neighbors.append(b)

		if self.valid(row+1,col):
			b = Board(deepcopy(self.blocks))
			b.exch(row+1,col,row,col)
			neighbors.append(b)

		if self.valid(row,col-1):
			b = Board(deepcopy(self.blocks))
			b.exch(row,col-1,row,col)
			neighbors.append(b)

		return neighbors

	def valid(self, row, col):
		if row < 0 or row > self.size() - 1: return False
		if col < 0 or col > self.size() - 1: return False
		return True

	def exch(self, frow, fcol, trow, tcol):
		tmp = self.blocks[frow][fcol]
		self.blocks[frow][fcol] = self.blocks[trow][tcol]
		self.blocks[trow][tcol] = tmp

	def twin(self):
		twin = deepcopy(self.blocks)
		for i in range(2):
			if twin[i][0] != 0 and twin[i][1] != 0:
				twin[i][0], twin[i][1] = twin[i][1], twin[i][0]
				break
		return Board(twin)

	def __str__(self):
		out = '%2r\n' % self.size()
		for i in range(self.size()):
			for j in range(self.size()):				
				out += ' %2r' % self.blocks[i][j] if self.blocks[i][j] != 0 else '   ' 
			out += '\n'
		return out

def imprimirBloque(b):
	for x in b.neighbors():
		print(x)
		#print(b)
def encolarEstado(cola, bloque):# POR CADA BLOQUE QUE TENEMOS, BUSCAMOS SUS POSIBLES ESTADOS (RETORNAMOS UNA COLA)
	for x in bloque.neighbors():
		cola.append(x)
	cola.pop(0) # ELIMINAMOS EL PRIMER ESTADO PARA BUSCAR QUE NO SE REPITA EL ANALISIS HASTA EL INFITNITO
	return cola
	
def generarLista(bloque):# GENERAMOS UNA LISTA APARTIR DE UN BLOQUE, USAMOS EL METODO DE LOS BLOQUES QUE NOS PERMITE UBICAR DATO POR DATO, ENTENDEMOS QUE UN BLOQUE ES UNA MATRIX X*Y
# NOSOTROS GENERAMOS LA LISTA PARA PODER COMPARAR LISTASOLUCION == LISTADEPRUEBA
	listaT = []

	lista1 = []
	lista2 = []
	lista3 = []
	lista4 = []

	fila = 0
	col = 0

	while fila <= 3:
		if fila == 0:
			if col <= 3:
				lista1.append(bloque.tileAt(fila,col))
				col += 1
			else:
				listaT.append(lista1)
				fila += 1
				col = 0

		if fila == 1:
			if col <= 3:
				lista2.append(bloque.tileAt(fila,col))
				col += 1
			else:
				listaT.append(lista2)
				fila += 1
				col = 0

		if fila == 2:
			if col <= 3:
				lista3.append(bloque.tileAt(fila,col))
				col += 1
			else:
				listaT.append(lista3)
				fila += 1
				col = 0

		if fila == 3:
			if col <= 3:
				lista4.append(bloque.tileAt(fila,col))
				col += 1
			else:
				listaT.append(lista4)
				fila += 1
				col = 0

	return listaT

def ComprobarVistado(listaVisitados, ListaPrueba):

	tamanoLista = len(listaVisitados)
	contador = 0

	while contador < tamanoLista:
		print(ListaPrueba, " = ", listaVisitados[contador])
		if ListaPrueba == listaVisitados[contador]:
			print("Estado visitado")
			return 1
		contador += 1
	return 0

		
def comprobarSolucion(cola):# CONE EL ARGUMENTO COLA, HACERMOS LA BUSQUEDA

	primerElmC = cola.pop(0) # SACAMOS EL PRIMER ELEMENTO QUE TENGA LA COLA

	fin = False
	while fin == False:	
		if ComprobarVistado(listaVisitados, generarLista(primerElmC)) == 1:
			primerElmC = cola.pop(0)
		else:
			listaVisitados.append(generarLista(primerElmC))
			fin == True
		

	xSol = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]] # ESTADO AL QUE QUEREMOS LLEGAR (SOLUCION)

	if generarLista(primerElmC) == xSol:# COMPARAMOS POR SI ENCONTRAMOS LA SOLUCION Y SI ES ASI RETORNAMOS 1
		print(primerElmC)
		print("Estado solucion encontrado")
		return 1
	else: # SINO, CON EL PRIMER ESATADO SACADO DE LA COLA, BUSCAMOS SUS VECIONOS Y LOS ENCOLAMOS (FINAL MENTE RETORNAMOS LA COLA NUEVA)
		print(primerElmC)
		cola = encolarEstado(cola, primerElmC) # CON EL ESTADO QUE NO FUNCIONO, BUSCAMOS A SUS VECINOS Y LOS EN COLAMOS
		listaVisitados.append(generarLista(primerElmC))
		return cola


if __name__ == '__main__':
	
	# 8  1  3        1  2  3     1  2  3  4  5  6  7  8    1  2  3  4  5  6  7  8
    # 4     2        4  5  6     ----------------------    ----------------------
    # 7  6  5        7  8        1  1  0  0  1  1  0  1    1  2  0  0  2  2  0  3

    # initial          goal         Hamming = 5 + 0          Manhattan = 10 + 0

	#x = [[7,0,2],[8,5,3],[6,4,1]]
	#x = [[1,2,3],[4,5,6],[8,7,0]]
	#x = [[1,2,3],[4,0,6],[8,5,7]]
	#x = [[0,1,3],[4,2,5],[7,8,6]]
	#x = [[8,1,3],[4,0,2],[7,6,5]]
	#x = [[6,0,5],[8,7,4],[3,2,1]]
	x = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,0,14,15]] # ESTADO INCIAL PARA DAR SOLUCION
	#x = [[1,2,3,4],[6,10,7,8],[5,0,11,12],[9,13,14,15]] 
	#--------------------------------------------------------------
	cola = []

	xSol = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]] # ESTADO AL QUE QUEREMOS LLEGAR (SOLUCION)


	b = Board(x) #Creamos un bloque
	
	if generarLista(b) == xSol: # PREGUNTAMOS SI EL ESTADO INICIAL ES EL ESTADO SOLUCIOM
		print("Estado solucion encontrado")
	else: # SINO REALIZAMOS EL ALGORITMO QUE BUSQUEDA 
		listaVisitados.append(generarLista(b))
		
		cont = 0 # UN CONTADOR SIMPLE

		# IMPRIMIMOS EL ESTADO INICIAL
		print("--------------- ESTADO INICIAL ----------------\n")
		print(b)
		print("-----------------------------------------------\n")

		fin = 1 # CREAMOS UNA BANDERA QUE FINALIZA EL CICLO
		while fin != 0: # EL CICLO TERMINA CUANDO FIN SEA DISTINTO DE 0

			cont += 1
			print("---------- ITERACION # ", cont , (" -----------\n"))
			cola = encolarEstado(cola,b) #Encolamos a sus vecinos, O ESTADOS POSIIBLES Y ACTUALIZAMOS LA COLA
			cola = comprobarSolucion(cola) # SEGUN EL ALGORITMO BUSCAMOS SOLUCION (NOS PUEDE RETORNAR LA COLA NUEVA A ANALIZAR O SOLO UN 1 CUANDO SE ENCOTRO SOLUCION)
			if cola == 1: # SI COLA ES 1 ES PORQUE SE ENCONTRO SOLUCION
				fin = 0 

	#print(len(cola)) # ESTO ME DA EL TAMAÑO DE LOS DATOS EN LA COLA
	#print(len(b.neighbors()))  # ESTO ME DA LA CANTIDAD DE MOVS QUE SE PUEDEN HACER EN UN ESTADO DETERMINADO