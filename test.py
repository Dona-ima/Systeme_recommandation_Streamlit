import csv

with open('appusers.csv', mode='r', newline='') as file:
    reader = csv.DictReader(file)
    print(reader.fieldnames)  # Affiche les noms des colonnes