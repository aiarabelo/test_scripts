f = open("POSCAR2", "r")
f_read = f.readlines()

x = [f_read[i].split( ) for i in range(8,len(f_read))]


x.sort(key=lambda y: y[1])
x.sort(key=lambda y: y[2])

g = open("TPOSCAR", "a+")

for i in range(49):
    g.write(x[i][0] + " " + x[i][1] + " " +  x[i][2] + "\n ") 


def get_heights(self):
    heights = []

    for height in range(8, len(self.f_read) - self.adsorbate_atoms):
        heights.append(self.f_read[height].split( )[2])

    max_height = float(max(heights))

    height_range = max_height/self.tot_layers
    self.adjusted_height_range = height_range - self.tolerance
    bulk_height = self.adjusted_height_range*(self.tot_layers-self.surface_layers)
    return bulk_height


print(str(x))