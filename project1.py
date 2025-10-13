import csv

def main():
    """Main function to execute the program logic."""

def load_penguins(csv_file):
    """Reads csv and creates a list of dictionaries containing species, flipper length, and body mass."""
    penguins = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            penguin = {
                "species": row["species"],
                "flipper_length_mm": row["flipper_length_mm"], 
                "body_mass_g": row["body_mass_g"] 
            }
            penguins.append(penguin)
    return penguins

penguins = load_penguins('penguins.csv')
#print(penguins)

def get_penguin_species(penguins):
    """Creates a dictionary of only Adelie penguins information"""
    adelie_penguins = {}
    index = 0

    for penguin in penguins:
        if penguin["species"] == "Adelie":
            adelie_penguins[index] = penguin
            index += 1

    return adelie_penguins

print(get_penguin_species(penguins))



def average_flipper_length(adelie_penguins):
    """Calculates the average flipper length of Adelie penguins"""

def find_above_average(adelie_penguins, average_length, island):
    """Finds all the Adelie penguins on Biscoe island and returns the percentage that have above average flipper length"""

def results(average, percentage):
    """Writes the calculated average and percentage aboce average to a text file"""