import re

class ReadFile():
	def __init__(self, filename="POSCAR2"):
		f = open(filename, "r")
		f_read = f.readlines()

		g = open("new_POSCAR", "a+")
		for i in range(0,7):
			g.write(f_read[i])

		atomic_species = f_read[5].split( )
		number_of_atoms = f_read[6].split( )

	def check_format(self):
		try: 
			regex = r"(![a-zA-Z]+)+"
			r = re.search(regex, f_read[8])
			print(r.group(0))
		except:
			print("Failed type 1")
			try: 
				regex = r"([a-zA-Z]+)+"
				r = re.search(regex, f_read[8])
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

class SelectiveDynamics(ReadFile):
	def __init__(self):
		format_type, regex = self.check_format()
		print(format_type, regex)		

	def write_coordinate_labels(self, i, height, format_type, atom_counter = None, r = None):
		if format_type == 3:
			if float(f_read[i].split( )[2]) < height:
				g.write(f_read[i].strip("\n") + " T T T !" + atomic_species[j] + "\n")
			elif float(f_read[i].split( )[2]) > height:
				g.write(f_read[i].strip("\n") + " F F F !" + atomic_species[j] + "\n")
		else: 	
			if float(f_read[i].split( )[2]) < height:
				g.write(f_read[i].replace(r.group(0), "T T T !" + r.group(0)))
			elif float(f_read[i].split( )[2]) > height:
				g.write(f_read[i].replace(r.group(0), "F F F !" + r.group(0)))
			else:
				pass

	def enable_selective_dynamics(self, format_type, regex):
		g.write("selective dynamics \n")
		g.write(f_read[7])

		height = float(input("Freeze below what height (in Angstroms)? "))

		if format_type == 3:
			j = 0 
			c = 8 + int(number_of_atoms[j])
		
			for i in range(8,len(f_read)):			
				if i == c-1:
					print("i = ", i)
					print("c = ", c)
					print(f_read[i].split( )[2], atomic_species[j])
					write_coordinate_labels(i, height, format_type)
					try:
						j=j+1
						c = c + int(number_of_atoms[j])
						print("Going onto next element: ", atomic_species[j])
					except:
						print("end of loop") 
				else:
					print(f_read[i].split( )[2], atomic_species[j])
					write_coordinate_labels(i, height, format_type, atom_counter=j)
		else: 
			for i in range(8,len(f_read)):
				r = re.search(regex, f_read[i])
				write_coordinate_labels(i, height, format_type, r=r)


## TO DO: Make modules and classes and shit 








