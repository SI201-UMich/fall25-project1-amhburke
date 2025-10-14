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
                "body_mass_g": row["body_mass_g"],
                "island": row["island"]
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

#print(get_penguin_species(penguins))

def average_flipper_length(adelie_penguins):
    """Calculates the average flipper length of Adelie penguins"""
    total_length = 0
    count = 0

    for penguin in adelie_penguins.values():
        flipper = penguin["flipper_length_mm"]

        if flipper and flipper != "NA":
            total_length += float(flipper)
            count += 1

    if count == 0:
        return 0

    average_length = total_length / count
    return round(average_length, 2)

#penguins = load_penguins('penguins.csv')             
#adelie_penguins = get_penguin_species(penguins)      
#print(average_flipper_length(adelie_penguins)) 

def find_above_average(adelie_penguins, average_length, island):
    """Finds all the Adelie penguins on Biscoe island and returns the percentage that have above average flipper length"""
    total_on_island = 0
    above_count = 0

    for penguin in adelie_penguins.values():
        if penguin.get("island") != island:
            continue

        flipper = penguin.get("flipper_length_mm")
        if not flipper:
            continue

        s = str(flipper).strip()
        if s.upper() in ("NA", "N/A", "NAN", "NULL"):
            continue

        try:
            length = float(s)
        except ValueError:
            continue

        total_on_island += 1
        if length > average_length:
            above_count += 1

    if total_on_island == 0:
        return 0.0

    percentage = (above_count / total_on_island) * 100.0
    return round(percentage, 1)

#adelie_penguins = get_penguin_species(penguins)      
#print(find_above_average(adelie_penguins, 189.95, "Biscoe"))


def results(average, percentage, filename="results.txt"):
    """Writes the calculated average and percentage above average to a text file."""
    # Coerce inputs to floats if possible
    try:
        avg = float(average)
    except (TypeError, ValueError):
        avg = None

    try:
        pct = float(percentage)
    except (TypeError, ValueError):
        pct = None

    lines = []
    if avg is not None:
        lines.append(f"Average Adelie flipper length: {avg:.1f} mm")
    else:
        lines.append("Average Adelie flipper length: N/A")

    if pct is not None:
        lines.append(f"Percent above average on Biscoe: {pct:.1f}%")
    else:
        lines.append("Percent above average on Biscoe: N/A")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

adelie_penguins = get_penguin_species(penguins)
avg = average_flipper_length(adelie_penguins)
pct = find_above_average(adelie_penguins, avg, "Biscoe")
results(avg, pct)  
