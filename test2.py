f = open("POSCAR2", "r")
f_read = f.readlines()

def species():
    species = []
    count = 0
    atom_count = 0

    atoms = [int(i) for i in f_read[6].split()]

    for row in f_read[8:]:
        if count == 0:
            species.append([])
        info = row.split()  # if you want to add just a value you can do that here too, for now im just adding the whole row
        species[len(species) - 1].append(info)
        count += 1
        if count == atoms[atom_count]:
            count = 0
            atom_count += 1

    # access species here
    print(species)

species()