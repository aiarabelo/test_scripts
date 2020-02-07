import re

f = open("POSCAR", "r")
f_read = f.readlines()

g = open("new_POSCAR", "a+")

for i in range(0,7):
	g.write(f_read[i])

selective_dynamics = input("Turn on Selective Dynamics? [y/n]: ")

format_type = None
regex = None

atomic_species = f_read[5].split( )
number_of_atoms = f_read[6].split( )

def check_format():
	## TODO: Fix this. does not recognize types 1 and 2 
	regex = r"(![a-zA-Z]+)+"
	r = re.search(regex, f_read[8])

	try: 
		print(r.group(0))
	except:
		print("Failed type 1")
		regex = r"([a-zA-Z]+)+"
		pass
	else: 
		format_type = 1
	try: 
		print(r.group(0))
	except: 
		print("Failed type 2")
		format_type = 3 
		pass
	else:
		format_type = 2

	print("Note: format may be unidentified. Please check POSCAR format and revise code if necessary.")
	print("Format type:", format_type)

	return format_type, regex

def enable_selective_dynamics(format_type, regex):
	g.write("selective dynamics \n")
	g.write(f_read[7])

	height = float(input("Freeze below what height (in Angstroms)? "))

	if format_type == 3:
		# TODO: Fix numbering 
		j = 0 
		c = 8 + int(number_of_atoms[j])
	
		for i in range(8,len(f_read)):			
			if i == c-1:
				print(f_read[i].split( )[2], atomic_species[j])
				print("i = ", i)
				print("c = ", c)
				if float(f_read[i].split( )[2]) < height:
					g.write(f_read[i].strip("\n") + " T T T !" + atomic_species[j] + "\n")
				elif float(f_read[i].split( )[2]) > height:
					g.write(f_read[i].strip("\n") + " F F F !" + atomic_species[j] + "\n")
				try:
					j=j+1
					c = c + int(number_of_atoms[j])
					print("Going onto next element: ", atomic_species[j])
				except:
					print("end of loop") 
			else:
				print(f_read[i].split( )[2], atomic_species[j])
				print("i = ", i)
				print("c = ", c)
				if float(f_read[i].split( )[2]) < height:
					g.write(f_read[i].strip("\n") + " T T T !" + atomic_species[j] + "\n")
				elif float(f_read[i].split( )[2]) > height:
					g.write(f_read[i].strip("\n") + " F F F !" + atomic_species[j] + "\n")

				

	else: 
		try:
			for i in range(8,len(f_read)):
				r = re.search(regex, f_read[i])
				if float(f_read[i].split( )[2]) < height:
					g.write(f_read[i].replace(r.group(0), "T T T !" + r.group(0)))
				elif float(f_read[i].split( )[2]) > height:
					g.write(f_read[i].replace(r.group(0), "F F F !" + r.group(0)))
				else:
					pass
		except: 
			print("Unidentified format")

## TO DO: Make modules and classes and shit 

if selective_dynamics == "y":
		format_type, regex = check_format()
		print(format_type, regex)
		enable_selective_dynamics(format_type, regex)
else:
	pass	










