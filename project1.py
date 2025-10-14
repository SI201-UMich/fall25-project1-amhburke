import os
import csv
import unittest
import tempfile

def main():
    csv_file = "penguins.csv"
    island = "Biscoe"

    try:
        penguins = load_penguins(csv_file)
        adelie_penguins = get_penguin_species(penguins)
        avg = average_flipper_length(adelie_penguins)
        pct = find_above_average(adelie_penguins, avg, island)

        results(avg, pct)  
        print(f"Average Adelie flipper length: {avg:.1f} mm")
        print(f"Percent above average on {island}: {pct:.1f}%")
        print('Results written to "results.txt".')

    except FileNotFoundError:
        print(f'Could not find "{csv_file}". Make sure it is in the same folder as this program.')


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

#penguins = load_penguins('penguins.csv')
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

    target = str(island).strip().lower()

    for penguin in adelie_penguins.values():
        isl = str(penguin.get("island","")).strip().lower()
        if isl != target:
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

#adelie_penguins = get_penguin_species(penguins)
#avg = average_flipper_length(adelie_penguins)
#pct = find_above_average(adelie_penguins, avg, "Biscoe")
#results(avg, pct)  

if __name__ == "__main__":
    main()





def write_csv(path, rows):
    headers = ["", "species", "island", "bill_length_mm", "bill_depth_mm",
               "flipper_length_mm", "body_mass_g", "sex", "year"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for r in rows:
            row = {h: "" for h in headers}  
            row.update(r)
            w.writerow(row)


class TestLoadPenguins(unittest.TestCase):
    def test_basic_load_returns_expected_fields(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tf:
            write_csv(tf.name, [
                {"": "1", "species": "Adelie", "island": "Biscoe",
                 "flipper_length_mm": "190", "body_mass_g": "3700"},
                {"": "2", "species": "Gentoo", "island": "Torgersen",
                 "flipper_length_mm": "210", "body_mass_g": "5000"},
            ])
        try:
            data = load_penguins(tf.name)
            self.assertEqual(len(data), 2)
            self.assertEqual(set(data[0].keys()),
                             {"species", "flipper_length_mm", "body_mass_g", "island"})
            self.assertEqual(data[0]["species"], "Adelie")
            self.assertEqual(data[1]["flipper_length_mm"], "210")
        finally:
            os.remove(tf.name)

    def test_handles_missing_flipper_length(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tf:
            write_csv(tf.name, [
                {"": "1", "species": "Adelie", "island": "Dream",
                 "flipper_length_mm": "", "body_mass_g": "3800"},
            ])
        try:
            data = load_penguins(tf.name)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["flipper_length_mm"], "")
        finally:
            os.remove(tf.name)

    def test_ignores_extra_columns(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tf:
            write_csv(tf.name, [
                {"": "1", "species": "Adelie", "island": "Biscoe",
                 "flipper_length_mm": "185", "body_mass_g": "3600",
                 "bill_depth_mm": "18.5", "sex": "F"},
            ])
        try:
            data = load_penguins(tf.name)
            self.assertEqual(len(data), 1)
            self.assertNotIn("bill_depth_mm", data[0])
            self.assertNotIn("sex", data[0])
        finally:
            os.remove(tf.name)

    def test_preserves_island_value(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tf:
            write_csv(tf.name, [
                {"": "1", "species": "Adelie", "island": "Biscoe",
                 "flipper_length_mm": "191", "body_mass_g": "3700"},
            ])
        try:
            data = load_penguins(tf.name)
            self.assertEqual(data[0]["island"], "Biscoe")
        finally:
            os.remove(tf.name)


class TestGetPenguinSpecies(unittest.TestCase):
    def test_filters_only_adelie(self):
        penguins = [
            {"species": "Adelie", "flipper_length_mm": "190", "body_mass_g": "3700", "island": "Biscoe"},
            {"species": "Gentoo", "flipper_length_mm": "210", "body_mass_g": "5000", "island": "Biscoe"},
            {"species": "Adelie", "flipper_length_mm": "186", "body_mass_g": "3600", "island": "Dream"},
        ]
        adelies = get_penguin_species(penguins)
        self.assertEqual(len(adelies), 2)
        for v in adelies.values():
            self.assertEqual(v["species"], "Adelie")

    def test_no_adelie_returns_empty_dict(self):
        penguins = [
            {"species": "Chinstrap", "flipper_length_mm": "195", "body_mass_g": "3700", "island": "Dream"},
        ]
        adelies = get_penguin_species(penguins)
        self.assertEqual(adelies, {})

    def test_index_keys_are_sequential(self):
        penguins = [
            {"species": "Adelie", "flipper_length_mm": "180", "body_mass_g": "3400", "island": "Biscoe"},
            {"species": "Adelie", "flipper_length_mm": "185", "body_mass_g": "3500", "island": "Biscoe"},
            {"species": "Adelie", "flipper_length_mm": "190", "body_mass_g": "3600", "island": "Biscoe"},
        ]
        adelies = get_penguin_species(penguins)
        self.assertEqual(set(adelies.keys()), {0, 1, 2})

    def test_includes_entries_with_missing_fields(self):
        penguins = [
            {"species": "Adelie", "flipper_length_mm": "", "body_mass_g": "3600", "island": "Dream"},
            {"species": "Adelie", "flipper_length_mm": "190", "body_mass_g": "", "island": "Biscoe"},
        ]
        adelies = get_penguin_species(penguins)
        self.assertEqual(len(adelies), 2)


class TestAverageFlipperLength(unittest.TestCase):
    def test_average_normal_values(self):
        adelies = {
            0: {"flipper_length_mm": "190"},
            1: {"flipper_length_mm": "200"},
        }
        self.assertEqual(average_flipper_length(adelies), 195.0)

    def test_skips_NA(self):
        adelies = {
            0: {"flipper_length_mm": "190"},
            1: {"flipper_length_mm": "NA"},
        }
        self.assertEqual(average_flipper_length(adelies), 190.0)

    def test_skips_empty_string(self):
        adelies = {
            0: {"flipper_length_mm": "180"},
            1: {"flipper_length_mm": ""},
        }
        self.assertEqual(average_flipper_length(adelies), 180.0)

    def test_returns_zero_when_no_valid_entries(self):
        adelies = {
            0: {"flipper_length_mm": "NA"},
            1: {"flipper_length_mm": ""},
        }
        self.assertEqual(average_flipper_length(adelies), 0.0)


class TestFindAboveAverage(unittest.TestCase):
    def test_basic_percentage_calculation(self):
        adelies = {
            0: {"island": "Biscoe", "flipper_length_mm": "180"},
            1: {"island": "Biscoe", "flipper_length_mm": "195"},
            2: {"island": "Biscoe", "flipper_length_mm": "200"},
            3: {"island": "Torgersen", "flipper_length_mm": "210"},
        }
        pct = find_above_average(adelies, average_length=190.0, island="Biscoe")
        self.assertEqual(pct, 66.7)  # 2 of 3 -> 66.7%

    def test_island_matching_is_case_insensitive(self):
        adelies = {
            0: {"island": "bIsCoE", "flipper_length_mm": "191"},
            1: {"island": "BISCOE", "flipper_length_mm": "170"},
        }
        pct = find_above_average(adelies, average_length=190.0, island="biscoe")
        self.assertEqual(pct, 50.0)

    def test_skips_invalid_flipper_values_in_denominator(self):
        adelies = {
            0: {"island": "Biscoe", "flipper_length_mm": "NA"},
            1: {"island": "Biscoe", "flipper_length_mm": "195"},
            2: {"island": "Biscoe", "flipper_length_mm": "180"},
        }
        pct = find_above_average(adelies, average_length=190.0, island="Biscoe")
        self.assertEqual(pct, 50.0)  # 1 of 2 valid entries

    def test_returns_zero_when_no_penguins_on_island(self):
        adelies = {
            0: {"island": "Dream", "flipper_length_mm": "200"},
        }
        pct = find_above_average(adelies, average_length=190.0, island="Biscoe")
        self.assertEqual(pct, 0.0)


class TestResults(unittest.TestCase):
    def test_writes_numbers_to_default_file(self):
        with tempfile.TemporaryDirectory() as td:
            fname = os.path.join(td, "results.txt")
            # patch: pass filename explicitly to avoid writing in CWD
            results(189.25, 42.66, filename=fname)
            with open(fname, "r", encoding="utf-8") as f:
                content = f.read().strip().splitlines()
            self.assertEqual(content[0], f"Average Adelie flipper length: {189.25:.1f} mm")
            self.assertEqual(content[1], "Percent above average on Biscoe: 42.7%")

    def test_writes_when_inputs_are_strings(self):
        with tempfile.TemporaryDirectory() as td:
            fname = os.path.join(td, "results.txt")
            results("189.24", "43.34", filename=fname)
            with open(fname, "r", encoding="utf-8") as f:
                lines = f.read().strip().splitlines()
            self.assertEqual(lines[0], "Average Adelie flipper length: 189.2 mm")
            self.assertEqual(lines[1], "Percent above average on Biscoe: 43.3%")

    def test_handles_invalid_inputs(self):
        with tempfile.TemporaryDirectory() as td:
            fname = os.path.join(td, "results.txt")
            results("not-a-number", None, filename=fname)
            with open(fname, "r", encoding="utf-8") as f:
                lines = f.read().strip().splitlines()
            self.assertEqual(lines[0], "Average Adelie flipper length: N/A")
            self.assertEqual(lines[1], "Percent above average on Biscoe: N/A")

    def test_custom_filename_is_respected(self):
        with tempfile.TemporaryDirectory() as td:
            custom = os.path.join(td, "my_output.txt")
            results(190.0, 50.0, filename=custom)
            self.assertTrue(os.path.exists(custom))
            with open(custom, "r", encoding="utf-8") as f:
                txt = f.read().strip()
            self.assertIn("Average Adelie flipper length: 190.0 mm", txt)
            self.assertIn("Percent above average on Biscoe: 50.0%", txt)


if __name__ == "__main__":
    unittest.main(verbosity=2)
