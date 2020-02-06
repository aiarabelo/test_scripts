import re

f = open("POSCAR", "r")
f_read = f.readlines()

g = open("new_POSCAR", "a+")

regex = r"([a-zA-Z]+)+"
r = re.search(regex, f_read[8])

print(r.group(0))