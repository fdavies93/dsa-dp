import random

def generate_entries(to_make : int = 1000):
    first_names = ["Luke", "Leia", "Han", "Obi-Wan", "Darth", "Sheev", "Ben", "Rey", "Lando", "Jabba", "Padme", "Chewbacca", "R2", "Wedge", "JarJar", "Count", "Boba", "Jango"]
    last_names = ["Skywalker", "Organa", "Solo", "Kenobi", "Vader", "Palpatine", "Calrissian", "Von Hutt", "Amidala", "D2", "Antilles", "Bane", "Binks", "Dooku", "Fett"]
    entries = []

    for i in range(to_make):
        first_nm = random.choice(first_names)
        last_nm = random.choice(last_names)
        email = first_nm.replace(" ", "").lower() + last_nm.replace(" ", "").lower() + str(i) + "@evilcorp.com"
        entries.append([i, first_nm, last_nm, email])

    return entries

print(generate_entries(10))