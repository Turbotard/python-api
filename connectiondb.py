import mysql.connector

# Tentative de connexion à la base de données
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="python_api",
        port="8889"
    )

    if db.is_connected():
        print("Connexion à la base de données réussie.")
        # Vous pouvez exécuter des opérations sur la base de données ici
except mysql.connector.Error as e:
    print(f"Erreur lors de la connexion à la base de données : {e}")
finally:
    # Fermeture de la connexion
    if db.is_connected():
        db.close()
        print("Connexion à la base de données fermée.")

