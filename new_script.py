import re

class ProcessFile:
    """
    FUNCTION: Provides methods for reading the POSCAR file
    """
    def __init__(self, filename = "POSCAR2", output_filename = "xPOSCAR"):
        self.filename = filename
        self.output_filename = output_filename
        self.wf = open(self.output_filename, "a+")

        f = open(self.filename, "r")
        self.f_read = f.readlines()

        self.j = 0        
        self.atomic_species = self.f_read[5].split( )
        self.number_of_atoms = self.f_read[6].split( )

    def write_preamble(self):
        """
        FUNCTION: writes the first 5 lines of the POSCAR
        TODO: Change this to 5 if Bi-u modeling 
        """
        for i in range(0,5):
            self.wf.write(self.f_read[i])

    def initialize_list_of_elements(self):
        """
        FUNCTION: Returns a list of empty lists, for the purpose of filling it up
                  with coordinates of elements later on 
                  The number of empty lists is the same as the number of atom species
        """
        overall_list_of_elements = []
        for i in range(len(self.atomic_species)): # this works but i guess this can be refactored to something better
            placeholder = []
            overall_list_of_elements.append(placeholder)
        return overall_list_of_elements

    def parse_coordinates(self):
        """
        FUNCTION: Each loop creates appends a list of x, y, z coordinates corresponding to each
                  row in the POSCAR to the empty list generated by initialize_list_of_elements
                  based on the atomic species it corresponds to.
        """
        
        self.overall_list_of_coordinates = self.initialize_list_of_elements()
        c = 8 + int(self.number_of_atoms[self.j])

        for i in range(8, len(self.f_read)):
            x = self.f_read[i].split( )
            x.append(self.atomic_species[self.j])
            self.overall_list_of_coordinates[self.j].append(x)

            if i == c - 1: 
                try:
                    print("Atom read: ", self.atomic_species[self.j])
                    self.j = self.j + 1
                    c = c + int(self.number_of_atoms[self.j])
                except:
                    print("finished reading atoms")
            else:
                continue

        return self.overall_list_of_coordinates

    def write_labels(self):
        """
        FUNCTION: writes the desired labels, based on functionality enabled 
        """
        pass      
        
    def loop_over_elements(self):
        pass

class SelectiveDynamics(ProcessFile):
    """
    FUNCTION: Freezes based on given height 
    TODO: Base on # of desired layers to be frozen as well 
    """
    def __init__(self, height):
        ProcessFile.__init__(self)
        self.overall_list_of_coordinates = self.parse_coordinates()
        self.height = float(height)
    
    def define_sd_labels(self, i, j):
        if float(self.overall_list_of_coordinates[i][j][2]) < self.height:
            label = "T T T !"
        else:
            label = "F F F !"
        return label

    def write_coordinates(self): 
        for i in range(len(self.overall_list_of_coordinates)):
            for j in range(len(self.overall_list_of_coordinates[i])):
                print(self.overall_list_of_coordinates[i][j])
                label = self.define_sd_labels(i, j)
                self.wf.write("%s %s %s %s \n" % (self.overall_list_of_coordinates[i][j][0],
                                                  self.overall_list_of_coordinates[i][j][1],
                                                  self.overall_list_of_coordinates[i][j][2], 
                                                  label)
                             )
            print("Moving on")
        
    def execute(self):
        self.write_preamble()
        for i in range(5,7):
            self.wf.write(self.f_read[i])
        self.wf.write("Selective Dynamics \n")
        self.write_coordinates()

class BiUModeling(ProcessFile):
    """
	FUNCTION: This class provides methods to adjust the POSCAR to treat a certain 
			  layer as the bulk and another layer as the surface depending on
			  the number of layers specified
	REMINDER: Put the adsorbate at the end 
	TODO: This is hardcoded for CuO (clean). Consider bond length z-components from PyMatGen and surfaces with adsorbed atoms
	"""
    def __init__(self, tot_layers = 7, surface_layers = 2, adsorbate_atoms = 0,
                 tolerance = 0):
        ProcessFile.__init__(self)
       
        self.tot_layers = int(tot_layers)
        self.surface_layers = int(surface_layers)
        self.adsorbate_atoms = int(adsorbate_atoms)
        self.tolerance = float(tolerance)

    def get_adjusted_height_range(self):
        """
        FUNCTION: Returns the approximate height of each layer
        """
        heights = []
        for height in range(8, len(self.f_read) - self.adsorbate_atoms):
            heights.append(self.f_read[height].split( )[2])

        max_height = float(max(heights))
        height_range = max_height/self.tot_layers
        adjusted_height_range = height_range - self.tolerance
        return adjusted_height_range

    def get_bulk_height(self):
        self.adjusted_height_range = self.get_adjusted_height_range()
        bulk_height = self.adjusted_height_range*(self.tot_layers-self.surface_layers)
        return bulk_height
    
    def get_number_of_bulk_atoms(self):
        """
        FUNCTION: Returns the number of transition metal bulk atoms
        """
        pass

    def execute(self):
        self.write_preamble()
        self.atomic_species.insert(0, '%s_B' % self.atomic_species[0])
        for i in range(len(self.atomic_species)):
            self.wf.write(" %s" % (self.atomic_species[i]))
        self.wf.write("\n")

biu = BiUModeling()
biu.execute()
