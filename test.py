f = open("POSCAR2", "r")
f_read = f.readlines()

x = [f_read[i].split( ) for i in range(8,len(f_read))]


x.sort(key=lambda y: y[1])
x.sort(key=lambda y: y[2])

g = open("TPOSCAR", "a+")

for i in range(49):
    g.write(x[i][0] + " " + x[i][1] + " " +  x[i][2] + "\n ") 

print(x)