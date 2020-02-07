import re

f = open("POSCAR", "r")
f_read = f.readlines()

g = open("new_POSCAR", "a+")

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
print(f_read[8])
print(regex)
print(format_type)