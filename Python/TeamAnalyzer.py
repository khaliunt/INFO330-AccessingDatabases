import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
conn = sqlite3.connect('pokemon.sqlite')
c = conn.cursor()

for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    # Analyze the pokemon whose pokedex_number is in "arg"
    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type

    # Pokemon name and type(s)
    c.execute("SELECT identifier, type1, type2 FROM pokemon WHERE id = ?", (arg,))
    row = c.fetchone()
    if not row:
        print(f"Could not find Pokemon with pokedex number {arg}")
        continue
    name, type1, type2 = row
    types_str = type1
    if type2:
        types_str += f"/{type2}"
    print(f"Analyzing {arg}\n{name} ({types_str})")

    # Types of Pokemon
strong_types = []
weak_types = []
for t in types:
        c.execute(f"SELECT against_{t} FROM type_efficacy WHERE damage_type_id = ?", (type1,))
        damage_factor = c.fetchone()[0]
        if damage_factor > 1:
            strong_types.append(t)
        elif damage_factor < 1:
            weak_types.append(t)
        if type2:
            c.execute(f"SELECT against_{t} FROM type_efficacy WHERE damage_type_id = ?", (type2,))
            damage_factor = c.fetchone()[0]
            if damage_factor > 1:
                strong_types.append(t)
            elif damage_factor < 1:
                weak_types.append(t)
print(f"Strong against: {', '.join(strong_types)}")
print(f"Weak against: {', '.join(weak_types)}")

team.append(arg)
print(f"{name} ({type1}{' '+type2 if type2 else ''}) is strong against {strong_types} but weak against {weak_types}")


answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

        # Write the pokemon team to the "teams" table

print("Saving " + teamName + " ...")
print("Bye for now!")