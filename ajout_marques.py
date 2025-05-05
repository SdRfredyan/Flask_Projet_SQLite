import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

marques = [
    "Peugeot", "Renault", "Citroën", "DS", "Bugatti", "Volkswagen", "Audi", "BMW", "Mercedes", "Porsche", "Opel",
    "Fiat", "Alfa Romeo", "Ferrari", "Maserati", "Lancia", "Lamborghini",
    "Toyota", "Honda", "Nissan", "Mazda", "Suzuki", "Mitsubishi", "Subaru", "Lexus", "Infiniti", "Isuzu",
    "Ford", "Chevrolet", "Dodge", "Jeep", "Tesla",
    "Aston Martin", "Bentley", "Rolls-Royce", "Jaguar", "Land Rover", "Mini", "McLaren", "MG", "Lotus",
    "Hyundai", "Kia",
    "Volvo", "Koenigsegg", "BYD", "Lynk & Co",
    "Dacia", "Skoda", "SEAT", "Cupra", "Smart"
]

for marque in marques:
    try:
        cursor.execute("INSERT INTO marque (nom) VALUES (?)", (marque,))
    except sqlite3.IntegrityError:
        pass  # La marque existe déjà

conn.commit()
conn.close()
print("✅ Marques ajoutées avec succès.")
