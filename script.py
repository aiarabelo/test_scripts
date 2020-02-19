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

	def write_labels(self, standard, i, label1, label0):
		"""
		FUNCTION: Write labels, depending on functionality
		ARGUMENTS:
			standard: for bi U modeling this would be what decides if it's a surface or not
					  for selective dynamics this would be what decides what should be frozen or not (height)
			label: the label at the end of the coordinates
				   for bi U modeling this is just a comment of classification of bulk (1)/surface (0)and what species it corresponds to
				   for selective dynamics this is the T T T (1) or F F F (0) and a comment of the species
		"""

		if self.format_type == 3:
			if float(self.f_read[i].split( )[2]) < standard:
				self.g.write(self.f_read[i].strip("\n") + label1 + self.atomic_species[self.j] + "\n")
			elif float(self.f_read[i].split( )[2]) > standard:
				self.g.write(self.f_read[i].strip("\n") + label0 + self.atomic_species[self.j] + "\n")
		else: 	
			if float(self.f_read[i].split( )[2]) < standard:
				self.g.write(self.f_read[i].replace(self.r.group(0), label1 + self.r.group(0)))
			elif float(self.f_rexad[i].split( )[2]) > standard:
				self.g.write(self.f_read[i].replace(self.r.group(0), label0 + self.r.group(0)))
			else:
				pass


class SelectiveDynamics(ProcessFile):
	def __init__(self, height):
		ProcessFile.__init__(self)

		self.height = float(height)
		self.format_type, self.regex = self.check_format()
		self.atomic_species, self.number_of_atoms = self.structure_details()
		self.g = self.write_file()

	def write_coordinate_labels(self, i, height, format_type):
		"""
		FUNCTION: Adds the selective dynamic labels and adds the atom identity as a comment
		ARGUMENTS: 
			i: the current iteration (loop is in write_coordinates method)
			height: freeze below this height (in Angstroms)
			atom_counter: counter used for labeling 
			r: for regex
		"""
		self.write_labels(height, i, label1 = " T T T !", label0 = " F F F !")

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
					self.write_coordinate_labels(i, self.height, self.format_type)
					try:
						self.j=self.j+1
						c = c + int(self.number_of_atoms[j])
						print("Going onto next element: ", self.atomic_species[self.j])
					except:
						print("end of loop") 
				else:
					print(self.f_read[i].split( )[2], self.atomic_species[self.j])
					self.write_coordinate_labels(i, self.height, self.format_type)
		else: 
			for i in range(8,len(self.f_read)):
				r = re.search(regex, self.f_read[i])
				self.r = r 
				self.write_coordinate_labels(i, self.height, self.format_type)

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
			  the number of layers specified
	REMINDER: Put the adsorbate at the end 
	TODO: This is hardcoded for CuO (clean). Consider bond length z-components from PyMatGen and surfaces with adsorbed atoms
	"""
	def __init__(self, tot_layers=7, surface_layers=2, adsorbate_atoms=2, tolerance=0, atoms = "Cu_B Cu O O"):
		ProcessFile.__init__(self)

		self.tot_layers = int(tot_layers)
		self.surface_layers = int(surface_layers)
		self.adsorbate_atoms = int(adsorbate_atoms)
		self.tolerance = float(tolerance)
		self.format_type, self.regex = self.check_format()
		self.atoms = atoms
		self.g = self.write_file()
		self.atomic_species, self.number_of_atoms = self.structure_details()

	def get_heights(self):
		heights = []

		for height in range(8, len(self.f_read) - self.adsorbate_atoms):
			heights.append(self.f_read[height].split( )[2])

		max_height = float(max(heights))

		height_range = max_height/self.tot_layers
		adjusted_height_range = height_range - self.tolerance
		return adjusted_height_range

	def get_bulk_height(self):
		self.adjusted_height_range = self.get_heights()
		bulk_height = self.adjusted_height_range*(self.tot_layers-self.surface_layers)
		return bulk_height

	def rearrange_layers(self):
		"""
		FUNCTION: Rearranges layers (intention: within each species)
		ARGUMENTS: 
			.
		"""
		pass

	def write_coordinate_labels(self):
		pass

	def write_coordinates(self):
		"""
		FUNCTION: Writes 
		"""
		pass

		

	# def write_coordinate_labels(self, i, height):
	# 	"""
	# 	FUNCTION: Adds the selective dynamic labels and adds the atom identity as a comment
	# 	ARGUMENTS: 
	# 		i: the current iteration (loop is in write_coordinates method)
	# 		height: freeze below this height (in Angstroms)
	# 		atom_counter: counter used for labeling 
	# 		r: for regex
	# 	"""
	# 	self.write_labels(height, i, label1 = " ! bulk", label0 = " ! surface")

	# def write_coordinates(self, i, adjusted_height_range, atom_counter = None, r = None):
	# 	"""
	# 	FUNCTION: Adds the selective dynamic labels and adds the atom identity as a comment
	# 	ARGUMENTS: 
	# 		i: the current iteration (loop is in write_coordinates method)
	# 		height: freeze below this height (in Angstroms)
	# 		atom_counter: counter used for labeling 
	# 		r: for regex
	# 	"""
	# 	bulk_counter = 0
	# 	self.bulk_counter = bulk_counter
	# 	j = 0 
	# 	self.j = j

	# 	self.g.write(self.f_read[7])			
	
	# 	if self.format_type == 3:

	# 		c = 8 + int(self.number_of_atoms[j])
		
	# 		for i in range(8,len(self.f_read)):			
	# 			if i == c-1:
	# 				# self.write_layer_labels(i, self.height, format_type)
	# 				try:
	# 					self.j=self.j+1
	# 					c = c + int(self.number_of_atoms[j])
	# 					print("Going onto next element: ", self.atomic_species[self.j])
	# 				except:
	# 					print("end of loop") 
	# 			else:
	# 				print(self.f_read[i].split( )[2], self.atomic_species[self.j])
	# 				# self.write_layer_labels(i, self.height, self.format_type, atom_counter=self.j)
				
	# 			if float(self.f_read[i].split( )[2]) < self.adjusted_height_range*(self.tot_layers-self.surface_layers):
	# 				self.g.write(self.f_read[i].strip("\n") + " ! bulk " + self.atomic_species[self.j] + "\n")
	# 				if self.j == 0:
	# 					self.bulk_counter = self.bulk_counter + 1
	# 			elif float(self.f_read[i].split( )[2]) > self.adjusted_height_range*(self.tot_layers-self.surface_layers):
	# 				self.g.write(self.f_read[i].strip("\n") + " ! surface " + self.atomic_species[self.j] + "\n")
	# 	else: 
	# 		print("type asd")
	# 		for i in range(8,len(self.f_read)):
	# 			r = re.search(self.regex, self.f_read[i])
	# 			# self.write_layer_labels(i, self.height, self.format_type, r=r)

	# 			if float(self.f_read[i].split( )[2]) < self.adjusted_height_range*(self.tot_layers-self.surface_layers):
	# 				if self.j == 0:
	# 					self.bulk_counter = self.bulk_counter + 1
	# 			elif float(self.f_read[i].split( )[2]) > self.adjusted_height_range*(self.tot_layers-self.surface_layers):
	# 				self.g.write(self.f_read[i].replace(r.group(0), " ! surface " + r.group(0)))
	# 			else:
	# 				pass

	# 	return self.bulk_counter


	# def separate_layers(self, bulk_counter):

	# 	f2 = open(self.output_filename, "r")
	# 	self.f2_read = f2.readlines()

	# 	h = open("new_POSCAR", "a+")
	# 	self.h = h 
	# 	for i in range(0, 5):
	# 		h.write(self.f2_read[i])

	# 	h.write(self.atoms + "\n")

	# 	h.write(str(self.bulk_counter) + " ")
	# 	for x in range(0, int(self.j)+1):
	# 		if x == 0: 
	# 			h.write(str(int(self.number_of_atoms[x]) - self.bulk_counter) + " ")
	# 		else: 
	# 			try: 
	# 				h.write(str(self.number_of_atoms[x]) + " ")

	# 			except: 
	# 				h.write("\n")
	# 	h.write("\n")
	# 	for i in range(8, len(self.f2_read)):
	# 		h.write(self.f2_read[i])

	# def rearrange_layers(self):
	# 	"""
	# 	FUNCTION: Rearranges the POSCAR coordinates according to z-coordinate, and then according to y-coordinate. 
	# 			  This is most relevant when working with antiferromagnetic materials, due to magnetic moments being relevant.
	# 	ARGUMENTS: 
			
	# 	"""
	# 	pass

	def execute(self):
	# 	adjusted_height_range = self.get_heights()
	# 	self.bulk_counter = self.write_coordinates(self.adjusted_height_range, self.regex)
	# 	print(self.bulk_counter)
	# 	self.separate_layers(self.bulk_counter)
		pass
		

class FixMAGMOM():
	pass

class BiUWithSelectiveDynamics(ProcessFile):
	pass


sd = SelectiveDynamics("0.38")
sd.execute()