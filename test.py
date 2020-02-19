f = open("POSCAR", "r")
f_read = f.readlines()

pd = [f_read[i].split( ) for i in range(8,len(f_read))]
print(pd)