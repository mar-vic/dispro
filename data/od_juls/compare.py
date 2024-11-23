import csv

# with open("./druhy_zoznam__dirty.csv", "r") as f:
# reader = csv.DictReader(f, delimiter=";")
# titles = []
#
# with open("./druhy_zoznam.csv", "w") as f:
#     fieldnames = ["Author", "Name", "Bibliography"]
#     writer = csv.DictWriter(f, fieldnames)
#     writer.writeheader()
#
#     for row in reader:
#         name = row["bib"].split(":")[1].split(".")[0].strip()
#         author = row["bib"].split(":")[0]
#         bib = row["bib"]
#         writer.writerow({"Author": author, "Name": name, "Bibliography": bib})
#         # titles.append(row["bib"])
#
# print(titles[0].split(":")[0])

druhy_zoznam, treti_zoznam, dispro_zoznam = set(), set(), set()


with open("./druhy_zoznam.csv", "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        author = row["Author"]
        name = row["Name"]

        druhy_zoznam.add(name)

with open("./treti_zoznam.csv", "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        author = row["Author"]
        name = row["Name"]

        treti_zoznam.add(name)

with open("./dispro_zoznam.csv", "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        author = row["Autor"]
        name = row["Názov diela"]

        dispro_zoznam.add(name)

# iba_v_druhom = druhy_zoznam - treti_zoznam
# iba_v_tretom = treti_zoznam - druhy_zoznam
# v_oboch = druhy_zoznam & treti_zoznam

# print(f"\nTituly v oboch zoznamoch ({len(v_oboch)}):")
# print(v_oboch)
# print(f"\nTituly len v druhom zozname ({len(iba_v_druhom)}):")
# print(iba_v_druhom)
# print(f"\nTituly len v tretom zozname ({len(iba_v_tretom)}):")
# print(v_oboch)
print(
    f"\nTituly v tretom zozname a dispro zozname ({len(treti_zoznam & dispro_zoznam)}):"
)
print(treti_zoznam & dispro_zoznam)
print(
    f"\nTituly v tretom zozname, ktore sa nenachadzaju v dispro zozname ({len(treti_zoznam - dispro_zoznam)}):"
)
print(treti_zoznam - dispro_zoznam)


# for name in druhy_zoznam:
#     if name in treti_zoznam:
#         v_oboch.append(name)
#     else:
#         iba_v_druhom.append(name)
#
# for name in treti_zoznam:
#     if name not in druhy_zoznam:
#         iba_v_tretom.append(name)
