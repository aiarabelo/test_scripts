import re

class ProcessFile:
	"""
	FUNCTION: This class provides methods that for reading the POSCAR
	"""
	def __init__(self, filename="POSCAR2", output_filename="test_POSCAR"):
		self.filename = filename 
		self.output_filename = output_filename

		f = open(self.filename, "r")
		self.f_read = f.readlines()

	# def read_file(self):
	# 	f = open(self.filename, "r")
	# 	self.f_read = f.readlines()

	# 	return self.f_read

	def structure_details(self):
		atomic_species = self.f_read[5].split( )
		number_of_atoms = self.f_read[6].split( )

		return atomic_species, number_of_atoms

	def write_file(self):
		g = open(self.output_filename, "a+")
		self.g = g
		for i in range(0,7):
			g.write(self.f_read[i])

		return self.g 

	def check_format(self):
		try: 
			regex = r"(![a-zA-Z]+)+"
			r = re.search(regex, self.f_read[8])
			print(r.group(0))
		except:
			print("Failed type 1")
			try: 
				regex = r"([a-zA-Z]+)+"
				r = re.search(regex, self.f_read[8])
				print(r.group(0))
			except: 
				print("Failed type 2")
				format_type = 3 
				pass
			else:
				format_type = 2
		else: 
			format_type = 1						

		return format_type, regex

class SelectiveDynamics(ProcessFile):
	def __init__(self, height):
		ProcessFile.__init__(self)

		self.height = float(height)
		self.format_type, self.regex = self.check_format()
		self.atomic_species, self.number_of_atoms = self.structure_details()
		self.g = self.write_file()

	def write_coordinate_labels(self, i, height, format_type, atom_counter = None, r = None):
		"""
		FUNCTION: Adds the selective dynamic labels and adds the atom identity as a comment
		ARGUMENTS: 
			i: the current iteration (loop is in write_coordinates method)
			height: freeze below this height (in Angstroms)
			atom_counter: counter used for labeling 
			r: for regex
		"""
		if format_type == 3:
			if float(self.f_read[i].split( )[2]) < height:
				self.g.write(self.f_read[i].strip("\n") + " T T T !" + self.atomic_species[self.j] + "\n")
			elif float(self.f_read[i].split( )[2]) > height:
				self.g.write(self.f_read[i].strip("\n") + " F F F !" + self.atomic_species[self.j] + "\n")
		else: 	
			if float(self.f_read[i].split( )[2]) < height:
				self.g.write(self.f_read[i].replace(r.group(0), "T T T !" + r.group(0)))
			elif float(self.f_rexad[i].split( )[2]) > height:
				self.g.write(self.f_read[i].replace(r.group(0), "F F F !" + r.group(0)))
			else:
				pass

	def write_coordinates(self, format_type, regex):
		"""
		FUNCTION: Writes the coordinates of the POSCAR, with consideration to formatting
				  to avoid labeling errors 
		ARGUMENTS: 
			format_type: the format of the coordinates as dictated by check_format
			regex: the regular expression used to classify the POSCAR files 
		"""
		self.g.write("selective dynamics \n")
		self.g.write(self.f_read[7])

		if format_type == 3:
			j = 0 
			self.j = j
			c = 8 + int(self.number_of_atoms[j])
		
			for i in range(8,len(self.f_read)):			
				if i == c-1:
					print("i = ", i)
					print("c = ", c)
					print(self.f_read[i].split( )[2], self.atomic_species[j])
					self.write_coordinate_labels(i, self.height, format_type)
					try:
						j=j+1
						c = c + int(self.number_of_atoms[j])
						print("Going onto next element: ", self.atomic_species[j])
					except:
						print("end of loop") 
				else:
					print(self.f_read[i].split( )[2], self.atomic_species[j])
					self.write_coordinate_labels(i, self.height, self.format_type, atom_counter=self.j)
		else: 
			for i in range(8,len(self.f_read)):
				r = re.search(regex, self.f_read[i])
				self.write_coordinate_labels(i, self.height, self.format_type, r=r)

	def execute(self):
		"""
		FUNCTION: execute the script to enable selective dynamics
		ARGUMENTS: 
			height: freeze below this height (in Angstroms)
		"""
		self.write_coordinates(self.format_type, self.regex)

class BiUModeling(ProcessFile):
	
	"""
	FUNCTION: This class provides methods to adjust the POSCAR to treat a certain 
			  layer as the bulk and another layer as the surface depending on
			  the number of layers 
	REMINDER: Put the adsorbate at the end 
	TODO: This is hardcoded for CuO. Consider bond length z-components from PyMatGen
	"""
	def __init__(self, tot_layers=7, surface_layers=2, adsorbate_atoms=2, tolerance=0.01):
		ProcessFile.__init__(self)

		self.tot_layers = int(tot_layers)
		self.surface_layers = int(surface_layers)
		self.adsorbate_atoms = int(adsorbate_atoms)
		self.tolerance = float(tolerance)

	def get_heights(self):
		heights = []

		for height in range(8, len(self.f_read) - self.adsorbate_atoms):
			heights.append(self.f_read[height].split( )[2])

		max_height = float(max(heights))

		height_range = max_height/self.tot_layers
		adjusted_height_range = height_range - self.tolerance
		print(adjusted_height_range)


	def separate_layers(self):
		pass

biu = BiUModeling()
biu.get_heights() 


