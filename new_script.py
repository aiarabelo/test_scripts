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
        FUNCTION: writes the first 7 lines of the POSCAR
        TODO: Change this to 5 if Bi-u modeling 
        """
        for i in range(0,7):
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

    def parse_coordinates(self, atomic_specie=None):
        self.overall_list_of_coordinates = self.initialize_list_of_elements()
        c = 8 + int(self.number_of_atoms[self.j])

        for i in range(8, len(self.f_read)):
            self.overall_list_of_coordinates[self.j].append(self.f_read[i].split( ))

            if i == c - 1: 
                try:
                    print("Current atom: ", self.atomic_species[self.j])
                    self.j = self.j + 1
                    c = c + int(self.number_of_atoms[self.j])
                except:
                    print("end of loop")
            else:
                continue

        return self.overall_list_of_coordinates
            
        
    def loop_over_elements(self):
        pass

    def execute(self):
        # Delete this; this is for testing only
        self.write_preamble()
        self.parse_coordinates()


pf = ProcessFile()
pf.execute()