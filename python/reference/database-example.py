import random

def make_hr_records(contacts):
    entries = []
    contact_sample = random.sample(contacts, round(len(contacts) / 2))
    for contact in contact_sample:
        # columns: ID number, isJedi, isSith, salary in USD, midichlorian count
        entries.append([ contact[0], bool(random.getrandbits(1)), bool(random.getrandbits(1)), random.randint(16000, 250000), random.randint(0, 10000)])
    return entries

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

employees = generate_entries(10)
hr_records = make_hr_records(employees)
print(employees)
print(hr_records)